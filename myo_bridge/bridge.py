"""myo-bridge: keeps one Myo connected and links it to the Mac.

Gestures in: the band's own pose classifier → GestureTracker → a Hammerspoon URL
(hammerspoon://myo?gesture=NAME), where ~/.hammerspoon/myo.lua decides what each does.
Buzzes out: any program writes a pattern name to the Unix socket SOCKET_PATH
(`myo-buzz waiting`), and the band vibrates.

It also writes the band's state to STATE_DIR/status.json and logs the battery
every few minutes to STATE_DIR/battery.jsonl, which doubles as the battery-health test.

macOS kills a Bluetooth program whose starting app declares no Bluetooth use, so run
it from Ghostty, the Claude app's Terminal panel, or the MyoBridge app (see README).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import urlencode

from . import protocol as P
from .gestures import GestureTracker

SOCKET_PATH = Path(os.environ.get("MYO_BRIDGE_SOCKET", "/tmp/myo-bridge.sock"))
STATE_DIR = Path(os.environ.get("MYO_BRIDGE_STATE", Path.home() / ".local/state/myo-bridge"))
BATTERY_EVERY_S = 300
TICK_S = 0.1
FEEDBACK = {"double_tap": "short", "fist_hold_start": "short"}

log = logging.getLogger("myo-bridge")


def hammerspoon_dispatch(gesture: str, **extra: str) -> None:
    """Hand a gesture to Hammerspoon. `open -g` returns at once and keeps focus."""
    url = "hammerspoon://myo?" + urlencode({"gesture": gesture, **extra})
    subprocess.run(["/usr/bin/open", "-g", url], check=False, timeout=5)


class Bridge:
    """Everything that happens on a connected band, independent of how it was found."""

    def __init__(self, dispatch=hammerspoon_dispatch, clock=time.monotonic, state_dir: Path = STATE_DIR):
        self.dispatch = dispatch
        self.clock = clock
        self.state_dir = state_dir
        self.tracker = GestureTracker()
        self.client = None
        self.status: dict = {"connected": False, "synced": False}

    # -- band events -------------------------------------------------------

    def on_classifier(self, data: bytes) -> list[str]:
        try:
            ev = P.parse_classifier_event(bytes(data))
        except ValueError as e:
            log.warning("bad classifier event %s: %s", bytes(data).hex(), e)
            return []
        out: list[str] = []
        if ev.type == P.EventType.POSE and ev.pose is not None:
            out = self.tracker.on_pose(ev.pose, self.clock())
            self.status["last_pose"] = ev.pose.name.lower()
        elif ev.type == P.EventType.ARM_SYNCED:
            self._set(synced=True)
            out = ["synced"]
            if self.client is not None:
                asyncio.ensure_future(self.command(P.cmd_unlock("hold")))  # report every pose
        elif ev.type in (P.EventType.ARM_UNSYNCED, P.EventType.SYNC_FAILED):
            self._set(synced=False)
            out = self.tracker.reset() + ["unsynced"]
        for g in out:
            self.emit(g)
        return out

    def tick(self) -> list[str]:
        out = self.tracker.on_tick(self.clock())
        for g in out:
            self.emit(g)
        return out

    def emit(self, gesture: str) -> None:
        log.info("gesture %s", gesture)
        self.status["last_gesture"] = gesture
        self.status["last_gesture_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        self._write_status()
        try:
            self.dispatch(gesture)
        except Exception as e:  # a failed hand-off must not drop the band
            log.warning("dispatch of %s failed: %s", gesture, e)
        if gesture in FEEDBACK and self.client is not None:
            asyncio.ensure_future(self.buzz(FEEDBACK[gesture]))

    # -- commands to the band ----------------------------------------------

    async def command(self, payload: bytes) -> None:
        await self.client.write_gatt_char(P.COMMAND_CHAR, payload, response=True)

    async def buzz(self, pattern: str) -> str:
        if pattern not in P.PATTERNS:
            return f"unknown pattern {pattern!r}; known: {', '.join(P.PATTERNS)}"
        if self.client is None or not self.status.get("connected"):
            return "not connected"
        await self.command(P.PATTERNS[pattern])
        return "ok"

    async def read_battery(self) -> int:
        level = (await self.client.read_gatt_char(P.BATTERY_CHAR))[0]
        self._set(battery=level)
        self.state_dir.mkdir(parents=True, exist_ok=True)
        with open(self.state_dir / "battery.jsonl", "a") as f:
            f.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "battery": level,
                                "synced": self.status.get("synced", False)}) + "\n")
        return level

    # -- connection lifecycle ----------------------------------------------

    async def attach(self, client) -> None:
        """Set the band up once connected: info, classifier stream, battery."""
        self.client = client
        fw = P.parse_firmware(await client.read_gatt_char(P.FIRMWARE_CHAR))
        serial = P.parse_serial(await client.read_gatt_char(P.INFO_CHAR))
        self._set(connected=True, synced=False, firmware=fw, serial=serial)
        await client.start_notify(P.CLASSIFIER_EVENT_CHAR, lambda _c, d: self.on_classifier(d))
        await self.command(P.cmd_set_mode(emg=0x00, imu=0x00, classifier=0x01))
        await self.read_battery()
        log.info("attached: firmware %s, serial %s, battery %s %%", fw, serial, self.status["battery"])
        self.emit("connected")

    def detach(self) -> None:
        for g in self.tracker.reset():
            self.emit(g)
        self.client = None
        self._set(connected=False, synced=False)
        self.emit("disconnected")

    def _set(self, **kv) -> None:
        self.status.update(kv)
        self._write_status()

    def _write_status(self) -> None:
        try:
            self.state_dir.mkdir(parents=True, exist_ok=True)
            tmp = self.state_dir / "status.json.tmp"
            tmp.write_text(json.dumps(self.status, indent=2))
            tmp.replace(self.state_dir / "status.json")
        except OSError as e:
            log.warning("status write failed: %s", e)


# -- the buzz socket -------------------------------------------------------

async def serve_socket(bridge: Bridge, path: Path = SOCKET_PATH) -> asyncio.AbstractServer:
    async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            line = (await asyncio.wait_for(reader.readline(), 5)).decode().strip()
            if line == "status":
                reply = json.dumps(bridge.status)
            else:
                reply = await bridge.buzz(line or "short")
        except Exception as e:
            reply = f"error: {e}"
        writer.write((reply + "\n").encode())
        await writer.drain()
        writer.close()

    if path.exists():
        path.unlink()
    server = await asyncio.start_unix_server(handle, path=str(path))
    os.chmod(path, 0o600)
    return server


# -- finding and holding the band -------------------------------------------

async def find_myo(timeout: float):
    from bleak import BleakScanner

    def is_myo(device, adv) -> bool:
        uuids = [u.lower() for u in adv.service_uuids]
        return P.CONTROL_SERVICE in uuids or "myo" in (adv.local_name or device.name or "").lower()

    return await BleakScanner.find_device_by_filter(is_myo, timeout=timeout)


async def run(bridge: Bridge) -> None:
    from bleak import BleakClient

    server = await serve_socket(bridge)
    log.info("buzz socket at %s", SOCKET_PATH)

    async def ticker():
        while True:
            await asyncio.sleep(TICK_S)
            bridge.tick()

    tick_task = asyncio.create_task(ticker())
    backoff = 2.0
    try:
        while True:
            device = await find_myo(timeout=20)
            if device is None:
                log.debug("no Myo advertising; scanning again")
                await asyncio.sleep(backoff)
                backoff = min(backoff * 1.5, 30)
                continue
            backoff = 2.0
            disconnected = asyncio.Event()
            log.info("connecting to %s (%s)", device.name, device.address)
            try:
                async with BleakClient(device, timeout=20,
                                       disconnected_callback=lambda _c: disconnected.set()) as client:
                    await bridge.attach(client)
                    while not disconnected.is_set():
                        try:
                            await asyncio.wait_for(disconnected.wait(), BATTERY_EVERY_S)
                        except asyncio.TimeoutError:
                            await bridge.read_battery()
            except Exception as e:
                log.warning("connection lost: %s: %s", type(e).__name__, e)
            finally:
                if bridge.status.get("connected"):
                    bridge.detach()
            await asyncio.sleep(1)
    finally:
        tick_task.cancel()
        server.close()
        SOCKET_PATH.unlink(missing_ok=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--scan-only", type=float, metavar="SECONDS",
                    help="scan once, log what Bluetooth sees, and exit (checks permission)")
    args = ap.parse_args()
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler(STATE_DIR / "bridge.log")])
    logging.getLogger("bleak").setLevel(logging.WARNING)
    if args.scan_only:
        from bleak import BleakScanner
        found = asyncio.run(BleakScanner.discover(timeout=args.scan_only))
        myo = asyncio.run(find_myo(timeout=1)) if found else None
        log.info("scan-only: %d Bluetooth devices seen, Myo %s", len(found), "found" if myo else "not found")
        return
    try:
        asyncio.run(run(Bridge()))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()

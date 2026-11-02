"""The bridge against a fake band: no Bluetooth, no Hammerspoon."""
import asyncio
import json

import pytest

from myo_bridge import bridge as B
from myo_bridge import protocol as P


class FakeBand:
    def __init__(self, battery=87):
        self.writes: list[bytes] = []
        self.notify = {}
        self.battery = battery

    async def read_gatt_char(self, uuid):
        return {
            P.FIRMWARE_CHAR: bytes([1, 0, 5, 0, 0xB2, 0x07, 2, 0]),
            P.INFO_CHAR: bytes([1, 2, 3, 4, 5, 6]) + bytes(14),
            P.BATTERY_CHAR: bytes([self.battery]),
        }[uuid]

    async def write_gatt_char(self, uuid, data, response=True):
        assert uuid == P.COMMAND_CHAR
        self.writes.append(bytes(data))

    async def start_notify(self, uuid, cb):
        self.notify[uuid] = cb

    def send(self, *raw):
        self.notify[P.CLASSIFIER_EVENT_CHAR](None, bytes(raw))


class Clock:
    t = 0.0

    def __call__(self):
        return self.t


@pytest.fixture
def setup(tmp_path):
    sent: list[str] = []
    clock = Clock()
    br = B.Bridge(dispatch=sent.append, clock=clock, state_dir=tmp_path)
    return br, FakeBand(), sent, clock, tmp_path


async def settle():
    for _ in range(3):
        await asyncio.sleep(0)


def test_attach_reads_band_enables_classifier_and_logs_battery(setup):
    br, band, sent, _, tmp = setup

    async def go():
        await br.attach(band)
    asyncio.run(go())
    assert P.cmd_set_mode(0, 0, 1) in band.writes
    assert br.status["firmware"] == "1.5.1970 (rev D)" and br.status["battery"] == 87
    assert sent == ["connected"]
    log = [json.loads(l) for l in (tmp / "battery.jsonl").read_text().splitlines()]
    assert log[-1]["battery"] == 87
    assert json.loads((tmp / "status.json").read_text())["connected"] is True


def test_sync_unlocks_and_gestures_flow_with_feedback(setup):
    br, band, sent, clock, _ = setup

    async def go():
        await br.attach(band)
        band.send(1, 1, 1, 0, 0, 0)          # arm synced
        await settle()
        band.send(3, 5, 0, 0, 0, 0)          # double tap
        await settle()
        band.send(3, 1, 0, 0, 0, 0)          # fist
        clock.t = 0.7
        br.tick()
        await settle()
        band.send(3, 0, 0, 0, 0, 0)          # rest
        await settle()
    asyncio.run(go())
    assert sent == ["connected", "synced", "double_tap", "fist_hold_start", "fist_hold_end"]
    assert P.cmd_unlock("hold") in band.writes
    assert band.writes.count(P.cmd_vibrate("short")) == 2  # double tap + fist start


def test_unsync_closes_fist_hold(setup):
    br, band, sent, clock, _ = setup

    async def go():
        await br.attach(band)
        band.send(3, 1, 0, 0, 0, 0)
        clock.t = 1.0
        br.tick()
        band.send(2, 0, 0, 0, 0, 0)          # arm unsynced
        await settle()
    asyncio.run(go())
    assert sent[-2:] == ["fist_hold_end", "unsynced"]


def test_garbage_event_is_ignored(setup):
    br, band, sent, _, _ = setup
    assert br.on_classifier(b"") == []


def test_buzz_socket_end_to_end(setup, monkeypatch):
    import tempfile
    from pathlib import Path
    br, band, _, _, _ = setup
    sock = Path(tempfile.mkdtemp(prefix="myo", dir="/tmp")) / "b.sock"  # AF_UNIX paths cap at 104 bytes
    monkeypatch.setattr(B, "SOCKET_PATH", sock)

    async def ask(line):
        r, w = await asyncio.open_unix_connection(str(sock))
        w.write((line + "\n").encode())
        await w.drain()
        reply = (await r.readline()).decode().strip()
        w.close()
        return reply

    async def go():
        server = await B.serve_socket(br, sock)
        before = await ask("waiting")
        await br.attach(band)
        after = await ask("waiting")
        bad = await ask("tickle")
        status = json.loads(await ask("status"))
        server.close()
        return before, after, bad, status
    before, after, bad, status = asyncio.run(go())
    assert before == "not connected"
    assert after == "ok" and P.PATTERNS["waiting"] in band.writes
    assert bad.startswith("unknown pattern")
    assert status["connected"] is True


def test_detach_reports_disconnect(setup):
    br, band, sent, _, _ = setup

    async def go():
        await br.attach(band)
    asyncio.run(go())
    br.detach()
    assert sent[-1] == "disconnected" and br.status["connected"] is False

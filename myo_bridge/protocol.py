"""Myo Bluetooth LE protocol: UUIDs, command bytes and event parsing.

Built from Thalmic's myohw.h (github.com/thalmiclabs/myo-bluetooth) and the
byte order every working open-source library uses (little-endian, although the
header says big-endian). Pure functions only, so it can be tested without a band.
"""
from __future__ import annotations

import struct
from dataclasses import dataclass
from enum import IntEnum


def _uuid(short: int) -> str:
    return f"d506{short:04x}-a904-deb9-4748-2c7f4a124842"


CONTROL_SERVICE = _uuid(0x0001)
INFO_CHAR = _uuid(0x0101)
FIRMWARE_CHAR = _uuid(0x0201)
COMMAND_CHAR = _uuid(0x0401)
CLASSIFIER_EVENT_CHAR = _uuid(0x0103)
BATTERY_CHAR = "00002a19-0000-1000-8000-00805f9b34fb"


class Pose(IntEnum):
    REST = 0
    FIST = 1
    WAVE_IN = 2
    WAVE_OUT = 3
    FINGERS_SPREAD = 4
    DOUBLE_TAP = 5
    UNKNOWN = 0xFFFF


class EventType(IntEnum):
    ARM_SYNCED = 1
    ARM_UNSYNCED = 2
    POSE = 3
    UNLOCKED = 4
    LOCKED = 5
    SYNC_FAILED = 6
    WARMUP_COMPLETED = 7  # not in myohw.h; seen from real bands (OSA-MYO-Controller notes)


@dataclass(frozen=True)
class ClassifierEvent:
    type: EventType | int
    pose: Pose | None = None
    arm: int | None = None          # 1 right, 2 left, 0xff unknown
    x_direction: int | None = None  # 1 toward wrist, 2 toward elbow


def parse_classifier_event(data: bytes) -> ClassifierEvent:
    """Parse one classifier indication. The band may send 3 or 6 bytes."""
    if not data:
        raise ValueError("empty classifier event")
    kind = data[0]
    try:
        kind = EventType(kind)
    except ValueError:
        return ClassifierEvent(type=kind)
    if kind == EventType.POSE:
        if len(data) < 3:
            raise ValueError(f"pose event too short: {data.hex()}")
        (raw,) = struct.unpack_from("<H", data, 1)
        try:
            pose = Pose(raw)
        except ValueError:
            pose = Pose.UNKNOWN
        return ClassifierEvent(type=kind, pose=pose)
    if kind == EventType.ARM_SYNCED:
        arm = data[1] if len(data) > 1 else None
        x_dir = data[2] if len(data) > 2 else None
        return ClassifierEvent(type=kind, arm=arm, x_direction=x_dir)
    return ClassifierEvent(type=kind)


# Commands: [command id, payload length, payload...] written to COMMAND_CHAR.

def cmd_set_mode(emg: int = 0x00, imu: int = 0x00, classifier: int = 0x01) -> bytes:
    """emg 0 off/2 filtered/3 raw; imu 0 off/1 data/2 events/3 all; classifier 0/1."""
    return bytes([0x01, 0x03, emg, imu, classifier])


VIBRATE = {"short": 1, "medium": 2, "long": 3}


def cmd_vibrate(length: str = "short") -> bytes:
    return bytes([0x03, 0x01, VIBRATE[length]])


def cmd_vibrate_pattern(steps: list[tuple[int, int]]) -> bytes:
    """Extended vibrate: up to 6 (duration ms, strength 0-255) steps."""
    if len(steps) > 6:
        raise ValueError("at most 6 vibration steps")
    padded = list(steps) + [(0, 0)] * (6 - len(steps))
    body = b"".join(struct.pack("<HB", min(d, 0xFFFF), max(0, min(s, 255))) for d, s in padded)
    return bytes([0x07, len(body)]) + body


# Named buzz patterns the bridge accepts on its socket.
PATTERNS = {
    "short": cmd_vibrate("short"),
    "medium": cmd_vibrate("medium"),
    "long": cmd_vibrate("long"),
    "double": cmd_vibrate_pattern([(120, 255), (120, 0), (120, 255)]),
    "waiting": cmd_vibrate_pattern([(80, 200), (100, 0), (80, 200), (100, 0), (250, 255)]),
}


def cmd_sleep_mode(never_sleep: bool) -> bytes:
    return bytes([0x09, 0x01, 0x01 if never_sleep else 0x00])


UNLOCK = {"lock": 0, "timed": 1, "hold": 2}


def cmd_unlock(kind: str = "hold") -> bytes:
    return bytes([0x0A, 0x01, UNLOCK[kind]])


def parse_firmware(data: bytes) -> str:
    major, minor, patch, hw = struct.unpack("<4H", data[:8])
    rev = {1: "rev C", 2: "rev D"}.get(hw, f"hw {hw}")
    return f"{major}.{minor}.{patch} ({rev})"


def parse_serial(data: bytes) -> str:
    return ":".join(f"{b:02x}" for b in reversed(data[0:6]))

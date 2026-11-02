"""Byte layouts checked against OSA-MYO-Controller (dnlfbr), a library used with real
Myos on Apple Silicon. Its mock emits classifier events as 6-byte indications
[type, b1, b2, b3, 0, 0]; myohw.h documents 3 bytes. No real band was available,
so these fixtures come from that library and the header, not from a capture.
"""
import pytest

from myo_bridge.protocol import (
    PATTERNS, ClassifierEvent, EventType, Pose, cmd_set_mode, cmd_unlock,
    cmd_vibrate, cmd_vibrate_pattern, parse_classifier_event, parse_firmware, parse_serial,
)


def test_pose_event_six_bytes():
    ev = parse_classifier_event(bytes([3, 5, 0, 0, 0, 0]))
    assert ev == ClassifierEvent(type=EventType.POSE, pose=Pose.DOUBLE_TAP)


def test_pose_event_three_bytes_like_header():
    assert parse_classifier_event(bytes([3, 1, 0])).pose == Pose.FIST


def test_unknown_pose_value_maps_to_unknown():
    assert parse_classifier_event(bytes([3, 0xFF, 0xFF, 0, 0, 0])).pose == Pose.UNKNOWN
    assert parse_classifier_event(bytes([3, 9, 0])).pose == Pose.UNKNOWN


def test_arm_synced_reads_arm_and_direction():
    ev = parse_classifier_event(bytes([1, 1, 1, 2, 0, 0]))
    assert ev.type == EventType.ARM_SYNCED and ev.arm == 1 and ev.x_direction == 1


def test_unlisted_event_type_is_kept_as_int():
    assert parse_classifier_event(bytes([0x42, 0, 0])).type == 0x42


def test_empty_and_short_events_raise():
    with pytest.raises(ValueError):
        parse_classifier_event(b"")
    with pytest.raises(ValueError):
        parse_classifier_event(bytes([3, 1]))


def test_commands_match_header():
    assert cmd_set_mode(0, 0, 1) == bytes([0x01, 0x03, 0, 0, 1])
    assert cmd_vibrate("short") == bytes([0x03, 0x01, 0x01])
    assert cmd_unlock("hold") == bytes([0x0A, 0x01, 0x02])


def test_extended_vibrate_is_20_bytes_little_endian():
    b = cmd_vibrate_pattern([(300, 255)])
    assert len(b) == 20 and b[:2] == bytes([0x07, 18])
    assert b[2:5] == bytes([0x2C, 0x01, 0xFF])  # 300 ms little-endian, full strength
    assert b[5:] == bytes(15)
    with pytest.raises(ValueError):
        cmd_vibrate_pattern([(10, 10)] * 7)


def test_every_pattern_is_a_valid_command():
    for name, b in PATTERNS.items():
        assert b[0] in (0x03, 0x07), name
        assert len(b) == 2 + b[1], name


def test_firmware_and_serial():
    assert parse_firmware(bytes([1, 0, 5, 0, 0xB2, 0x07, 2, 0])) == "1.5.1970 (rev D)"
    assert parse_serial(bytes([0x11, 0x22, 0x33, 0x44, 0x55, 0x66]) + bytes(14)) == "66:55:44:33:22:11"

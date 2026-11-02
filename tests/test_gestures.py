from myo_bridge.gestures import GestureTracker
from myo_bridge.protocol import Pose


def test_quick_poses_fire_at_once():
    g = GestureTracker()
    assert g.on_pose(Pose.DOUBLE_TAP, 0.0) == ["double_tap"]
    assert g.on_pose(Pose.WAVE_OUT, 1.0) == ["wave_out"]
    assert g.on_pose(Pose.REST, 1.2) == []


def test_brief_fist_does_nothing():
    g = GestureTracker(fist_hold_seconds=0.6)
    assert g.on_pose(Pose.FIST, 0.0) == []
    assert g.on_tick(0.3) == []
    assert g.on_pose(Pose.REST, 0.4) == []
    assert g.on_tick(1.0) == []


def test_held_fist_starts_once_and_ends_on_release():
    g = GestureTracker(fist_hold_seconds=0.6)
    g.on_pose(Pose.FIST, 0.0)
    assert g.on_tick(0.7) == ["fist_hold_start"]
    assert g.on_tick(0.9) == []
    assert g.on_pose(Pose.REST, 2.0) == ["fist_hold_end"]


def test_fist_into_another_pose_ends_hold_then_fires_new_pose():
    g = GestureTracker(fist_hold_seconds=0.6)
    g.on_pose(Pose.FIST, 0.0)
    g.on_tick(1.0)
    assert g.on_pose(Pose.DOUBLE_TAP, 1.5) == ["fist_hold_end", "double_tap"]


def test_repeated_fist_reports_do_not_restart_the_timer():
    g = GestureTracker(fist_hold_seconds=0.6)
    g.on_pose(Pose.FIST, 0.0)
    g.on_pose(Pose.FIST, 0.5)
    assert g.on_tick(0.65) == ["fist_hold_start"]


def test_reset_closes_an_open_hold():
    g = GestureTracker(fist_hold_seconds=0.6)
    g.on_pose(Pose.FIST, 0.0)
    g.on_tick(1.0)
    assert g.reset() == ["fist_hold_end"]
    assert g.reset() == []

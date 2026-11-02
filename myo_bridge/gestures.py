"""Turn the band's pose stream into the gestures the Mac acts on.

The band reports a pose each time it changes (rest, fist, wave in, ...).
Quick poses fire at once; a fist fires only after it has been held for
FIST_HOLD_SECONDS, so grabbing a cup does not start dictation, and it ends
when the hand relaxes. Pure logic with an injected clock, so it is testable.
"""
from __future__ import annotations

from .protocol import Pose

FIST_HOLD_SECONDS = 0.6

INSTANT = {
    Pose.DOUBLE_TAP: "double_tap",
    Pose.WAVE_IN: "wave_in",
    Pose.WAVE_OUT: "wave_out",
    Pose.FINGERS_SPREAD: "fingers_spread",
}


class GestureTracker:
    def __init__(self, fist_hold_seconds: float = FIST_HOLD_SECONDS):
        self.fist_hold_seconds = fist_hold_seconds
        self._fist_since: float | None = None
        self._fist_active = False

    def on_pose(self, pose: Pose, now: float) -> list[str]:
        """A new pose arrived. Returns the gestures to emit, in order."""
        out: list[str] = []
        if pose != Pose.FIST:
            if self._fist_active:
                out.append("fist_hold_end")
            self._fist_since = None
            self._fist_active = False
        if pose == Pose.FIST and self._fist_since is None:
            self._fist_since = now
        elif pose in INSTANT:
            out.append(INSTANT[pose])
        return out

    def on_tick(self, now: float) -> list[str]:
        """Called a few times a second; starts the fist hold once it is long enough."""
        if self._fist_since is not None and not self._fist_active:
            if now - self._fist_since >= self.fist_hold_seconds:
                self._fist_active = True
                return ["fist_hold_start"]
        return []

    def reset(self) -> list[str]:
        """The band lost sync or disconnected: close an open fist hold."""
        out = ["fist_hold_end"] if self._fist_active else []
        self._fist_since = None
        self._fist_active = False
        return out

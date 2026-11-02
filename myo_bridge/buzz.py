"""myo-buzz: ask the running myo-bridge to vibrate the band.

    myo-buzz [short|medium|long|double|waiting|status]

Exits 0 even when the bridge or the band is absent, so hooks can call it blindly;
use --strict to get exit 1 instead.
"""
from __future__ import annotations

import socket
import sys

from .bridge import SOCKET_PATH


def send(line: str, timeout: float = 3.0) -> str:
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        s.connect(str(SOCKET_PATH))
        s.sendall((line + "\n").encode())
        return s.makefile().readline().strip()


def main() -> None:
    args = [a for a in sys.argv[1:] if a != "--strict"]
    strict = "--strict" in sys.argv
    pattern = args[0] if args else "short"
    try:
        reply = send(pattern)
    except OSError as e:
        reply = f"bridge not running ({e.__class__.__name__})"
    print(reply)
    if strict and reply != "ok" and pattern != "status":
        sys.exit(1)


if __name__ == "__main__":
    main()

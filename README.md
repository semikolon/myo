# Myo armbands

Two Thalmic Labs Myo armbands, to be driven from the Mac Mini over Bluetooth LE without the dongle. First goal: wake them, read battery and firmware. Later: arm motion as mouse, muscle signals as clicks. The starting prompt is `~/Desktop/ThalmicLabsMyo.md` (AI-written; its sample code is untested).

## State (2026-11-02)

- Both bands light up while charging, and go dark the instant they are unplugged, although they were fully charged a few days before. No Bluetooth scan has ever seen them.
- Reading from Thalmic's own LED table: a band that is dark right after unplugging has flat or failed cells. Moving it wakes normal sleep, and unplugging ends deep sleep, so neither explains it.
- Replacement cells ordered 2026-10-28 from Teknikdelar (2 x Cameron Sino CS-MYG100RC, 3.7 V 220 mAh, 99 kr each). **Each band holds two cells** (Adafruit teardown; Visconti et al. 2018), so these cover one band.
- Full research: `reports/Myo wake and Bluetooth connection.md`, notes in `research_notes/`.

## Before opening a band

Plug it into the Mac's own USB port. If a drive named "Myo" mounts, the main board is alive and the cells are the fault. If nothing mounts, try another port or cable before cutting anything.

## Running the scan

macOS kills a Bluetooth program started from Claude Code's own shell (its bundled binary declares no Bluetooth use). Run from the Claude app's Terminal panel or Ghostty:

    uv run -q --with bleak python -I myo_probe.py 180

`myo_probe.py` scans in 10 s rounds up to the given seconds, stops at the first Myo, then reads battery %, firmware and serial and buzzes the band once. A band advertises only when unplugged and awake (logo pulsing blue), for about 30 s before it sleeps.

## The bridge (built 2026-11-02, untested on a real band)

`myo-bridge` keeps one Myo connected and links it to the Mac. A LaunchAgent (`com.fredrikbranstrom.myo-bridge`) runs it inside `~/Applications/MyoBridge.app`, so macOS asks for Bluetooth under the name MyoBridge.

- **Gestures in.** The band's own pose classifier → `myo_bridge/gestures.py` (a fist counts after 0.6 s held) → `hammerspoon://myo?gesture=NAME` → `~/.hammerspoon/myo.lua`, where each gesture's action lives: double tap starts a Ruby conversation, a held fist toggles SuperWhisper recording, spread fingers play/pause, waves skip back/forward. The band buzzes briefly on a double tap and a fist start.
- **Buzzes out.** `.venv/bin/myo-buzz short|medium|long|double|waiting|status` talks to `/tmp/myo-bridge.sock`. A `Notification` hook in `~/.claude/settings.json` sends `waiting` when a Claude session asks permission or sits idle at its prompt; it does nothing when no band is connected.
- **State.** `~/.local/state/myo-bridge/`: `status.json`, `bridge.log`, and `battery.jsonl` (battery every 5 min, the raw data for the battery-health test).
- **After putting the band on**, make the sync gesture (wave out) once; gestures arrive only after that.
- **Rebuild and reload**: `bash scripts/install_agent.sh`. Stop: `launchctl bootout gui/$(id -u)/com.fredrikbranstrom.myo-bridge`. Tests: `uv run --extra test pytest` (22, against a simulated band).

Verified without a band: protocol bytes against OSA-MYO-Controller, gesture logic, the buzz socket, Hammerspoon receiving gestures, the app running under launchd with Bluetooth attributed to MyoBridge. Not yet verified: anything on a real band, and the `superwhisper://record` link (read from the app's binary, never fired).

## Next steps

1. When the cells arrive: the "Myo" drive check above, then replace both cells in one band and run the scan.
2. If that band comes back: decide on two more cells for the second band.
3. Then: battery drain test, library choice (OSA MYO Controller or pymyo, see the report).

## What to use them for (proposed 2026-11-02, not yet ruled on)

Most value for the least work, even with one band: a silent two-way link with the setup he already runs.

- **Gestures in.** The band's own pose classifier (rest, fist, wave in, wave out, fingers spread, double tap) streams over BLE when `set_mode` enables it, so no training or ML. It needs the sync gesture each time the band is put on. Double tap → start Ruby (what Ctrl+§ does; the "Hey Ruby" wakeword refuses his voice since 2026-07), held fist → dictation, waves → pause or skip what is playing.
- **Buzz out.** The vibration motor as a quiet signal: a Claude session waiting for him, an urgent notification while on a call or at night.
- **Ranked lower.** Arm-as-mouse (the starting prompt's idea): arm fatigue and IMU drift. Workout rep and muscle tracking: fun, EMG is coarse (8-bit, 200 Hz), likely little daily use.
- **To run in the background** the bridge needs its own app bundle declaring Bluetooth use; macOS kills a Bluetooth process started from a shell that lacks it.

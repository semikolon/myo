# Myo armband power states, wake behaviour and LED meanings

Research date: 2026-11-02. Primary sources are Thalmic Labs' own support articles (support.getmyo.com, a Zendesk help centre), read as Wayback Machine snapshots dated 2016-08-01 to 2019-07-19 (the snapshot timestamp is in each URL), and Thalmic's Bluetooth protocol header `myohw.h` (github.com/thalmiclabs/myo-bluetooth; protocol commits March to September 2015, relicensed under Google LLC in September 2020). Community sources are marked as such.

Note on access: WebFetch refuses web.archive.org, so the archived articles were fetched with `curl` from `https://web.archive.org/web/<timestamp>id_/<url>` and the text extracted locally. The list of archived article URLs came from the Wayback CDX API.

## What sleep states exist, and what enters each?

### Takeaway
Thalmic documents three low-power states: a normal idle sleep (entered automatically after a short idle period when the armband is not synced), "turned off", which is really the protocol's deep sleep (entered only on command, from Myo Connect's "Turn Myo Off" button or the raw `deep_sleep` BLE command), and an empty battery. Thalmic documents no separate factory shipping mode; the "turned off" state fills that role ("to prepare it for travel or an extended sleep").

### Cited Findings
- Normal sleep: "The Myo armband automatically enters a battery-saving sleep mode when it is idle for a short period of time. It will exit sleep mode when you pick it up." — [How do I turn off the Myo armband? (Thalmic support, article dated 2016-02-25, snapshot 2016-08-01)](https://web.archive.org/web/20160801023928/https://support.getmyo.com/hc/en-us/articles/204167679-How-do-I-turn-off-the-Myo-armband-)
- Sleep is suppressed while synced: "Myo is not connected by Bluetooth and the Sync Gesture has been performed. Myo will not enter sleep mode while synced." And for the unsynced case: "Myo will enter sleep mode after a short period of time." — [LED status descriptions (Thalmic support, snapshot 2016-09-09)](https://web.archive.org/web/20160909133119/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- Protocol sleep modes: `myohw_sleep_mode_normal = 0` "Normal sleep mode; Myo will sleep after a period of inactivity." and `myohw_sleep_mode_never_sleep = 1` "Never go to sleep.", set with `myohw_command_set_sleep_mode = 0x09` (payload size 1). — [myohw.h (Thalmic, 2015)](https://github.com/thalmiclabs/myo-bluetooth/blob/master/myohw.h)
- Deep sleep command: `myohw_command_deep_sleep = 0x04` "Put Myo into deep sleep", payload size 0. The header says nothing about how the device wakes from it. — [myohw.h](https://github.com/thalmiclabs/myo-bluetooth/blob/master/myohw.h)
- "Turn off" in Myo Connect: the Armband Manager's "Turn Myo Off - Turn Myo off completely to prepare it for travel or an extended sleep." — [Using the Armband Manager in Myo Connect (Thalmic support, snapshot 2017-11-08)](https://web.archive.org/web/20171108204254/https://support.getmyo.com/hc/en-us/articles/205031939-Using-the-Armband-Manager-in-Myo-Connect)
- Community: the pyomyo `power_off()` docstring says "according to the official BLE specification, the 0x04 command puts the Myo into deep sleep, there is no way to completely turn the device off", and that without it "you have to wait until the Myo battery is fully discharged, or use the official Myo app for Windows or Mac and turn off the device from there." — [pyomyo source, community library (author Alvaro Villoslada)](https://github.com/PerlinWarp/pyomyo/blob/main/src/pyomyo/pyomyo.py)
- Community: MioConnect's README says that after `deep_sleep` "the armband will go into a state with basically everything off and can stay in that state for months", attributing this to Thalmic's release notes (which I could not find). — [MioConnect README (community)](https://github.com/francocruces/MioConnect)
- No physical power button exists. — [Pocket Insider review, 2015](https://pocketinsider.com/2015/09/16/review-myo-armband/) (via search summary)

### Inferences
- "Turned off" in Thalmic's consumer docs and `deep_sleep` in the protocol are the same state (the pyomyo docstring equates them, and both are left only by USB; see next section). This is consistent across sources but not stated in one Thalmic sentence.
- A Myo that someone turned off in Myo Connect years ago (plausible if they were put away for travel or storage) would sit in deep sleep and would not respond to shaking.

### Gaps
- No Thalmic statement on the exact idle timeout before normal sleep ("a short period of time" only).
- No source on whether low battery forces a sleep or deep sleep before reaching 0 %.
- Thalmic's firmware release notes that introduced deep sleep were not found in the archive.

## What wakes the Myo from each state?

### Takeaway
Normal sleep is left by motion ("when you pick it up"). Deep sleep / "turned off" and an empty battery are left only by connecting USB power; Thalmic's own reset procedure is "connect it via micro USB, then disconnect it". Nothing indicates skin or EMG contact is needed to wake it.

### Cited Findings
- Normal sleep: "It will exit sleep mode when you pick it up." — [How do I turn off the Myo armband?](https://web.archive.org/web/20160801023928/https://support.getmyo.com/hc/en-us/articles/204167679-How-do-I-turn-off-the-Myo-armband-)
- Turned off: "In order to turn Myo back on, you must connect it to your computer or a wall charger through the micro USB cable." — same article.
- Both LEDs off has three meanings per Thalmic: "1) Myo is in sleep mode. Move Myo to wake it. 2) Myo is turned off. Connect to a power source via USB to turn on. 3) The battery in Myo is at 0%. Connect to a power source via USB to charge." — [LED status descriptions](https://web.archive.org/web/20160909133119/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- Reset: "You can reset your Myo armband by connecting it to your computer using a micro USB cable (like the one provided with your Myo armband) then disconnecting it." — [How to reset the Myo armband (Thalmic support, snapshot 2019-07-19)](https://web.archive.org/web/20190719060714/https://support.getmyo.com/hc/en-us/articles/201769279-How-to-reset-the-Myo-armband)
- The armband is deliberately inert while plugged in: "The Myo armband is not intended to be worn while plugged in ... and is specifically designed to be non-operational while plugged in." — [How do I charge the Myo armband? (Thalmic support, snapshot 2016-08-01)](https://web.archive.org/web/20160801023714/https://support.getmyo.com/hc/en-us/articles/202649593-How-do-I-charge-the-Myo-armband-)
- Boot can fail around a USB plug/unplug: "In some cases the Myo armband may fail to boot after connecting or disconnecting from a computer via USB or a firmware update may not finish successfully leaving the Myo in an unresponsive state." — [Unresponsive / won't turn on / solid orange LED (Thalmic support, snapshot 2016-08-01)](https://web.archive.org/web/20160801023636/https://support.getmyo.com/hc/en-us/articles/202198919-My-Myo-armband-is-unresponsive-won-t-turn-on-or-displays-a-solid-orange-LED)
- Community: MioConnect says the only way to turn the armband back on after deep sleep is plugging it in over USB, "as MyoConnect would". — [MioConnect README](https://github.com/francocruces/MioConnect)
- Community review: after a period without gestures, a double tap (middle finger and thumb) is needed to wake it. — [search summary of a review; source not opened, treat as weak](https://www.techguide.com.au/amp/reviews/myo-armband-review-control-your-devices-and-apps-wirelessly-with-gestures/). This most likely describes the gesture *unlock* (`myohw_command_unlock`, timed re-lock), not power sleep.

### Inferences
- Because the Myo is "non-operational while plugged in", it should not be expected to advertise over Bluetooth while on the charger. The test that matters is what happens in the seconds after unplugging: per the reset article, unplugging is itself the boot/reset event.
- After unplugging, an unsynced, unconnected Myo should show the logo LED pulsing blue with the status LED off (the advertising/idle state, see LED section) and then fall into normal sleep "after a short period of time". A 5-minute BLE scan started some time after unplugging could miss it entirely; moving or shaking it during the scan (or unplugging it just before the scan starts) is needed to keep it awake. Unconfirmed by a Thalmic source, which never states that the device advertises only while awake, though that is the expected design.
- If no LED lights at all in the first seconds after unplugging, the likely causes are (a) a battery that cannot carry the load (see battery section), or (b) a failed boot after USB disconnect, for which Thalmic's remedy is reflashing firmware via the "Myo" USB drive.
- Wake from normal sleep needs only motion (the IMU), not skin or EMG contact: Thalmic says "pick it up" / "Move Myo". Wearing it matters only for the sync gesture, which in turn stops it from sleeping.

### Gaps
- No Thalmic statement on whether motion alone can ever wake a Myo from deep sleep (all sources say USB only).
- Whether the Myo advertises during normal sleep at a slow interval is not documented anywhere I found.

## What do the LEDs mean?

### Takeaway
There are two LEDs: the Thalmic logo LED (on the main pod) and the status LED (a bar). Thalmic's own table, quoted in full below, covers charging, low battery, connection/sync, warm-up and firmware states.

### Cited Findings
All rows verbatim from [LED status descriptions (Thalmic support, snapshot 2016-09-09)](https://web.archive.org/web/20160909133119/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-):

| Logo LED | Status LED | Meaning |
|---|---|---|
| Off | Pulse orange | Connected to a power source and charging |
| Off | Constant green | Connected to a power source and fully charged |
| Constant blue | Flash orange | Low battery, in use or idle |
| Off | Off | Battery at 0 %; or asleep (move it); or turned off (USB to turn on) |
| Constant blue | Constant blue | Connected by Bluetooth, sync gesture performed |
| Pulse blue | Constant blue | Connected by Bluetooth, sync gesture not performed |
| Constant blue | Off | Not connected by Bluetooth, synced; will not sleep while synced |
| Pulse blue | Off | Not connected by Bluetooth, not synced; will sleep after a short period |
| Flash blue | Constant blue | Warming up; vibrates when warm-up is over |
| Off | Pulse purple | Completing a firmware update |
| Off | Flash red | An error has occurred; reload the firmware |
| Off | Constant red | An error has occurred; contact support |

- After a firmware reload: "The status LED on the Myo will pulse a pale purple colour for a few moments while the firmware update is applied. The Thalmic Labs logo will glow blue when the operation is complete." — [Status LED flashing red (Thalmic support, snapshot 2016-08-01)](https://web.archive.org/web/20160801024347/https://support.getmyo.com/hc/en-us/articles/202419849-The-status-LED-on-the-Myo-armband-is-flashing-red)
- A solid orange LED is listed in an article title as a symptom of an unresponsive Myo needing firmware reload. — [Unresponsive / solid orange LED](https://web.archive.org/web/20160801023636/https://support.getmyo.com/hc/en-us/articles/202198919-My-Myo-armband-is-unresponsive-won-t-turn-on-or-displays-a-solid-orange-LED)
- In the Getting Started flow: "The logo LED should be pulsing blue and the status LED off ... If you see the status LED blue, that means Myo is already connected to another computer or mobile device ... If you see the status LED flashing red or both LEDs off, you will need to manually reload the firmware." — [Myo not connecting via Bluetooth during Getting Started Guide (Thalmic support, snapshot 2017-07-04)](https://web.archive.org/web/20170704034009/https://support.getmyo.com/hc/en-us/articles/210708483-Myo-not-connecting-via-Bluetooth-during-Getting-Started-Guide)
- Community: LED colours can be set over BLE with an undocumented command 6 (`write_attr(0x19, pack('8B', 6, 6, *(logo + line)))`, RGB for logo then bar). It is absent from the public `myohw.h`. — [pyomyo source](https://github.com/PerlinWarp/pyomyo/blob/main/src/pyomyo/pyomyo.py)

### Inferences
- "Logo pulsing blue, status off" is the state to look for when expecting the Myo to be discoverable: awake, not connected, not synced.
- "Status LED constant blue" while the Mac sees nothing means it is connected to some other host (an old phone, a BLED112 dongle on another computer) and will not be advertising.
- There is no dedicated bootloader LED in Thalmic's table; in bootloader/USB-drive mode the device is on USB, so it shows the charging colours, and a mounted "Myo" drive is the sign of that mode.

### Gaps
- No Thalmic source describes a dedicated "advertising" blink pattern distinct from the "pulse blue logo" row.

## Charging behaviour

### Takeaway
Thalmic: any standard micro-USB charger works; status LED pulses orange while charging and turns solid green when full; typical charge time 2 to 3 hours; the device is non-operational on USB. Nothing official addresses reviving a cell left empty for years.

### Cited Findings
- "You can also use any standard Micro USB charger ... The Myo armband's LED will pulse orange when charging and then change to solid green when fully charged. The typical charging time is 2-3 hours." — [How do I charge the Myo armband?](https://web.archive.org/web/20160801023714/https://support.getmyo.com/hc/en-us/articles/202649593-How-do-I-charge-the-Myo-armband-)
- Connected to a computer, the Myo mounts as a removable drive named "Myo" (used for firmware reflash; drop the HEX file, a SUCCESS.txt appears, then unplug). — [Manually update the firmware (Thalmic support, snapshot 2016-09-09)](https://web.archive.org/web/20160909214528/https://support.getmyo.com/hc/en-us/articles/201763319-How-do-I-manually-update-the-firmware-on-my-Myo-armband-)
- If the drive does not mount, Thalmic's "full reset" is to let the battery drain completely ("can take 2 - 3 days"; "You'll know it has drained if the LEDs do not light up when you move the armband"), then reconnect. — [Myo armband not recognized through USB (Thalmic support, snapshot 2016-08-01)](https://web.archive.org/web/20160801023732/https://support.getmyo.com/hc/en-us/articles/206475205-Myo-armband-not-recognized-through-USB)
- If no LEDs light when plugged in: try another cable, another port, a wall charger, another computer. — [Myo armband is not charging or turning on (Thalmic support, snapshot 2019-07-17)](https://web.archive.org/web/20190717172200/https://support.getmyo.com/hc/en-us/articles/208807646-Myo-armband-is-not-charging-or-turning-on)
- Firmware downloads were hosted from a support article "Myo Connect, SDK and firmware downloads" (archived 2019-07-17). — [CDX listing entry](https://web.archive.org/web/20190717172846/https://support.getmyo.com/hc/en-us/articles/360018409792-Myo-Connect-SDK-and-firmware-downloads) (not opened)

### Inferences
- Both of the user's armbands lighting on a 5 V 1 A charger shows the charge path and the MCU still work. Whether the light is pulsing orange (charging) or solid green (full) matters: solid green within minutes of plugging in a long-unused unit would suggest a cell that reports full but has lost most of its capacity.
- A Li-ion/Li-po cell stored empty for years may have been held in protection cut-off; the charger IC normally pre-charges such a cell slowly. Giving each armband a long, uninterrupted charge (several hours, well past the official 2 to 3 h, until solid green) before testing unplugged behaviour is the cheap first step. General Li-ion knowledge, not a Myo-specific source.

### Gaps
- No source on the Myo's charger IC, pre-charge behaviour or the cut-off voltage of its protection circuit.
- No community report found of reviving a Myo after years of storage (searches for Reddit threads returned nothing relevant).

## Does the Myo need to be worn to stay awake?

### Takeaway
No. Wake and stay-awake are motion-based; being worn matters only for the sync gesture, and a synced Myo never sleeps. Software can also disable sleep entirely with `never_sleep`.

### Cited Findings
- Exits sleep "when you pick it up"; "Move Myo to wake it." — [turn-off article](https://web.archive.org/web/20160801023928/https://support.getmyo.com/hc/en-us/articles/204167679-How-do-I-turn-off-the-Myo-armband-), [LED table](https://web.archive.org/web/20160909133119/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- "Myo will not enter sleep mode while synced." — [LED table](https://web.archive.org/web/20160909133119/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- `myohw_sleep_mode_never_sleep = 1` via command `0x09`; community libraries send it right after connecting (pyomyo: `write_attr(0x19, b'\x09\x01\x01')`; MioConnect's connect sequence includes "Disable sleep"). — [myohw.h](https://github.com/thalmiclabs/myo-bluetooth/blob/master/myohw.h), [pyomyo](https://github.com/PerlinWarp/pyomyo/blob/main/src/pyomyo/pyomyo.py), [MioConnect](https://github.com/francocruces/MioConnect)

### Inferences
- For a bench test on the desk, keeping the armband moving (or in hand) until a connection is made and `never_sleep` is written is enough; it does not need to be on an arm.

### Gaps
- Whether `never_sleep` persists across disconnects or reboots is undocumented.

## Battery life and signs of a worn-out battery

### Takeaway
Thalmic: a day of continued use, up to about a week in standby when not connected. The hardware holds two small cells (Adafruit teardown). Capacity figures exist only from replacement-part sellers and conflict.

### Cited Findings
- "The Myo armband has a rechargeable lithium-ion battery and is designed to last a day of continued use. When not connected to a device and in standby mode, the battery is expected to last up to a week." — [Battery life of the Myo armband (Thalmic support, snapshot 2019-07-17)](https://web.archive.org/web/20190717173148/https://support.getmyo.com/hc/en-us/articles/202641403-Battery-life-of-the-Myo-armband)
- Teardown: "there are two batteries tucked in different cubbies"; main board carries an nRF51822 BLE transceiver/processor and a Freescale Kinetis MK22FN1M0 (Cortex-M4, 120 MHz). No capacity given; no date or author on the page (image timestamps early 2016). — [Adafruit, Myo armband teardown](https://learn.adafruit.com/myo-armband-teardown)
- Replacement-cell listings: 3.7 V Li-polymer, part numbers 144440100156 / 571830, listed as 300 mAh by one seller and 220 mAh / 0.81 Wh by another; unverified seller data. — [search summary of seller listings, e.g. batteryclerk](https://www.batteryclerk.com/collections/remote-control-batteries/brand_myo)
- Thalmic discontinued the Myo to build a different product. — [Engadget, Thalmic tag page](https://www.engadget.com/tag/Thalmic)

### Inferences
- "Lights while plugged in, dark the moment it is unplugged, even with motion" is the classic sign of a cell that cannot supply the boot current (high internal resistance or capacity near zero). Thalmic's docs do not name this symptom, but their "both LEDs off" row would show exactly this.
- With two cells, one failed cell could produce the same symptom. Replacement cells appear to be sold, so a rebuild is possible if the cells are dead.

### Gaps
- No Thalmic statement on battery cycle life or degradation.
- No measured capacity from a teardown.

## Bluetooth discovery notes relevant to the Mac scan

### Takeaway
The Myo's control service UUID is `d5060001-a904-deb9-4748-2c7f4a124842`; community bleak-based tooling scans for it. Thalmic officially required its own BLED112 dongle for Myo Connect, but the published protocol permits any BLE adapter.

### Cited Findings
- Service UUID construction: "the full service UUID for GCControlService would be d5060001-a904-deb9-4748-2c7f4a124842"; `MYO_SERVICE_INFO_UUID` bytes encode the same. — [myohw.h](https://github.com/thalmiclabs/myo-bluetooth/blob/master/myohw.h)
- Thalmic: "the Myo armband requires the included Bluetooth adapter" for Myo Connect, but "Developers can create their own Bluetooth connection implementation to connect to built-in Bluetooth adapters using the Bluetooth Protocol." — [Can I use my computer's built-in Bluetooth? (Thalmic support, snapshot 2019-07-17)](https://web.archive.org/web/20190717164800/https://support.getmyo.com/hc/en-us/articles/203996655-Can-I-use-my-computers-built-in-Bluetooth-)
- Pairing in Myo Connect was done by tapping the logo to the USB adapter. — [Pair and connect a new Myo Armband (Thalmic support, snapshot 2019-07-17)](https://web.archive.org/web/20190717171738/https://support.getmyo.com/hc/en-us/articles/208807366-Pair-and-connect-a-new-Myo-Armband-in-Myo-Connect)
- bleak on macOS: `service_uuids` limits results to advertisements containing that UUID and was required on macOS 12.0 to 12.3; CoreBluetooth hides MAC addresses; passive scanning is unsupported on macOS. — [bleak BleakScanner docs](https://bleak.readthedocs.io/en/stable/api/scanner.html)
- Community: dl-myo is a bleak-based Myo library listing macOS support, which states any Myo should carry the service UUID d5060001-.... — [dl-myo on PyPI (search summary; page did not render)](https://pypi.org/project/dl-myo/0.1.2)

### Inferences
- A scan that saw "no Myo at all" is consistent with the armband never being awake during the scan (deep sleep, normal sleep after the unplug wake-up, or a battery that dies on unplug), more than with a scanning problem. Still, matching on the advertised name or service UUID rather than on a remembered address is required on macOS.
- Suggested test order from these sources: charge to solid green; unplug while the scan is already running; watch the LEDs in the first seconds (logo pulsing blue = awake and should be advertising; nothing = battery or boot failure); keep the armband moving throughout; if it lights then goes dark at once on unplug, suspect the cells; if status LED flashes red, reflash firmware via the "Myo" USB drive.

### Gaps
- Whether the Myo's advertisement contains the 128-bit service UUID in the primary packet or only in the scan response was not found; on macOS, bleak's active scanning would collect both.
- No source confirms a current macOS + bleak connection to a Myo working end to end.

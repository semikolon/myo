# Reviving discontinued Thalmic Myo armbands: failure modes, fixes and field reports

Scope: two Myos unused for years. Plugged into USB they light up; unplugged and shaken they show no light, and a BLE scan from a Mac finds no Myo.

Source note: the most authoritative material turned out to be Thalmic's own support knowledge base (support.getmyo.com, Zendesk), now offline but preserved on the Wayback Machine. The article bodies below were retrieved from Wayback snapshots from 2019 (the "unresponsive" article snapshot is dated 2019-11-19; the others were fetched with a 2019 snapshot request). Wayback URLs are given as `https://web.archive.org/web/2019/<original URL>`. Community field reports from 2020-2026 are thin; Reddit threads did not surface in any search (see Gaps).

---

## Q1. "Won't turn on / won't wake / not detected / only works while plugged in": reported causes and fixes

### Takeaway
Thalmic documented four distinct states that all look like "dark when unplugged": normal sleep (move it to wake), "turned off" deep sleep (USB plug/unplug wakes it), battery at 0 % (charge it), and a firmware fault after a failed boot or update (reflash by copying a .hex to the "Myo" USB drive, after fully draining the battery if the drive does not mount). Critically, the Myo is designed to do nothing over Bluetooth while plugged in, so "lights only while plugged in" is the normal charging indication, not evidence that it works.

### Cited Findings
- Official LED table: logo LED off + status LED off means one of three things: "1) Myo is in sleep mode. Move Myo to wake it. 2) Myo is turned off. Connect to a power source via USB to turn on. 3) The battery in Myo is at 0%. Connect to a power source via USB to charge." — [Thalmic support: LED status descriptions (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- Same table, the states visible while plugged in: logo off + status pulse orange = charging; logo off + status constant green = fully charged. Unplugged and awake but not connected: logo pulses blue, status off ("Myo will enter sleep mode after a short period of time"). Low battery: logo constant blue + status flashing orange. — [Thalmic support: LED status descriptions](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- Same table, firmware states: status pulse purple = completing firmware update; status flashing red = "An error has occurred on Myo. Reload the firmware."; status constant red = "An error has occurred on Myo. Contact support" (no user fix documented). — [Thalmic support: LED status descriptions](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202724369-What-are-the-different-LED-status-descriptions-for-the-Myo-armband-)
- "The Myo armband is not intended to be worn while plugged in ... and is specifically designed to be non-operational while plugged in." Charging LED pulses orange, then solid green; typical charge time 2-3 hours. — [Thalmic support: How do I charge the Myo armband? (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202649593-How-do-I-charge-the-Myo-armband-)
- Official "unresponsive / won't turn on / solid orange LED" procedure: "In some cases the Myo armband may fail to boot after connecting or disconnecting from a computer via USB or a firmware update may not finish successfully leaving the Myo in an unresponsive state." Steps: connect by USB; if the removable "Myo" drive mounts, copy the firmware HEX file to it and disconnect (LED pulses pale purple while completing). If the drive does not mount: disconnect, "Wait for the battery in the Myo to drain completely", reconnect; the "Myo" drive will mount; "If you do not see the Myo drive the battery may not be completely drained. Disconnect and wait longer. If the battery has drained, try connecting to another USB port, an external USB hub or another computer." Then reload firmware. — [Thalmic support: My Myo armband is unresponsive, won't turn on, or displays a solid orange LED (Wayback 2019-11-19)](https://web.archive.org/web/20191119111921/https://support.getmyo.com/hc/en-us/articles/202198919-My-Myo-armband-is-unresponsive-won-t-turn-on-or-displays-a-solid-orange-LED)
- "Not charging or turning on" (no LED activity at all when plugged): try another cable (it may be damaged or "losing data"), every USB port, avoid powered external hubs and use a port on the computer, try a USB wall charger, try another computer. — [Thalmic support: Myo armband is not charging or turning on (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/208807646-Myo-armband-is-not-charging-or-turning-on)
- Flashing red status LED: reload firmware via the "Myo" drive; if it still flashes red, try another standard micro-USB cable, another USB port "(preferably on another USB host controller)", another computer. — [Thalmic support: The status LED is flashing red (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202419849-The-status-LED-on-the-Myo-armband-is-flashing-red)
- Batteries in a unit stored for years: an aggregator buying guide claims LiPo cells "degrade after 5–6 years; swelling or failure common in units stored >3 years". This is unsourced aggregator content and should be treated as a plausible generic claim, not a measured Myo statistic. — [Alibaba electronics guide (2026)](https://electronics.alibaba.com/question/myo-armband-still-available-uses,-price-alternatives)
- Academic note (2025): "The Myo has been discontinued, and remaining devices have gradually become nonfunctional." (no failure mode given) — [von Arnim et al., "A Sensor is not a Sensor" (2025)](https://doi.org/10.1145/3771594.3771626)
- Single anecdote (Japanese blog, 2014): a user plugged in, accepted a firmware update, and "the charging lamp stopped lighting"; the author advises never to update firmware while the LED is slowly blinking orange (charging) and to update with the band lying still on a flat surface. — [dvorak.hatenablog.com (2014-12-15)](https://dvorak.hatenablog.com/entry/2014/12/15/152831)

### Inferences
- The described symptom (lights when plugged, nothing when unplugged and shaken, no BLE advertisement) matches the "battery at 0 % / cell no longer holds charge" branch best: a Myo merely in sleep or deep sleep would wake after a plug/unplug (the documented reboot) and its logo LED would pulse blue for a while after unplugging. A firmware fault would more likely show flashing red. This is inference from the LED table, not a field report.
- The LED colour while plugged in is the cheapest discriminator: pulsing orange for hours that never turns green suggests the charger never sees the cell reach full (failed or disconnected cell); green within minutes followed by darkness on unplug suggests a cell with almost no capacity left; flashing red means firmware.
- Whether the "Myo" mass-storage drive mounts on the Mac while plugged in is a second free diagnostic: it proves the main MCU (Kinetis) boots on USB power regardless of battery state.

### Gaps
- No 2020-2026 first-hand report was found of the exact pattern "lights on USB, dead off USB" with a confirmed root cause.
- No source states how long a Myo stays in "turned off" deep sleep before the battery is flat, beyond the protocol note that it "can stay in that state for months" (see Q2).

---

## Q2. How do you wake a Myo from sleep or deep sleep ("shipping mode")? Is plugging in USB enough?

### Takeaway
Two sleep levels exist. Normal sleep is ended by moving the band. Deep sleep ("turned off", also what a new boxed unit ships in by implication) is ended only by connecting USB power; Thalmic's own reboot is "plug it in, then unplug it", with no minimum time stated. There is no separate "shipping mode" in Thalmic's documentation beyond this deep sleep.

### Cited Findings
- "The Myo armband automatically enters a battery-saving sleep mode when it is idle for a short period of time. It will exit sleep mode when you pick it up. You can also turn Myo off completely by using the Turn Off button in the Armband Manager ... In order to turn Myo back on, you must connect it to your computer or a wall charger through the micro USB cable." — [Thalmic support: How do I turn off the Myo armband? (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/204167679-How-do-I-turn-off-the-Myo-armband-)
- Reset: "You can reset your Myo armband by connecting it to your computer using a micro USB cable ... then disconnecting it." — [Thalmic support: How to reset the Myo armband (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/201769279-How-to-reset-the-Myo-armband)
- Thalmic UX designer (2014): "Myo also has a full reboot. Just plug it in to your computer, then unplug it." — [Thalmic Labs on Medium, "Tips and tricks for the Myo armband" (2014-12-30)](https://medium.com/thalmic/thalmic-labs-user-experience-designer-shares-tips-and-tricks-for-myo-ce8d9c4f7960)
- BLE protocol: command 0x04 `myohw_command_deep_sleep` "Put Myo into deep sleep"; sleep modes `normal` (sleeps after inactivity) and `never_sleep` (command 0x09). — [thalmiclabs/myo-bluetooth myohw.h](https://github.com/thalmiclabs/myo-bluetooth/blob/master/myohw.h)
- MioConnect README: "according to the release notes, the armband will go into a state with basically everything off and can stay in that state for months. The only way to turn it back on is plugging it via USB". — [francocruces/MioConnect](https://github.com/francocruces/MioConnect)
- Alvipe (2017): "according to the official BLE specification, the 0x04 command puts the Myo into deep sleep, there is no way to completely turn the device off". — [dzhu/myo-raw PR #23](https://github.com/dzhu/myo-raw/pull/23)
- Normal sleep timing: an SDK user reported the band "will undergo sleep mode after approximately 30 seconds if no activity detected" when not synced (2016). — [myo-python issue #36](https://github.com/NiklasRosenstein/myo-python/issues/36); the al42and dongleless project also notes letting it "go to sleep by placing it on a flat surface for ~30 seconds". — [al42and/myo-sleep mirror](https://safaia.net/al42and/myo-sleep)
- Battery life: about one day of continuous use; "When not connected to a device and in standby mode, the battery is expected to last up to a week." — [Thalmic support: Battery life (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/202641403-Battery-life-of-the-Myo-armband)
- Reviewers confirm no power button; USB connection is the only way to power on after it is turned off. — [Pocket Insider review (2015)](https://pocketinsider.com/2015/09/16/review-myo-armband/); [Beebom review (2016)](https://beebom.com/myo-gesture-control-armband-review/)
- Myo Alpha (pre-production) had a pinhole reset button; production units do not mention one. — [FCC filing "Getting To Know Myo" (FCC ID 2ACKVTL9B)](https://fcc.report/FCC-ID/2ACKVTL9B/2323425.pdf)

### Inferences
- A unit that sat in deep sleep or plain sleep for years has almost certainly self-discharged its cells to 0 % (standby lasts "up to a week"; deep sleep "months"), so after years the realistic state is "battery at 0 %" plus possibly over-discharged cells. A plug/unplug alone will not help until the cells take a charge.
- Waking procedure to try: charge until the status LED turns solid green (2-3 h nominal), unplug, and watch for the logo LED to pulse blue within seconds; move it. If it pulses blue, it is advertising and should appear in a scan for roughly the ~30 s before it sleeps again; keep moving it during the scan.

### Gaps
- No source gives a minimum plug-in duration for the USB wake; Thalmic's wording implies it is instantaneous (plug in, unplug).

---

## Q3. Long trickle charge to recover an over-discharged battery: durations and outcomes

### Takeaway
No Myo-specific field report of a long trickle-charge recovery was found. Thalmic's only "drain" guidance runs the other way: deliberately draining the battery to zero to force a clean boot into the USB drive/bootloader.

### Cited Findings
- Thalmic tells users to "Wait for the battery in the Myo to drain completely" so that the "Myo" drive will mount on reconnect, and to "wait longer" if it does not. — [Thalmic support: unresponsive / won't turn on (Wayback 2019-11-19)](https://web.archive.org/web/20191119111921/https://support.getmyo.com/hc/en-us/articles/202198919-My-Myo-armband-is-unresponsive-won-t-turn-on-or-displays-a-solid-orange-LED)
- Single anecdote (FreeMyo.py README, 2022): a macOS user could not connect until the battery was nearly drained: "when the battery got down to 2 or 3%, I was able to connect and didn't have any issues after that", speculating that the band drops stored pairing information when drained. — [jshahbazi/FreeMyo.py](https://github.com/jshahbazi/FreeMyo.py)
- Generic analogue (not Myo): a SparkFun forum answer on a MyoWare wireless shield (different product) suggests a weak on-board charger may need "a day or more" to fill a larger cell. — [SparkFun community](https://community.sparkfun.com/t/myoware-2-0-wireless-shield-battery/47487)

### Inferences
- Myo's charger runs at roughly 200-500 mA scale (2-3 h for about 440-520 mAh total), and many LiPo charge ICs pre-condition a deeply discharged cell at a low current before fast charging. Leaving the band on USB for several hours (well past the nominal 2-3 h) is a low-cost first attempt; if the status LED goes green quickly yet the band is dark the moment it is unplugged, the cells are probably not holding charge and need replacing. This is an inference, not a reported outcome.
- A cell over-discharged for years can be unsafe to recharge; check the pods for swelling (gaps between pod halves, bulging) before charging for long periods.

### Gaps
- No report found of anyone recovering a years-dead Myo by extended charging, nor of the opposite outcome. Reddit, which would be the likeliest home for such reports, did not surface in searches.

---

## Q4. Battery replacement: cell type, size, connector, teardown, difficulty

### Takeaway
The Myo holds two LiPo cells in two separate pods. Academic teardowns list them as 3.7 V 260 mAh each; aftermarket replacements sold as Myo part 571830 / 144440100156 are 3.7 V 220 mAh, 32 x 17 x 6 mm. Opening requires cutting through the rubber gasket that joins the pods. ⚠ *(Probably not; see the 2026-11-03 note at the end of this section.)* No step-by-step replacement guide or hands-on replacement report was found (no iFixit guide surfaced).

### Cited Findings
- Adafruit teardown: "Upon clipping through the rubber gasket to unfold the ring, the EMG electrode units were unveiled. Inside each cubby was a small circuit board, and there are two batteries tucked in different cubbies." Main board: Freescale Kinetis MK22FN1M0 Cortex-M4 120 MHz, Nordic nRF51822 BLE under a can, vibration motor; MPU-9150 IMU on the back. — [Adafruit: Myo Armband Teardown](https://learn.adafruit.com/myo-armband-teardown/inside-myo) (video: [YouTube E0GufWmT4mU](https://www.youtube.com/watch?v=E0GufWmT4mU))
- Spec from a 2018 review paper: "2 x lithium battery 3.7 V - 260mAh", "located into two elements of the armband", with photos of a cell "housed behind of one of the eight electrodes". — [Visconti et al., "Technical Features and Functionalities of Myo Armband" (2018)](https://www.researchgate.net/publication/324889539_Technical_Features_and_Functionalities_of_Myo_Armband_An_Overview_on_Related_Literature_and_Advanced_Applications_of_Myoelectric_Armbands_Mainly_Focused_on_Arm_Prostheses); repeated in [DLR master's thesis](https://elib.dlr.de/137442/1/Shreyas_Waichal_Final_Master_Thesis.pdf)
- Aftermarket cell: Cameron Sino CS-MYG100RC, Li-Polymer 3.7 V 220 mAh, 0.81 Wh, 32 x 17 x 6 mm, 6 g, listed as replacing "Myo 144440100156 571830"; about 10-12 EUR, about 45 days delivery. — [Volterino CS-MYG100RC](https://www.volterino.com/CS-MYG100RC.html); also [Techtek.de](https://www.techtek.de/en/device/remote-controls/myo/gesture-control-armband), [Unicell SG](https://www.battery.com.sg/product/myo-144440100156-571830-battery-for-myo-gesture-control-armband), [Mercateo FR](https://www.mercateo.fr/p/6802-31066350/Batterie_3_7V_0_22Ah_LiPo_pour_Myo_Bracelet_controle_gestuel.html)
- Reviews list the battery as "Li-ion Battery, Non Removable". — [Beebom review (2016)](https://beebom.com/myo-gesture-control-armband-review/)
- A 2023 Japanese user found references to a 220 mAh pack and speculated there may be several cells. — [manumaruscript.com (2023-05-09)](https://manumaruscript.com/myo-armband-setup-2023/)

### Inferences
- The two capacity figures (260 vs 220 mAh) conflict; the papers likely read a label, while the 220 mAh figure is a reseller's compatible part. The part code 571830 follows the usual LiPo naming (about 5.7 mm thick, 18 mm wide, 30 mm long), which roughly matches the 32 x 17 x 6 mm listing. Measure the original cells before buying.
- Since a replacement would need two cells per band, and each cell sits behind an electrode in a separate pod, the job involves cutting the gasket, desoldering or unplugging two cells, and resealing; difficulty is moderate to high and the band will not be watertight or as neat afterwards. No source confirms whether the cells use connectors or are soldered. ⚠ *Superseded 2026-11-03: the FCC internal photos show the cells soldered with three wires, and an outer plate removed without cutting; see `research_notes/opening/session_2026-11-03_opening_and_cells.md`.*
- If one cell has failed and the other has not, the two are presumably in parallel; replacing both together is the safe choice (inference).

### Gaps
- No hands-on report of a completed Myo battery replacement was found, nor whether the cells are wired in parallel or series, nor connector type. No iFixit guide exists in search results.

---

## Q5. Bootloader, DFU and firmware recovery without Myo Connect; LED pattern for bootloader mode

### Takeaway
Recovery does not need Myo Connect. The Myo enumerates over USB as a mass-storage drive named "Myo"; copying the firmware .hex onto it reflashes the band, and a SUCCESS.txt appears when it took. The last firmware, 1.5.1970, is mirrored on GitHub. The bootloader belongs to the Kinetis MK22 main MCU (not the nRF51), and Thalmic documents no button or LED pattern for "bootloader mode": the drive simply mounts on USB, and if it does not, a full battery drain is the documented way to force it.

### Cited Findings
- Manual firmware update, "same process for Windows and Mac OS X": connect by USB, "A removable drive will be mounted called 'Myo'"; copy the HEX file to it "(The INFO.TXT file is a hidden file)"; the drive unmounts and remounts after a few seconds; "You should see a SUCCESS.txt file. If you do not, repeat step 3."; disconnect, LED pulses pale purple, then returns to normal. — [Thalmic support: How do I manually update the firmware (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/201763319-How-do-I-manually-update-the-firmware-on-my-Myo-armband-)
- Thalmic's final downloads page lists "Myo Firmware v1.15.1970" (file name myo-firmware-1.5.1970.hex) plus Myo Connect 1.0.1 for Windows and macOS. — [Thalmic support: Myo Connect, SDK and firmware downloads (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/360018409792-Myo-Connect-SDK-and-firmware-downloads)
- The original S3 links (`s3.amazonaws.com/thalmicdownloads/firmware/...hex`) now return HTTP 403 (checked 2026-11-02). The firmware is mirrored as a release asset: `myo-firmware-1.5.1970.hex` (1,009,572 bytes) along with MyoConnect.dmg, the Windows installer and SDKs. — [NiklasRosenstein/myo-python release v1.0.4](https://github.com/NiklasRosenstein/myo-python/releases/tag/v1.0.4); Myo Connect v1.0.1 Windows installer also archived at [andyman1222/MyoConnectSoftware (2023)](https://github.com/andyman1222/MyoConnectSoftware)
- Field report (2025-09, macOS): a user whose band ran firmware 0.8.18 REV-D upgraded to 1.5.1970 by the drag-the-hex method; the maintainer: "upgrading the firmware is really easy"; the user: "Wow, wasn't knowing it was so easy to upgrade the firmware!" After the update `myo.info` worked (reading the GAP name characteristic still failed). — [Crimson-Crow/pymyo issue #5](https://github.com/Crimson-Crow/pymyo/issues/5)
- Old firmware 0.8.18 was posted in a 2014 GitHub thread as an S3 link (now dead); firmware 1.0+ stopped exposing EMG the old way. — [dzhu/myo-raw issue #4](https://github.com/dzhu/myo-raw/issues/4)
- Aggregator mirror pages restate the procedure ("It will mount as a storage device. Drag the .hex file into the mounted Myo drive") for 1.5.1931 and 1.5.1970. — [PCI-DB 1.5.1970](https://pci-db.com/driver/154654/thalmic-labs-myo-armband-firmware-151970); Softpedia is referenced by the pymyo maintainer
- Hardware: two MCUs, the Kinetis MK22 Cortex-M4 and the nRF51822 BLE SoC. — [Adafruit teardown](https://learn.adafruit.com/myo-armband-teardown/inside-myo)
- The BLE header warns that it "omits features that may permanently change the Myo in a not easily-reversible fashion" and contains no DFU or bootloader commands. — [thalmiclabs/myo-bluetooth](https://github.com/thalmiclabs/myo-bluetooth/); [myohw.h](https://raw.githubusercontent.com/thalmiclabs/myo-bluetooth/master/myohw.h)

### Inferences
- Because the USB drive is served by the main MCU on bus power, the "Myo" drive mounting on a Mac proves the board is alive even if the cells are dead. If the drive mounts, reflashing 1.5.1970 is cheap and rules out firmware as the cause.
- Whether the .hex also reflashes the nRF51 radio firmware is not documented; there is no public SWD procedure for either chip.
- macOS note (inference): on recent macOS, copying with Finder may create hidden `._` files; the SUCCESS.txt check is the confirmation to rely on.

### Gaps
- No source documents a Myo-specific bootloader LED pattern or a button combination to force bootloader mode. No public SWD/JTAG pinout or recovery for a Myo whose USB bootloader itself is corrupt was found.
- "Constant red" status LED has no documented user fix.

---

## Q6. Bluetooth-only use (no dongle) on Mac, Linux, Windows and phones, 2020-2026; first steps that made it show up in a scan; nRF Connect as a test

### Takeaway
Dongle-less BLE works on all desktop platforms through Bleak-based libraries (dl-myo, pymyo, FreeMyo.py, MyoInterface), and a 2025 macOS user found their Myo by filtering a Bleak scan on the Myo control service UUID `d5060001-a904-deb9-4748-2c7f4a124842`. The Myo only advertises while it is awake and unplugged, and a band still connected or bonded elsewhere may not show up. A phone scanner app (nRF Connect, LightBlue, BlueSee) is the standard first test and is named for exactly this purpose in one library's README.

### Cited Findings
- Scan filter that worked on macOS (2025-09): `BleakScanner.discover(service_uuids=["d5060001-a904-deb9-4748-2c7f4a124842"])` — user: "Yes, it can discover my Myo". On macOS Bleak returns a device UUID rather than a MAC. — [Crimson-Crow/pymyo issue #4](https://github.com/Crimson-Crow/pymyo/issues/4); pymyo describes itself as platform-agnostic BLE "without requiring the original dongle or the Myo SDK" — [pymyo on PyPI](https://pypi.org/project/pymyo/)
- dl-myo: "Any Myo Armband should have the service UUID d5060001-a904-deb9-4748-2c7f4a124842"; supports Linux, Raspberry Pi, macOS and Windows via Bleak (Docker example "doesn't work on macOS"). — [iomz/dl-myo](https://github.com/iomz/dl-myo)
- FreeMyo.py (designed "primarily ... for macOS"): "If you're not sure about the Device UUID, download an app like BlueSee or Lightblue and do a scan. It'll come up under the name Myo"; plus the drain-to-2-3 % anecdote in Q3. — [jshahbazi/FreeMyo.py](https://github.com/jshahbazi/FreeMyo.py)
- MyoInterface (Bleak): "use Scanning_for_mac_address.py to scan for myoband mac address, mine showed up as DIUxMyo" (the advertised name is the user-set name, not necessarily "Myo"). — [madwilliam/MyoInterface](https://github.com/madwilliam/MyoInterface)
- ESP32 library (2024) auto-scans by BLE name and lists the services (control d5060001, IMU d5060002, classifier d5060003, EMG d5060005, standard battery 0x180F). — [kasi09/Myo_ESP32](https://github.com/kasi09/Myo_ESP32)
- Arduino BLE field report (2026): zero EMG data because ArduinoBLE used ATT Write-with-response to enable notifications and "the Myo never sends" a write response; switching to write-without-response fixed it. — [Fazlay Rabby on LinkedIn (2026-05)](https://www.linkedin.com/posts/fazlayrabbyofficial_after-weeks-of-debugging-i-finally-figured-activity-7465153229778132992-LZEU)
- Thalmic officially required the dongle on PCs but said developers could connect built-in adapters via the published protocol. — [Thalmic support: Can I use my computer's built-in Bluetooth? (Wayback 2019)](https://web.archive.org/web/2019/https://support.getmyo.com/hc/en-us/articles/203996655-Can-I-use-my-computers-built-in-Bluetooth-)
- Connection exclusivity (2015 review): to use the band with a phone near the computer you had to disconnect the dongle, and then disconnect the phone to go back. — [CIO review (2015)](https://www.cio.com/article/247234/thalmic-labs-myo-review-gesture-control-armband.html)
- Old caveat from myo-raw: may not work "with a Myo that has never been plugged in and set up with Myo Connect". — [dzhu/myo-raw README](https://github.com/dzhu/myo-raw/)
- A 2019-2020 report: an HM-10 user saw the Myo's status LED stay off (not connected) with the HM-10, but "when I am connecting the Bluetooth dongle to my PC, the LED turns on (blue-ish color)". — [vroland/MyoBridge issue #18](https://github.com/vroland/MyoBridge/issues/18)
- nRF Connect (Android) scanner shows advertising data, RSSI, and a CONNECT button for connectable devices; Android needs Location permission and Location service on for scanning. — [nRF Connect for Android docs](https://github.com/nordicsemi/Android-nRF-Connect/blob/main/documentation/README.md)
- Contested claim, low reliability: an aggregator asserts that "newer chipsets (Intel AX200+, Apple M-series) often reject connection handshake" with Myo. It cites no evidence, and the 2025 macOS pymyo report contradicts it for at least discovery and data. — [Alibaba electronics guide](https://electronics.alibaba.com/question/myo-armband-still-available-uses,-price-alternatives); contradicted by [pymyo issue #4/#5](https://github.com/Crimson-Crow/pymyo/issues/5)

### Inferences
- Order of tests that follows from the sources: (1) charge to solid green; (2) unplug and confirm the logo LED pulses blue (no LED means it is not awake, so no scan will find it); (3) within ~30 s, or while keeping the band moving, scan with nRF Connect or LightBlue on a phone, filtering by name "Myo" or by service UUID d5060001-...; (4) on the Mac, scan with Bleak filtered on that UUID. A phone app is a good first test because it removes macOS permission and library variables, but it cannot help if the band is dark.
- Make sure no old pairing (the original dongle, a phone with the Myo app) is in range and connected, since a connected BLE peripheral normally stops advertising.

### Gaps
- No 2020-2026 report specifically used nRF Connect on a revived Myo; the recommendation rests on the generic tool docs plus the BlueSee/LightBlue advice in FreeMyo.py.
- Exact advertising interval and how long it advertises after waking before sleeping were not found.

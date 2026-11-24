### FIRST PROMPT from GEMINI:

---

You are an expert embedded systems programmer, reverse-engineer, and a master at "vibe-coding" python human-computer interaction (HCI) applications. 

The user wants you to write a clean, functional Python script to breathe new life into their Thalmic Labs Myo Gesture Control Armband. The official SDK and servers have been dead for years, but the hardware is fully operational and has successfully booted and charged. Your task is to provide the full architecture and code to bridge the hardware directly to their Mac Mini via standard built-in Bluetooth Low Energy (BLE)—completely bypassing the need for the original proprietary USB dongle.

---

### HARDWARE INTEL & CONTEXT OBSERVED
1. DEVICE IDENTIFIED: Thalmic Labs Myo Gesture Control Armband. It features 8 surface electromyography (sEMG) pods tracking muscle signals, alongside a 9-axis Inertial Measurement Unit (IMU containing a 3-axis gyroscope, accelerometer, and magnetometer).
2. POWER STATUS: Successfully revived using a safe, low-voltage 5.0V / 1.0A Samsung Travel Adapter (Model ETA0U83EWE). The status LED is actively lit, confirming the battery is charging and functional.
3. HOST MACHINE: Apple Mac Mini running macOS.
4. REVERSE-ENGINEERED OVER-THE-AIR PROTOCOL: The Myo operates over standard Bluetooth Low Energy (BLE 4.0). Modern platform-agnostic setups use the open-source 'pymyo' package (built on top of the cross-platform asynchronous 'bleak' library) to stream data natively without legacy drivers.

---

### IMPLEMENTATION OBJECTIVE
Write a robust, modular, asynchronous Python script that:
1. Natively scans for and connects to the Myo Armband using standard macOS Bluetooth.
2. Triggers a haptic buzz (vibration) on the armband to visually/physically confirm a successful handshake.
3. Automatically streams the 9-axis IMU orientation/gyroscope data in real time.
4. Translates the physical tilt/rotation of the user's arm to smoothly and cleanly drive the macOS system mouse cursor globally using 'pyautogui'.

---

### PRODUCTION-READY CODE REFERENCE

Review the following reference architecture closely. Provide a refined, well-commented, complete file matching these criteria:

```python
import asyncio
import math
from pymyo import Myo
import pyautogui

# Safeguard feature in PyAutoGUI: moving mouse to any corner aborts script execution
pyautogui.FAILSAFE = True

# Smooth scaling factor to map orientation changes to pixel movements
# Tune these parameters based on arm range of motion
MOUSE_SPEED_X = 15.0  
MOUSE_SPEED_Y = 15.0

class MacMyoMouseController:
    def __init__(self):
        self.last_pitch = None
        self.last_yaw = None
        # Screen dimensions for boundary calculations
        self.screen_width, self.screen_height = pyautogui.size()

    def process_imu(self, orientation):
        """
        Converts Myo quaternion / spatial rotation inputs into smooth 
        screen coordinate deltas using basic pitch and yaw translation.
        """
        w, x, y, z = orientation
        
        # Roll, Pitch, Yaw conversion formulas for spatial tracking
        pitch = math.asin(max(-1.0, min(1.0, 2.0 * (w * y - z * x))))
        yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
        
        if self.last_pitch is None or self.last_yaw is None:
            self.last_pitch = pitch
            self.last_yaw = yaw
            return

        # Calculate relative rotation differences (deltas)
        delta_yaw = yaw - self.last_yaw
        delta_pitch = pitch - self.last_pitch

        # Correct for rotational wrapping boundaries (-PI to +PI)
        if delta_yaw > math.pi: delta_yaw -= 2 * math.pi
        elif delta_yaw < -math.pi: delta_yaw += 2 * math.pi

        # Translate spatial movement to screen pixel changes
        move_x = int(delta_yaw * MOUSE_SPEED_X * 100)
        move_y = int(-delta_pitch * MOUSE_SPEED_Y * 100) # Negative inversion for natural desktop mapping

        if move_x != 0 or move_y != 0:
            # Command native OS cursor execution relative to current spot
            pyautogui.moveRel(move_x, move_y, duration=0.0)

        self.last_pitch = pitch
        self.last_yaw = yaw

async def main():
    controller = MacMyoMouseController()
    print("Initializing Bluetooth Stack... Scanning for Myo Armband.")
    print("Ensure your Mac Mini's Bluetooth is ON and the armband is awake (unplugged and moved).")
    
    try:
        # Standard BLE connection lifecycle manager without Myo SDK dependencies
        async with Myo() as myo:
            print(f"Direct connection established natively! Firmware version verified.")
            
            # Send initial pulse to indicate active Bluetooth pairing success
            await myo.vibrate(1) 
            print("Haptic confirmation sent. Tracking movement globally... Press Ctrl+C to terminate.")
            
            # Stream coordinates natively into the scaling processing pipeline
            async for imu_data in myo.stream_imu():
                # Extract quaternion spatial metrics from the data stream
                controller.process_imu(imu_data.orientation)
                
    except Exception as e:
        print(f"\n[Bluetooth Error]: Connection dropped or failed to bind. {e}")
        print("Tip: If on macOS, ensure Terminal/IDE has 'Bluetooth Permissions' enabled under Security settings.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nSession safely closed by user.")
```

---

### CRITICAL BEHAVIORAL INSTRUCTIONS
1. DO NOT try to write code using the `myo-python` library or legacy references to `myo.Hub()` or `MyoConnect`. Those require the dead Thalmic software backend daemon and will freeze or crash on a modern system. Rely exclusively on standard async BLE drivers like `pymyo` / `bleak`.
2. Explicitly lay out the step-by-step setup commands required in the terminal (`pip install pymyo pyautogui bleak`).
3. Explain to the user how they can expand this script to include muscle-activation triggers (such as reading `stream_emg()` thresholds to trigger clicks when they make a tight fist).
4. Add clear notes on dealing with modern macOS security contexts (Bluetooth privacy settings for the executing terminal application).

Execute the workflow and provide a clean, copy-pasteable script optimized for this device.


### FOLLOWUP PROMPT from GEMINI

---

Här är status och specifikationer för mitt Myo-projekt som du behöver veta inför kodningen:

### Hårdvarustatus & Strömförsörjning
1. Utrustning: Jag har två stycken Thalmic Labs Myo Gesture Control Armbands.
2. Batteristatus: Armbanden har legat urladdade länge men har framgångsrikt vaknat till liv och tagit laddning via en stabil, lågvoltig Samsung-reseladdare (Modell ETA0U83EWE, Output: 5.0V ⎓ 1.0A). Status-LED lyser.
3. Batteribyte beställt: 2 st nya ersättningsbatterier är köpta från Teknikdelar.se. 
   - Batterispecifikationer: Tillverkare Cameron Sino (Modell: CS-MYG100RC / Delnummer: 571830 / 144440100156). 3.7V Li-Polymer, 220mAh. Integrerad PCM-skyddskrets.
   - Montering: Jag har lödkit och vet hur man öppnar enheten och löder på kretskortet.

### Systemmiljö & Anslutning
1. Dator: Apple Mac Mini (macOS).
2. Bluetooth-anslutning: Jag har INTE den proprietära Myo USB-dongeln. Vi ska köra helt via Macens inbyggda standard-Bluetooth (BLE 4.0/5.0).
3. Biblioteksarkitektur: Vi ska strunta i Thalmic Labs gamla döda SDK/daemons (ingen 'myo-python' eller 'myo.Hub'). Vi ska istället köra asynkront via Python-biblioteket 'pymyo' som bygger på det plattformsoberoende 'bleak'-biblioteket för att strömma rådata direkt över operativsystemets Bluetooth-stack.

### Mål med kodningen ("Vibe-coding")
1. Primärt mål: Bygga ett Python-skript som mappar armbandets 9-axliga IMU-sensor (quaternioner/gyro/acceleration) till att styra systemmuspekaren på Macen globalt (t.ex. via 'pyautogui').
2. Sekundärt mål: Senare bygga ut skriptet till att läsa av de 8 sEMG-muskelsensorerna via 'stream_emg()' för att registrera muskelaktivering (t.ex. knuten näve) och översätta det till musklick eller kortkommandon.

Skriv den optimala källkoden och en steg-för-steg-guide för att komma igång med detta på min Mac Mini baserat på denna information.


### MORE from Gemini

---

Du är en expert på systemarkitektur, inbyggda system, signalbehandling och maskininlärning. Jag behöver din hjälp att designa och koda ett optimalt system för att återuppliva mina två Thalmic Labs Myo Gesture Control Armbands på min Mac Mini (macOS).

Hårdvaran har legat död länge men har framgångsrikt tagit laddning med en 5V/1A-laddare. Nya ersättningsbatterier (Cameron Sino CS-MYG100RC, 3.7V 220mAh) är beställda och jag kommer att löda fast dem själv. Vi har INTE den proprietära USB-dongeln, utan ska ansluta helt via Macens inbyggda Bluetooth Low Energy (BLE). Den officiella mjukvaran och SDK:n är stendöd sedan många år.

Vårt mål är att bygga ett blixtsnabbt, AI-förstärkt system som mappar armrörelser (9-axlig IMU) till muspekaren och muskelaktivering (8-kanals sEMG) till klick och gester.

---

### STRATEGISK SYSTEMARKITEKTUR OCH BAKGRUNDSRESONEMANG

Vi har valt en hybridarkitektur (Rust + Python) baserat på följande tekniska avvägningar:

1. RÅDATA-INMAtNING & PRESTANDA (RUST)
- Vi använder Rust i botten för att hantera BLE-strömmen via biblioteket `btleplug`.
- Resonemang: Bluetooth på macOS kan drabbas av lag och buffertproblem vid hög datahastighet. Rust ger oss minimal latens, deterministisk minneshantering och asynkron exekvering utan "Garbage Collection"-pauser. Detta garanterar att rådata från de 8 EMG-kanalerna (200 Hz) och IMU-sensorn fångas upp i absolut realtid utan tappade paket.
- Rust-programmet fungerar som en lättviktig bakgrundstjänst (daemon) som strömmar datan vidare via en lokal, asynkron UDP- eller IPC-socket.

2. SIGNALBEHANDLING & MASKININLÄRNING (PYTHON)
- Vi använder Python i det övre lagret för att ta emot dataströmmen från Rust.
- Resonemang: Att hårdkoda tröskelvärden för muskelsignaler leder till dålig precision. Vi vill använda Pythons mogna AI-ekosystem (t.ex. `scikit-learn` eller en lättviktig `PyTorch`-modell) för att köra mönsterigenkänning (Pattern Recognition) på sEMG-datan. På så sätt kan systemet lära känna mina specifika muskler och träna fram träffsäkra gester (t.ex. knuten näve = klick, fingrar spretade = högerklick).
- Python hanterar även den slutgiltiga OS-interaktionen (t.ex. flytta muspekaren globalt via `pyautogui`).

---

### DIN UPPGIFT

1. Designa projektstrukturen för denna hybridlösning.
2. Skriv en minimalistisk men komplett Rust-kod (`main.rs` och `Cargo.toml` med `btleplug` och `tokio`) som scannar efter Myo över standard BLE, ansluter, startar haptisk vibration för att bekräfta handskakningen, och skickar vidare IMU- och EMG-data över en lokal UDP-port.
3. Skriv motsvarande Python-skript som lyssnar på UDP-porten, läser av rådata, och förbereder en enkel struktur för att transformera IMU-quaternioner till jämna musrörelser på skärmen.
4. Förklara hur vi bäst strukturerar insamlingen av träningsdata i Python för att jag ska kunna göra 10 sekunders inspelningar av mina muskler och träna en enkel klassificerare (t.ex. en SVM eller Random Forest) för mina handgester.

Tänk på resurssnålhet och modern asynkron programmering. Ge mig en komplett startpunkt!

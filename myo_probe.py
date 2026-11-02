"""Find Myo armbands over Bluetooth LE and read battery, firmware and serial.

Uses only bleak and the GATT layout Thalmic published in myohw.h.
Each Myo found gets one short vibration so you can tell which is which.
"""
import asyncio
import struct
import sys

from bleak import BleakClient, BleakScanner

CONTROL_SERVICE = "d5060001-a904-deb9-4748-2c7f4a124842"
INFO_CHAR = "d5060101-a904-deb9-4748-2c7f4a124842"
FIRMWARE_CHAR = "d5060201-a904-deb9-4748-2c7f4a124842"
COMMAND_CHAR = "d5060401-a904-deb9-4748-2c7f4a124842"
BATTERY_CHAR = "00002a19-0000-1000-8000-00805f9b34fb"

HARDWARE = {1: "rev C", 2: "rev D"}
SKU = {0: "unknown", 1: "black", 2: "white"}
VIBRATE_SHORT = bytes([0x03, 0x01, 0x01])


async def probe(device, rssi):
    print(f"\n== {device.name or '(no name)'}  id={device.address}  rssi={rssi} dBm")
    async with BleakClient(device, timeout=20) as client:
        battery = (await client.read_gatt_char(BATTERY_CHAR))[0]
        major, minor, patch, hw = struct.unpack("<4H", await client.read_gatt_char(FIRMWARE_CHAR))
        info = await client.read_gatt_char(INFO_CHAR)
        serial = ":".join(f"{b:02x}" for b in reversed(info[0:6]))
        sku = info[13] if len(info) > 13 else 0
        print(f"   battery   {battery} %")
        print(f"   firmware  {major}.{minor}.{patch}  hardware {HARDWARE.get(hw, hw)}")
        print(f"   serial    {serial}  colour {SKU.get(sku, sku)}")
        await client.write_gatt_char(COMMAND_CHAR, VIBRATE_SHORT, response=True)
        print("   vibrated once")


async def main():
    # Scan in 10 s rounds until a Myo shows up or the cap is reached.
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 12
    waited, myos = 0.0, []
    print(f"Scanning up to {cap:.0f} s, stopping at the first round that sees a Myo ...")
    while waited < cap and not myos:
        found = await BleakScanner.discover(timeout=min(10, cap - waited), return_adv=True)
        waited += min(10, cap - waited)
        myos = [
            (d, a) for d, a in found.values()
            if CONTROL_SERVICE in [u.lower() for u in a.service_uuids]
            or "myo" in (a.local_name or d.name or "").lower()
        ]
        print(f"  {waited:.0f} s: {len(found)} BLE devices, {len(myos)} Myo")
    if not myos:
        named = sorted({(a.local_name or d.name) for d, a in found.values() if (a.local_name or d.name)})
        print(f"No Myo in {cap:.0f} s. Named devices seen:", ", ".join(named) or "none")
    for d, a in myos:
        try:
            await probe(d, a.rssi)
        except Exception as e:
            print(f"   failed: {type(e).__name__}: {e}")


asyncio.run(main())

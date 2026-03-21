# Flashing the MacroPad Firmware

Okay so this is actually pretty easy, don't panic.

---

## Step 1 — Install CircuitPython on the ESP32-S3

1. Go to [circuitpython.org/downloads](https://circuitpython.org/downloads) and search **ESP32-S3**.  
   Pick the variant that matches your exact board (check the flash size — usually 4MB or 8MB).

2. Hold the **BOOT** button on your ESP32-S3 and plug it into USB.  
   It should show up as a drive called `ESP32S3` or similar.

3. Drag the downloaded `.bin` file onto that drive (or use `esptool` if it doesn't show up as a drive).

4. It'll reboot and show up as a `CIRCUITPY` drive. You're done with this step.

---

## Step 2 — Install the libraries

1. Download the **CircuitPython Library Bundle** for your version from [circuitpython.org/libraries](https://circuitpython.org/libraries).

2. Unzip it. Inside you'll find a `lib/` folder with a ton of `.mpy` files.

3. Copy these specific folders/files into the `lib/` folder on your `CIRCUITPY` drive:

```
adafruit_hid/
adafruit_neopixel/          (just neopixel.mpy actually)
adafruit_display_text/
adafruit_displayio_ssd1306.mpy
adafruit_ble/
adafruit_ble_services/
```

> If you don't want Bluetooth, you can skip the `adafruit_ble` ones. Just set USB_MODE stuff and don't flip the mode switch.

---

## Step 3 — Copy the firmware files

Copy all of these onto the root of your `CIRCUITPY` drive:

```
boot.py
code.py
config.py
keymap.py
```

Your drive should look like:
```
CIRCUITPY/
├── boot.py
├── code.py
├── config.py
├── keymap.py
└── lib/
    ├── adafruit_hid/
    ├── neopixel.mpy
    ├── adafruit_display_text/
    ├── adafruit_displayio_ssd1306.mpy
    ├── adafruit_ble/
    └── adafruit_ble_services/
```

---

## Step 4 — Update config.py for your wiring

Open `config.py` and check the pin numbers match how you actually wired things.  
The defaults are:

| Thing | Pins |
|---|---|
| Row pins | GPIO1–GPIO4 |
| Col pins | GPIO5–GPIO8 |
| NeoPixel data | GPIO18 |
| OLED SDA | GPIO9 |
| OLED SCL | GPIO10 |
| Mode switch | GPIO12 |

If yours are different, just change the numbers. That's literally all you have to do.

---

## Step 5 — Plug it in and test

- **USB mode**: keep the mode switch HIGH (or just leave GPIO0 floating — it's pulled up by default). It should show up as a USB keyboard.
- **Bluetooth mode**: flip the switch to pull GPIO0 LOW before plugging in. Look for "Next-Gen MacroPad" in your Bluetooth devices.

The OLED should show the current layer and mode. LEDs should light up. Press a key and something should happen.

If nothing happens, open a serial monitor (Mu editor works great, or PuTTY/screen) and check for error messages.

---

## Troubleshooting

**OLED is blank**  
→ Check I2C address. Try `0x3D` in config.py if `0x3C` doesn't work.  
→ Double-check SDA/SCL wiring.

**Keys don't register**  
→ Check your ROW_PINS and COL_PINS in config.py.  
→ Make sure diodes are the right way around (cathode toward column).

**Bluetooth won't pair**  
→ Make sure GPIO0 is pulled LOW *before* powering on (boot.py reads it at startup).  
→ Delete the device from your PC's Bluetooth list and try again.

**LEDs wrong color or not lighting**  
→ Check NEOPIXEL_PIN in config.py.  
→ Some NeoPixel strips are RGB not GRB — change `pixel_order=neopixel.GRB` to `RGB` in code.py.

**Import errors on boot**  
→ A library is missing from `/lib`. Check the error message — it'll tell you exactly which one.

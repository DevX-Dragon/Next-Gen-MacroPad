# code.py — Next-Gen MacroPad firmware
# ESP32-S3 | CircuitPython | 4x4 matrix | NeoPixels | OLED | USB+BT
# by Dragon (DevX-Dragon) — github.com/DevX-Dragon

import time
import board
import busio
import digitalio
import neopixel
import displayio
import terminalio
import supervisor

from adafruit_display_text import label
from adafruit_displayio_ssd1306 import SSD1306
import adafruit_displayio_ssd1306

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

import config
import keymap

# ─── DETECT MODE (set in boot.py via GPIO0) ───────────────────────────────────
_mode_pin = digitalio.DigitalInOut(config.MODE_PIN)
_mode_pin.direction = digitalio.Direction.INPUT
_mode_pin.pull = digitalio.Pull.UP
USB_MODE = _mode_pin.value  # True = USB HID, False = Bluetooth


# ══════════════════════════════════════════════════════════════════════════════
# USB HID SETUP
# ══════════════════════════════════════════════════════════════════════════════
keyboard = None
layout   = None
consumer = None

if USB_MODE:
    try:
        keyboard = Keyboard(usb_hid.devices)
        layout   = KeyboardLayoutUS(keyboard)
        consumer = ConsumerControl(usb_hid.devices)
        print("[USB] HID ready")
    except Exception as e:
        print(f"[USB] HID init failed: {e}")
        USB_MODE = False


# ══════════════════════════════════════════════════════════════════════════════
# BLUETOOTH SETUP (ESP32-S3 via _bleio)
# ══════════════════════════════════════════════════════════════════════════════
bt_keyboard = None
bt_consumer = None

if not USB_MODE:
    try:
        from adafruit_ble import BLERadio
        from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
        from adafruit_ble.services.standard.hid import HIDService
        from adafruit_ble.services.standard.device_info import DeviceInfoService

        ble         = BLERadio()
        ble.name    = config.BT_DEVICE_NAME
        hid_service = HIDService()
        device_info = DeviceInfoService(
            software_revision="1.0",
            manufacturer="DevX-Dragon"
        )
        advertisement = ProvideServicesAdvertisement(hid_service)

        bt_keyboard = Keyboard(hid_service.devices)
        layout      = KeyboardLayoutUS(bt_keyboard)
        bt_consumer = ConsumerControl(hid_service.devices)

        print("[BT] Advertising as:", config.BT_DEVICE_NAME)
        ble.start_advertising(advertisement)
    except Exception as e:
        print(f"[BT] Init failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# NEOPIXELS
# ══════════════════════════════════════════════════════════════════════════════
pixels = neopixel.NeoPixel(
    config.NEOPIXEL_PIN,
    config.NEOPIXEL_COUNT,
    brightness=config.NEOPIXEL_BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# Breathing effect state
_breathe_val = 0.0
_breathe_dir = 1

# tracking when each key was last pressed for fade-out
_key_pressed_time = [0.0] * 16

def _hsv_to_rgb(h, s, v):
    """Convert HSV (0–1 each) to (r, g, b) 0–255."""
    if s == 0:
        c = int(v * 255)
        return (c, c, c)
    i = int(h * 6)
    f = h * 6 - i
    p, q, t = v*(1-s), v*(1-s*f), v*(1-s*(1-f))
    i %= 6
    if i == 0: r, g, b = v, t, p
    elif i == 1: r, g, b = q, v, p
    elif i == 2: r, g, b = p, v, t
    elif i == 3: r, g, b = p, q, v
    elif i == 4: r, g, b = t, p, v
    else:        r, g, b = v, p, q
    return (int(r*255), int(g*255), int(b*255))

def update_leds(current_layer, pressed_keys):
    global _breathe_val, _breathe_dir
    effect = config.RGB_EFFECT
    now    = time.monotonic()

    if effect == "solid":
        color = config.LAYER_COLORS[current_layer % len(config.LAYER_COLORS)]
        for i in range(config.NEOPIXEL_COUNT):
            pixels[i] = color

    elif effect == "rainbow":
        for i in range(config.NEOPIXEL_COUNT):
            hue = (i / config.NEOPIXEL_COUNT + now * 0.1) % 1.0
            pixels[i] = _hsv_to_rgb(hue, 1.0, 1.0)

    elif effect == "breathe":
        _breathe_val += 0.02 * _breathe_dir
        if _breathe_val >= 1.0: _breathe_dir = -1
        if _breathe_val <= 0.0: _breathe_dir =  1
        base = config.LAYER_COLORS[current_layer % len(config.LAYER_COLORS)]
        color = tuple(int(c * _breathe_val) for c in base)
        for i in range(config.NEOPIXEL_COUNT):
            pixels[i] = color

    elif effect == "reactive":
        for i in range(config.NEOPIXEL_COUNT):
            if i in pressed_keys:
                pixels[i] = config.RGB_PRESS_COLOR
                _key_pressed_time[i] = now
            else:
                age   = now - _key_pressed_time[i]
                fade  = max(0.0, 1.0 - age * 3.0)   # fades out over ~330ms
                base  = config.LAYER_COLORS[current_layer % len(config.LAYER_COLORS)]
                press = config.RGB_PRESS_COLOR
                r = int(press[0] * fade + base[0] * (1 - fade))
                g = int(press[1] * fade + base[1] * (1 - fade))
                b = int(press[2] * fade + base[2] * (1 - fade))
                pixels[i] = (r, g, b)

    pixels.show()


# ══════════════════════════════════════════════════════════════════════════════
# OLED DISPLAY
# ══════════════════════════════════════════════════════════════════════════════
displayio.release_displays()

i2c     = busio.I2C(config.OLED_SCL, config.OLED_SDA)
bus     = displayio.I2CDisplay(i2c, device_address=config.OLED_ADDR)
display = SSD1306(bus, width=config.OLED_WIDTH, height=config.OLED_HEIGHT)

LAYER_NAMES = ["General", "Streaming", "Coding", "Numpad"]

_last_activity  = time.monotonic()
_display_on     = True

def make_display_group(layer_idx, mode_str, last_key_str=""):
    """Build the displayio group shown on OLED."""
    group = displayio.Group()

    # Header bar
    header = label.Label(
        terminalio.FONT, text="Next-Gen MacroPad",
        color=0xFFFFFF, x=2, y=6
    )
    group.append(header)

    div_bmp = displayio.Bitmap(config.OLED_WIDTH, 1, 1)
    div_pal = displayio.Palette(1)
    div_pal[0] = 0xFFFFFF
    div = displayio.TileGrid(div_bmp, pixel_shader=div_pal, x=0, y=14)
    group.append(div)

    # Layer info
    layer_name = LAYER_NAMES[layer_idx] if layer_idx < len(LAYER_NAMES) else f"Layer {layer_idx}"
    layer_lbl  = label.Label(
        terminalio.FONT,
        text=f"Layer {layer_idx}: {layer_name}",
        color=0xFFFFFF, x=2, y=26
    )
    group.append(layer_lbl)

    # Mode (USB / BT)
    mode_lbl = label.Label(
        terminalio.FONT, text=mode_str,
        color=0xFFFFFF, x=2, y=40
    )
    group.append(mode_lbl)

    # Last key hint
    if last_key_str:
        key_lbl = label.Label(
            terminalio.FONT, text=last_key_str,
            color=0xFFFFFF, x=2, y=54
        )
        group.append(key_lbl)

    return group

def refresh_display(layer_idx, last_key=""):
    global _display_on
    mode_str = "Mode: USB HID" if USB_MODE else "Mode: Bluetooth"
    display.root_group = make_display_group(layer_idx, mode_str, last_key)
    _display_on = True

def dim_display():
    global _display_on
    if _display_on:
        display.root_group = displayio.Group()  # blank
        _display_on = False


# ══════════════════════════════════════════════════════════════════════════════
# KEY MATRIX
# ══════════════════════════════════════════════════════════════════════════════
rows = []
for pin in config.ROW_PINS:
    r = digitalio.DigitalInOut(pin)
    r.direction = digitalio.Direction.OUTPUT
    r.value = False
    rows.append(r)

cols = []
for pin in config.COL_PINS:
    c = digitalio.DigitalInOut(pin)
    c.direction = digitalio.Direction.INPUT
    c.pull = digitalio.Pull.DOWN
    cols.append(c)

_prev_state = [False] * 16
_debounce   = [0.0]  * 16


def scan_matrix():
    """Return list of currently pressed key indices."""
    pressed = []
    for r_idx, row in enumerate(rows):
        row.value = True
        time.sleep(0.001)
        for c_idx, col in enumerate(cols):
            if col.value:
                pressed.append(r_idx * 4 + c_idx)
        row.value = False
    return pressed


# ══════════════════════════════════════════════════════════════════════════════
# KEY ACTION 
# ══════════════════════════════════════════════════════════════════════════════
current_layer   = 0
_last_key_label = ""

def do_press(action):
    """Execute a key action on press."""
    global current_layer, _last_key_label

    atype = action[0]

    if atype == "none":
        return

    elif atype == "key":
        kc = action[1]
        _last_key_label = f"Key: {kc}"
        if USB_MODE and keyboard:
            keyboard.press(kc)
        elif bt_keyboard:
            bt_keyboard.press(kc)

    elif atype == "mod":
        # supports 2 or 3 keycodes e.g. ("mod", CTRL, SHIFT, K)
        keys = action[1:]
        _last_key_label = "Combo"
        if USB_MODE and keyboard:
            keyboard.press(*keys)
        elif bt_keyboard:
            bt_keyboard.press(*keys)

    elif atype == "string":
        text = action[1]
        _last_key_label = f"> {text[:12]}"
        if layout:
            layout.write(text)

    elif atype == "media":
        code = action[1]
        _last_key_label = "Media"
        if USB_MODE and consumer:
            consumer.press(code)
        elif bt_consumer:
            bt_consumer.press(code)

    elif atype == "layer":
        val = action[1]
        if val == "cycle":
            current_layer = (current_layer + 1) % len(keymap.LAYERS)
        else:
            current_layer = int(val) % len(keymap.LAYERS)
        _last_key_label = f">> Layer {current_layer}"
        refresh_display(current_layer, _last_key_label)
        return  # skip generic display refresh below

    refresh_display(current_layer, _last_key_label)


def do_release(action):
    """Release keys on key-up."""
    atype = action[0]
    if atype in ("key",):
        if USB_MODE and keyboard:
            keyboard.release(action[1])
        elif bt_keyboard:
            bt_keyboard.release(action[1])
    elif atype == "mod":
        keys = action[1:]
        if USB_MODE and keyboard:
            keyboard.release(*keys)
        elif bt_keyboard:
            bt_keyboard.release(*keys)
    elif atype == "media":
        if USB_MODE and consumer:
            consumer.release()
        elif bt_consumer:
            bt_consumer.release()


# ══════════════════════════════════════════════════════════════════════════════
# STARTUP
# ══════════════════════════════════════════════════════════════════════════════
# Startup animation — wipe LEDs layer color
startup_color = config.LAYER_COLORS[0]
for i in range(config.NEOPIXEL_COUNT):
    pixels[i] = startup_color
    pixels.show()
    time.sleep(0.03)
time.sleep(0.3)

refresh_display(current_layer)
print(f"[BOOT] MacroPad ready | {'USB' if USB_MODE else 'Bluetooth'} mode")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════════════════════
while True:
    now = time.monotonic()

    # BT reconnect if disconnected
    if not USB_MODE:
        try:
            if not ble.connected:
                if not ble.advertising:
                    ble.start_advertising(advertisement)
        except Exception:
            pass

    # Scan keys
    pressed_now = scan_matrix()
    pressed_set  = set(pressed_now)

    for key_idx in range(16):
        was_pressed = _prev_state[key_idx]
        is_pressed  = key_idx in pressed_set

        # Debounce
        if now - _debounce[key_idx] < config.DEBOUNCE_MS / 1000:
            continue

        layer_map = keymap.LAYERS[current_layer % len(keymap.LAYERS)]
        action    = layer_map[key_idx] if key_idx < len(layer_map) else ("none",)

        if is_pressed and not was_pressed:
            _debounce[key_idx]  = now
            _prev_state[key_idx] = True
            _last_activity       = now
            do_press(action)

        elif not is_pressed and was_pressed:
            _debounce[key_idx]  = now
            _prev_state[key_idx] = False
            do_release(action)

    # RGB update
    update_leds(current_layer, pressed_set)

    # Display sleep
    if config.DISPLAY_SLEEP_SEC > 0:
        if now - _last_activity > config.DISPLAY_SLEEP_SEC:
            dim_display()

    time.sleep(0.001)  # tiny yield so CircuitPython stays happy

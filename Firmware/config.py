# config.py — all your hardware settings live here
# Change this file to match your wiring, don't dig through code.py

import board

# ─── KEY MATRIX PINS ──────────────────────────────────────────────────────────
# 4x4 matrix — 4 rows, 4 cols = 16 keys
ROW_PINS = [board.GPIO4, board.GPIO5, board.GPIO6, board.GPIO7]
COL_PINS = [board.GPIO8, board.GPIO9, board.GPIO10, board.GPIO11]

# ─── NEOPIXEL ─────────────────────────────────────────────────────────────────
NEOPIXEL_PIN   = board.GPIO18   # Data pin for NeoPixels
NEOPIXEL_COUNT = 16             # One LED per key
NEOPIXEL_BRIGHTNESS = 0.3       # 0.0 – 1.0 (keep it low to not blind yourself)

# ─── OLED DISPLAY ────────────────────────────────────────────────────────────
OLED_SDA = board.GPIO1
OLED_SCL = board.GPIO2
OLED_WIDTH  = 128
OLED_HEIGHT = 64
OLED_ADDR   = 0x3C             # Default I2C address, try 0x3D if it doesn't show up

# ─── MODE SWITCH ──────────────────────────────────────────────────────────────
# This pin is read in boot.py to decide USB vs BT mode
# HIGH (pulled up) = USB HID   |   LOW (switch to GND) = Bluetooth
MODE_PIN = board.GPIO0

# ─── BLUETOOTH ────────────────────────────────────────────────────────────────
BT_DEVICE_NAME = "Next-Gen MacroPad"

# ─── DEBOUNCE ─────────────────────────────────────────────────────────────────
DEBOUNCE_MS = 20  

# ─── DISPLAY SLEEP ────────────────────────────────────────────────────────────
DISPLAY_SLEEP_SEC = 30  

# ─── RGB EFFECTS ──────────────────────────────────────────────────────────────
# Options: "solid", "rainbow", "breathe", "reactive"
RGB_EFFECT = "reactive"
RGB_IDLE_COLOR = (0, 80, 255)      # Blue idle glow
RGB_PRESS_COLOR = (255, 255, 255)  # White flash on keypress

# ─── LAYERS ───────────────────────────────────────────────────────────────────
# Colour shown on OLED and LEDs per layer
LAYER_COLORS = [
    (0, 80, 255),    # — Blue
    (0, 220, 80),    # — Green
    (255, 60, 0),    # — Orange
    (180, 0, 255),   # — Purple
]

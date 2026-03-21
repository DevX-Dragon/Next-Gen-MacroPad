# keymap.py — all your macros live here
# Edit this file to change what each key does. No other file needs touching.
#
# Layout (how keys map to the grid):
#  [ 0] [ 1] [ 2] [ 3]
#  [ 4] [ 5] [ 6] [ 7]
#  [ 8] [ 9] [10] [11]
#  [12] [13] [14] [15]  ← key 15 = LAYER SWITCH (bottom right)
#
# Key types:
#   ("key",     keycode)           — single keypress
#   ("mod",     modifier, keycode) — modifier + key  e.g. Ctrl+C
#   ("string",  "text to type")    — types a whole string
#   ("media",   consumer_code)     — media key (volume, play, etc.)
#   ("layer",   layer_number)      — switch to that layer (or use "cycle")
#   ("none",)                      — does nothing
#  these codes are manually written by me

import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control_code import ConsumerControlCode

# ─── LAYER 0 — General / Default ──────────────────────────────────────────────
LAYER_0 = [
    ("mod",    Keycode.CONTROL, Keycode.C),       #  0 — Copy
    ("mod",    Keycode.CONTROL, Keycode.V),       #  1 — Paste
    ("mod",    Keycode.CONTROL, Keycode.Z),       #  2 — Undo
    ("mod",    Keycode.CONTROL, Keycode.Y),       #  3 — Redo

    ("mod",    Keycode.CONTROL, Keycode.S),       #  4 — Save
    ("mod",    Keycode.ALT,     Keycode.TAB),     #  5 — Alt+Tab
    ("key",    Keycode.PRINT_SCREEN),             #  6 — Screenshot
    ("mod",    Keycode.WINDOWS, Keycode.D),       #  7 — Show Desktop

    ("mod",    Keycode.CONTROL, Keycode.A),       #  8 — Select All
    ("mod",    Keycode.CONTROL, Keycode.X),       #  9 — Cut
    ("mod",    Keycode.CONTROL, Keycode.F),       # 10 — Find
    ("mod",    Keycode.ALT,     Keycode.F4),      # 11 — Close Window

    ("media",  ConsumerControlCode.MUTE),         # 12 — Mute
    ("media",  ConsumerControlCode.VOLUME_DECREMENT), # 13 — Vol Down
    ("media",  ConsumerControlCode.VOLUME_INCREMENT), # 14 — Vol Up
    ("layer",  "cycle"),                          # 15 — Next Layer ★
]

# ─── LAYER 1 — Streaming / OBS ────────────────────────────────────────────────
LAYER_1 = [
    ("key",    Keycode.F13),   #  0 — OBS: Scene 1
    ("key",    Keycode.F14),   #  1 — OBS: Scene 2
    ("key",    Keycode.F15),   #  2 — OBS: Scene 3
    ("key",    Keycode.F16),   #  3 — OBS: Scene 4

    ("key",    Keycode.F17),   #  4 — OBS: Start/Stop Stream
    ("key",    Keycode.F18),   #  5 — OBS: Start/Stop Recording
    ("key",    Keycode.F19),   #  6 — OBS: Mute Mic
    ("key",    Keycode.F20),   #  7 — OBS: Mute Desktop Audio

    ("media",  ConsumerControlCode.PLAY_PAUSE),        #  8 — Play/Pause music
    ("media",  ConsumerControlCode.SCAN_PREVIOUS_TRACK), # 9 — Prev Track
    ("media",  ConsumerControlCode.SCAN_NEXT_TRACK),   # 10 — Next Track
    ("media",  ConsumerControlCode.MUTE),              # 11 — Mute

    ("string", "!clip "),      # 12 — Chat command: !clip
    ("string", "!so "),        # 13 — Chat command: !so (shoutout)
    ("string", "Be right back!"), # 14 — BRB message
    ("layer",  "cycle"),       # 15 — Next Layer ★
]

# ─── LAYER 2 — Coding / Dev ───────────────────────────────────────────────────
LAYER_2 = [
    ("mod",    Keycode.CONTROL, Keycode.GRAVE),        #  0 — Toggle terminal (VS Code)
    ("mod",    Keycode.CONTROL, Keycode.SHIFT, Keycode.P), #  1 — Command palette
    ("key",    Keycode.F5),                            #  2 — Run / Debug
    ("key",    Keycode.F12),                           #  3 — Go to definition

    ("mod",    Keycode.CONTROL, Keycode.SLASH),        #  4 — Toggle comment
    ("mod",    Keycode.ALT,     Keycode.UP_ARROW),     #  5 — Move line up
    ("mod",    Keycode.ALT,     Keycode.DOWN_ARROW),   #  6 — Move line down
    ("mod",    Keycode.CONTROL, Keycode.D),            #  7 — Select next occurrence

    ("mod",    Keycode.CONTROL, Keycode.SHIFT, Keycode.K), #  8 — Delete line
    ("mod",    Keycode.CONTROL, Keycode.B),            #  9 — Toggle sidebar
    ("mod",    Keycode.CONTROL, Keycode.SHIFT, Keycode.FIVE), # 10 — Format document
    ("key",    Keycode.F2),                            # 11 — Rename symbol

    ("string", "print()"),     # 12 — Type print()
    ("string", "# TODO: "),    # 13 — Type TODO comment
    ("string", "git commit -m \"\""), # 14 — Git commit starter
    ("layer",  "cycle"),       # 15 — Next Layer ★
]

# ─── LAYER 3 — Numpad ─────────────────────────────────────────────────────────
LAYER_3 = [
    ("key",    Keycode.SEVEN),  #  0
    ("key",    Keycode.EIGHT),  #  1
    ("key",    Keycode.NINE),   #  2
    ("key",    Keycode.BACKSPACE), # 3

    ("key",    Keycode.FOUR),   #  4
    ("key",    Keycode.FIVE),   #  5
    ("key",    Keycode.SIX),    #  6
    ("key",    Keycode.EQUALS), #  7 — +

    ("key",    Keycode.ONE),    #  8
    ("key",    Keycode.TWO),    #  9
    ("key",    Keycode.THREE),  # 10
    ("key",    Keycode.MINUS),  # 11 — -

    ("key",    Keycode.ZERO),   # 12
    ("key",    Keycode.PERIOD), # 13
    ("key",    Keycode.ENTER),  # 14
    ("layer",  "cycle"),        # 15 — Next Layer ★
]

# All layers in order — add more if you want, just remember to add a color in config.py
LAYERS = [LAYER_0, LAYER_1, LAYER_2, LAYER_3]

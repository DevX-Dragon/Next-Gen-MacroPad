# boot.py — runs once on startup before code.py
# Disables USB drive in BT mode to save memory, enables HID in USB mode

import storage
import usb_hid
import digitalio
import board

# Read the mode switch pin EARLY (before USB negotiation)
# Pin GPIO0 LOW = Bluetooth mode, HIGH = USB HID mode
mode_pin = digitalio.DigitalInOut(board.GPIO0)
mode_pin.direction = digitalio.Direction.INPUT
mode_pin.pull = digitalio.Pull.UP

USB_MODE = mode_pin.value  # True = USB, False = BT

if USB_MODE:
    # USB HID mode — enable keyboard + consumer control (media keys)
    usb_hid.enable(
        (usb_hid.Device.KEYBOARD, usb_hid.Device.CONSUMER_CONTROL)
    )
    storage.disable_filesystem()  # optional: disable USB drive for cleanliness
else:
    # Bluetooth mode — disable USB HID entirely to free up resources
    usb_hid.disable()

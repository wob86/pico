import time
import board
import busio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_neotrellis.neotrellis import NeoTrellis

i2c_bus = busio.I2C(scl=board.GP1, sda=board.GP0)

keyboard = Keyboard(usb_hid.devices)

trellis = NeoTrellis(i2c_bus)

# some color definitions
OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)

# this will be called when button events are received
def blink(event):
    # turn the LED on when a rising edge is detected
    if event.edge == NeoTrellis.EDGE_RISING:
        if event.number == 2:
            trellis.pixels[event.number] = RED
            keyboard.press(Keycode.R)
        elif event.number == 1:
            trellis.pixels[event.number] = YELLOW
            trellis.pixels[2] = OFF
            trellis.pixels[3] = OFF
            keyboard.press(Keycode.X)
        elif event.number == 3:
            trellis.pixels[event.number] = GREEN
            keyboard.press(Keycode.SPACE)
        elif event.number == 0:
            trellis.pixels[event.number] = PURPLE
            keyboard.press(Keycode.HOME)
        else:
            trellis.pixels[event.number] = BLUE
        print(event.number)
    # turn the LED off when a rising edge is detected
    elif event.edge == NeoTrellis.EDGE_FALLING:
        if event.number == 2:
            keyboard.release(Keycode.R)
        elif event.number == 3:
            keyboard.release(Keycode.SPACE)
        elif event.number == 1:
            keyboard.release(Keycode.X)
            trellis.pixels[event.number] = OFF
        elif event.number == 0:
            keyboard.release(Keycode.HOME)
            trellis.pixels[event.number] = OFF              
        else:
            trellis.pixels[event.number] = OFF


for i in range(16):
    # activate rising edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_RISING)
    # activate falling edge events on all keys
    trellis.activate_key(i, NeoTrellis.EDGE_FALLING)
    # set all keys to trigger the blink callback
    trellis.callbacks[i] = blink

    # cycle the LEDs on startup
    if i % 2 == 0:
        trellis.pixels[i] = PURPLE
    else:
        trellis.pixels[i] = CYAN
    time.sleep(0.05)

for i in range(16):
    trellis.pixels[i] = OFF
    time.sleep(0.05)

while True:
    # call the sync function call any triggered callbacks
    trellis.sync()
    # the trellis can only be read every 17 millisecons or so
    time.sleep(0.02)

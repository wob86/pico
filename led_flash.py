from machine import Pin
import time

led = Pin(25, Pin.OUT)
x = 0

while True:
    led.toggle()
    print("3 * {} = {}".format(x, 3 * x))
    x += 1
    time.sleep(0.5)
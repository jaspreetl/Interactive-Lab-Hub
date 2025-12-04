import time
import board
import neopixel
import adafruit_mpr121

# NeoPixel setup
pixels = neopixel.NeoPixel(board.D18, 12, brightness=0.3, auto_write=True)

# MPR121 setup
import busio
i2c = busio.I2C(board.SCL, board.SDA)
touch = adafruit_mpr121.MPR121(i2c)

print("Touch test ready...")

while True:
    for i in range(12):  # electrodes 0–11
        if touch[i].value:  # touched
            pixels.fill((0, 50, 255))  # blue flash
        else:
            pixels.fill((0, 0, 0))  # off
    time.sleep(0.05)

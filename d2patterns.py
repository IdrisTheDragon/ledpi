import time
from rpi_ws281x import *



ledcoords = []

for x in range(0,10):
    for y in range(0,10):
        ledcoords.append([x,y])

def vline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][0] == offset:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

def hline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][1] == offset:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

    
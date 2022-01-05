import time
from rpi_ws281x import *



ledcoords = []

for x in range(0,16):
    for y in range(0,7):
        ledcoords.append([x,y])

assert(len(ledcoords)>99)

def vline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][0] == offset%10:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

def hline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][1] == offset%10:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

    
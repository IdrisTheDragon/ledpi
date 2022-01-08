import time
from rpi_ws281x import *

from alpha import *



ledcoords = []

for x in range(0,20):
    for y in range(0,5):
        ledcoords.append([x,(y if x%2 == 0 else 4-y)])
print(ledcoords)
assert(len(ledcoords)>99)
assert(len(ledcoords)<120)

print('[')
for y in range(0,5):
  l = '"'
  for x in range(0,20):
    l = l + '0'
  l = l+ '"'
  print(l)
print(']')

hello = [
'01001011111000000000',
'01001000100000000000',
'01111000100000000000',
'01001000100000000000',
'01001011111000000000'
]

text = [LH, LA, LP, LP, LY, LSP, LB, LI, LR, LT, LH, LD, LA, LY,LSP,LSP]

finalText = []
for i in range(5):
    l = ''
    for t in text:
        l += t[i]
    finalText.append(l)
finalText.reverse()
print(finalText)




def vline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][0] == offset%20:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

def hline(strip, color, wait_ms=50,offset=0):
    """Wipe color across display a pixel at a time."""
    global ledcoords
    for i in range(strip.numPixels()):
        if ledcoords[i][1] == offset%5:
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, Color(0,0,0))
    strip.show()
    time.sleep(wait_ms/1000.0)

def hi(strip, color, wait_ms=100):
  for i in range(strip.numPixels()):
    coord = ledcoords[i]
    if pattern[coord[1]][19-coord[0]] == '1':
      strip.setPixelColor(i, color)
    else:
      strip.setPixelColor(i, Color(0,0,0))
  strip.show()
  time.sleep(wait_ms/1000.0)

def hi(strip, color, wait_ms=100,offset=0):
  for i in range(strip.numPixels()):
    coord = ledcoords[i]
    if hello[coord[1]][19-coord[0]] == '1':
      strip.setPixelColor(i, color)
    else:
      strip.setPixelColor(i, Color(0,0,0))
  strip.show()
  time.sleep(wait_ms/1000.0)

def scrollText(strip, color, wait_ms=100,offset=0):
  for i in range(strip.numPixels()):
    coord = ledcoords[i]
    if finalText[coord[1]][(19-coord[0]+offset)%len(finalText[0])] == '1':
      strip.setPixelColor(i, color)
    else:
      strip.setPixelColor(i, Color(0,0,0))
  strip.show()
  time.sleep(wait_ms/1000.0)

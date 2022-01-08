import time
from rpi_ws281x import *

from alpha import *
from patterns import Pattern



ledcoords = []

for x in range(0,20):
    for y in range(0,5):
        ledcoords.append([x,(y if x%2 == 0 else 4-y)])
#print(ledcoords)
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

birthday = [LH, LA, LP, LP, LY, LSP, LB, LI, LR, LT, LH, LD, LA, LY,LSP,LSP]
letters = [LA,LB,LC,LD,LE,LF,LG,LH,LI,LJ,LK,LL,LM,LN,LO,LP,LQ,LR,LS,LT,LU,LV,LW,LX,LY,LZ]

def letterArrayToTextArray(letterArray):
  finalText = []
  for i in range(5):
      l = ''
      for t in letterArray:
          l += t[i]
      finalText.append(l)
  finalText.reverse()
  return finalText

def strToTextArray(input):
  letterArray = []
  for l in input:
    if l.isalpha():
      letterArray.append(letters[97 - ord(l.lower())])
    elif l == ' ':
      letterArray.append(LSP)
  return letterArrayToTextArray(letterArray)

finalText = strToTextArray("I Love you")


class Vline(Pattern):

  counter = -1
  counterMax = 20

  def step(self):
      """Wipe color across display a pixel at a time."""

      self.counter = (self.counter+1)%self.counterMax
      global ledcoords
      for i in range(self.strip.numPixels()):
          if ledcoords[i][0] == self.counter:
              self.strip.setPixelColor(i, self.settings.customColor)
          else:
              self.strip.setPixelColor(i, Color(0,0,0))
      self.strip.show()
      time.sleep(self.settings.speed/1000.0)

class Hline(Pattern):

  counter = -1
  counterMax = 5

  def step(self):
    self.counter = (self.counter+1)%self.counterMax
    global ledcoords
    for i in range(self.strip.numPixels()):
        if ledcoords[i][1] == self.counter:
            self.strip.setPixelColor(i, self.settings.customColor)
        else:
            self.strip.setPixelColor(i, Color(0,0,0))
    self.strip.show()
    time.sleep(self.settings.speed/1000.0)



class ScrollText(Pattern):
  counter = -1
  counterMax = 500

  def step(self):
    self.counter = (self.counter+1)%self.counterMax

    for i in range(self.strip.numPixels()):
      coord = ledcoords[i]
      if finalText[coord[1]][(19-coord[0]+self.counter)%len(finalText[0])] == '1':
        self.strip.setPixelColor(i, self.settings.customColor)
      else:
        self.strip.setPixelColor(i, Color(0,0,0))
    self.strip.show()
    time.sleep(self.settings.speed/1000.0)

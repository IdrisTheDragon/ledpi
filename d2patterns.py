import time
from rpi_ws281x import *

from patterns import Pattern

ledcoords = []

for x in range(0,20):
    for y in range(0,5):
        ledcoords.append([x,(y if x%2 == 0 else 4-y)])


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
      if self.settings.customTextArray[coord[1]][(19-coord[0]+self.counter)%len(self.settings.customTextArray[0])] == '1':
        self.strip.setPixelColor(i, self.settings.customColor)
      else:
        self.strip.setPixelColor(i, Color(0,0,0))
    self.strip.show()
    time.sleep(self.settings.speed/1000.0)

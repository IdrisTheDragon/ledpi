import time
from activeSettings import ActiveSettings
from rpi_ws281x import Color, Adafruit_NeoPixel

class Pattern:
    def setup(self,strip,settings:ActiveSettings) -> None:
        self.strip = strip
        self.settings = settings

class SetColor(Pattern):

    def __init__(self,color=Color(0,0,0)) -> None:
        self.color = color
        super().__init__()

    def step(self):
        for i in range(0,self.strip.numPixels()):
            self.strip.setPixelColor(i,self.color)
        self.strip.show()


class ColorWipe(Pattern):

    def __init__(self,customColor=False) -> None:
        self.customColor = customColor
        super().__init__()

    counter = -1

    def setup(self, strip, settings: ActiveSettings) -> None:
        self.counterMax = strip.numPixels()
        return super().setup(strip, settings)

    def step(self):
        """Wipe color across display a pixel at a time."""
        self.counter = (self.counter+1)%self.counterMax
        if self.customColor:
            self.strip.setPixelColor(self.counter,Color(self.settings.customColour[0],self.settings.customColour[1],self.settings.customColour[2]))
        else:
            self.strip.setPixelColor(self.counter, self.settings.color)
        self.strip.show()
        time.sleep(self.settings.speed/1000.0)

class TheaterChase(Pattern):
    """Movie theater light style chaser animation."""

    counter = -1
    counterMax = 3

    def step(self):
        self.counter = (self.counter+1)%self.counterMax
        for i in range(0, self.strip.numPixels(), 3):
            self.strip.setPixelColor(i+self.counter, self.settings.color)
        self.strip.show()
        time.sleep(self.settings.speed/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
            self.strip.setPixelColor(i+self.counter, 0)
        
 
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

class Rainbow(Pattern):

    counter = -1
    counterMax = 256    

    def step(self):
        self.counter = (self.counter+1)%self.counterMax
        """Draw rainbow that fades across all pixels at once."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, wheel((i+self.counter) & 255))
        self.strip.show()
        time.sleep(self.settings.speed/1000.0)

    
class RainbowCycle(Pattern):
    """Draw rainbow that uniformly distributes itself across all pixels."""

    counter = -1
    counterMax = 256

    def step(self):
        self.counter = (self.counter+1)%self.counterMax
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, wheel((int(i * 256 / self.strip.numPixels()) + self.counter) & 255))
        self.strip.show()
        time.sleep(self.settings.speed/1000.0)
 
class TheaterChaseRainbow(Pattern):
    """Draw rainbow that uniformly distributes itself across all pixels."""

    counter = -1
    counterMax = 256
    counter2 = -1
    counter2Max = 3


    def step(self):
        """Rainbow movie theater light style chaser animation."""
        self.counter2 += 1
        if self.counter2 > self.counter2Max:
            self.counter2 = 0
            self.counter = (self.counter+1)%self.counterMax

        for i in range(0, self.strip.numPixels(), 3):
            self.strip.setPixelColor(i+self.counter2, wheel((i+self.counter) % 255))
        self.strip.show()
        time.sleep(self.settings.speed/1000.0)
        for i in range(0, self.strip.numPixels(), 3):
            self.strip.setPixelColor(i+self.counter2, 0)
    
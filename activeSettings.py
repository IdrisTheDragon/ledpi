from rpi_ws281x import Color
from alpha import strToTextArray

class ActiveSettings:
    mode = 3
    prevmode = -1
    customColour = [0,0,0]
    customColor = Color(0,0,0)
    toggleenable = 0
    speed = 100
    customtext = 'Hello World'
    customTextArray = strToTextArray(customtext)

    def parse_update(self,message):
        msg = message.split("\n")
        for m in msg:
            t = m.split(":")
            if t[0] == "mode":
                self.mode = int(t[1])
                print(self.mode)
            elif t[0] == "speed":
                self.speed = int(t[1])
            elif t[0] == 'r':
                self.customColour[0] = int(t[1])
                self.customColor = Color(self.customColour[0],self.customColour[1],self.customColour[2])
            elif t[0] == 'g':
                self.customColour[1] = int(t[1])
                self.customColor = Color(self.customColour[0],self.customColour[1],self.customColour[2])
            elif t[0] == 'b':
                self.customColour[2] = int(t[1])
                self.customColor = Color(self.customColour[0],self.customColour[1],self.customColour[2])
            elif t[0] == "toggleenable":
                self.toggleenable = int(t[1])
                print(self.toggleenable)
            elif t[0] == 'customtext':
                self.customtext = t[1]
                self.customTextArray = strToTextArray(self.customtext)


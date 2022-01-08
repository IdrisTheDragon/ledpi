from rpi_ws281x import Color

class ActiveSettings:
    mode = 3
    prevmode = -1
    colour = 0
    colours = [ Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255), Color(127, 127, 127) ]
    customColour = [0,0,0]
    customColor = Color(0,0,0)
    toggleenable = 0
    speed = 100

    def parse_update(self,message):
        msg = message.split("\n")
        for m in msg:
            t = m.split(":")
            if t[0] == "mode":
                self.mode = int(t[1])
                print(self.mode)
            elif t[0] == "color":
                self.colour = int(t[1])
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


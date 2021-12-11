import time
from rpi_ws281x import *
from patterns import *

import zmq

# LED strip configuration:
LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

mode = 3
colour = 0
colours = [ Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255), Color(127, 127, 127) ]
customColour = [0,0,0]

def parse_update(message):
    global mode
    global colour
    msg = message.split("\n")
    for m in msg:
        t = m.split(":")
        if t[0] == "mode":
            mode = int(t[1])
            print(mode)
        elif t[0] == "color":
            colour = int(t[1])
        elif t[0] == 'r':
            customColour[0] = int(t[1])
        elif t[0] == 'g':
            customColour[1] = int(t[1])
        elif t[0] == 'b':
            customColour[2] = int(t[1])


 
# Main program logic follows:
if __name__ == '__main__':

    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:5555")

 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print ('Press Ctrl-C to quit.')
 
    try:
 
        while True:
            try:
                #print("getting msg")
                message = socket.recv_string(flags=zmq.NOBLOCK)
                print(message)
                parse_update(message)
            except zmq.ZMQError as e:
                #print("no msg",e)
                pass

            if mode == 0:
                colorWipe(strip, colours[colour])
            elif mode == 1:
                theaterChase(strip,colours[colour])
            elif mode == 2:
                rainbow(strip)
            elif mode == 3:
                rainbowCycle(strip,wait_ms=100)
            elif mode == 4:
                theaterChaseRainbow(strip,wait_ms=100)
            elif mode == 5:
                colorWipe(strip, Color(customColour[0],customColour[1],customColour[2]))
 
    except KeyboardInterrupt:
        colorWipe(strip, Color(0,0,0), 10)

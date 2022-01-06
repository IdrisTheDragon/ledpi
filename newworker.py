from typing import Text
from rpi_ws281x import *
from patterns import *
from d2patterns import *
from activeSettings import ActiveSettings

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
 
    settings = ActiveSettings()
    offset = 0
    patterns =[
        SetColor(),
        ColorWipe(),
        TheaterChase(),
        Rainbow(),
        RainbowCycle(),
        TheaterChaseRainbow(),
        ColorWipe(customColor=True)
    ]
    for p in patterns:
        p.setup(strip,settings)

    try:
        while True:
            offset = offset + 1 if offset < 100 else 0
            try:
                #print("getting msg")
                message = socket.recv_string(flags=zmq.NOBLOCK)
                print(message)
                settings.parse_update(message)
            except zmq.ZMQError as e:
                #print("no msg",e)
                pass
            if settings.toggleenable == 1:
                if settings.mode == -1:
                    settings.mode = settings.prevmode
                else:
                    settings.prevmode = settings.mode
                    settings.mode = -1
                settings.toggleenable = 0

            if -1 <= settings.mode <= len(patterns)-2:
                patterns[settings.mode+1].step()
            elif settings.mode == 6:
                vline(strip,Color(settings.customColour[0],settings.customColour[1],settings.customColour[2]),wait_ms=settings.speed,offset=offset)
            elif settings.mode == 7:
                hline(strip,Color(settings.customColour[0],settings.customColour[1],settings.customColour[2]),wait_ms=settings.speed,offset=offset)
            elif settings.mode == 8:
                hi(strip,Color(settings.customColour[0],settings.customColour[1],settings.customColour[2]),wait_ms=settings.speed)
            elif settings.mode == 9:
                scrollText(strip,Color(settings.customColour[0],settings.customColour[1],settings.customColour[2]),wait_ms=settings.speed,offset=offset)
         
 
    except KeyboardInterrupt:
        patterns[0].step()

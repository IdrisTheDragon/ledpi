
import board
import neopixel
import time

import time
import zmq

import random

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://*:5555")

pixels = neopixel.NeoPixel(board.D12, 100, auto_write=False)

mode=0
colour = 345

red = (50,0,0)
green = (0,50,0)
blue = (0,0,50)
colours = [red,green,blue]


def solid_colour(colour):
    for i in range(0,len(pixels)-1):
        pixels[i] = colour
    pixels.show()

def parse_update(message):
    global mode
    msg = message.split("\n")
    for m in msg:
        t = m.split(":")
        if t[0] == "mode":
            mode = int(t[1])
            print(mode)
        elif t[0] == "color":
            colour = int(t[1])

while True:
    #  Wait for next request from client
    try:
        print("getting msg")
        message = socket.recv_string(flags=zmq.NOBLOCK)
        print(message)
        parse_update(message)
    except zmq.ZMQError as e:
        print("no msg",e)
        pass

    if mode == 0:
        solid_colour(colour)
    else:
        c = random.choice(colours)
        solid_colour(c)

    #  Do some 'work'
    print("resting")
    time.sleep(1)
    print("awake")

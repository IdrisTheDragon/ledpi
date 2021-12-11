#!/usr/bin/env python

# make sure to use eventlet and call eventlet.monkey_patch()
import eventlet
eventlet.monkey_patch()

import random

import board
import neopixel

from flask import Flask, render_template, request, g, session, make_response, current_app, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# make sure to set the async_mode as 'eventlet'
socketio = SocketIO(app, async_mode='eventlet')

worker = None

red = (50,0,0)
green = (0,50,0)
blue = (0,0,50)
colours = [red,green,blue]

class Worker(object):

    worker = False
    switch = False
    unit_of_work = 0
    speed = 0.2
    mode = 0
    r=50
    g=0
    b=0

    def __init__(self, socketio):
        """
        assign socketio object to emit
        """
        self.socketio = socketio
        self.pixels = neopixel.NeoPixel(board.D18, 100)

    def do_work(self):
        """
        do work and emit message
        """
        # worker already running
        if self.worker:
           return
        self.worker = True
        self.switch = True
        while self.worker:
          if self.switch:
            self.unit_of_work += 1
            # must call emit from the socket io
            # must specify the namespace
            # self.socketio.emit("update", {"msg": self.unit_of_work}, namespace="/work")
            if self.mode == 0:
               self.pixels[self.unit_of_work] = (self.r,self.g,self.b)
            elif self.mode == 1:
               c = random.choice(colours)
               for x in range(self.unit_of_work,(self.unit_of_work+5)):
                 if x < 100:
                   self.pixels[x] = c
            else:
               self.pixels[self.unit_of_work] = 0
            # important to use eventlet's sleep method
            if self.unit_of_work == 99:
              self.unit_of_work = 0
          eventlet.sleep(self.speed)
    def update_pattern(self,data):
        self.r = data['r']
        self.g = data['g']
        self.b = data['b']
        self.mode = int(data['mode'])

    def stop(self):
        """
        stop the loop
        """
        self.switch = False


    def start(self):
        self.switch = True

@app.route('/')
def index():
    """
    renders demo.html
    """
    return render_template('demo.html')

@app.before_first_request
def start_worker():
    global worker
    worker = Worker(socketio)
    socketio.start_background_task(target=worker.do_work)
    print("execute before server starts")


@socketio.on('connect', namespace='/work')
def connect():
    """
    connect
    """
    emit("re_connect", {"msg": "connected"})


@socketio.on('start', namespace='/work')
def start_work():
    """
    trigger background thread
    """
    global worker
    worker.start()
    print("start once")
    emit("update", {"msg": "starting worker"})


@socketio.on('stop', namespace='/work')
def stop_work():
    """
    trigger background thread
    """
    global worker
    worker.stop()
    print("stop once")
    emit("update", {"msg": "worker has been stoppped"})

@socketio.on('update', namespace='/work')
def update_pattern(data):
    global worker
    worker.update_pattern(data)
    print('updated with', data)
    emit("update", {"msg":"updated data"})


if __name__ == '__main__':
    """
    launch server
    """
    #worker = Worker(socketio)
    #socketio.start_background_task(target=worker.do_work)
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

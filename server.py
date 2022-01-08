#!/usr/bin/env python

import zmq

from flask import Flask, render_template, request, g, session, make_response, current_app, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# make sure to set the async_mode as 'eventlet'
socketio = SocketIO(app, async_mode='eventlet')

zmqContext = zmq.Context()
zmqSocket = zmqContext.socket(zmq.PUSH)
zmqSocket.connect("tcp://localhost:5555")

settingsdata = {'nodata':True}


@app.route('/')
def index():
    """
    renders demo.html
    """
    return render_template('demo.html')

@app.route('/leds/toggle')
def toggleenable():
    """
    renders demo.html
    """
    zmqSocket.send_string("toggleenable:1")


@socketio.on('connect', namespace='/work')
def connect():
    """
    connect
    """
    emit("re_connect", {"msg": "connected"})

@socketio.on('get_settings', namespace='/work')
def get_settings(data):
    emit("update", {"msg":settingsdata})
    emit("settings", {"msg":settingsdata}, broadcast=True)

@socketio.on('update', namespace='/work')
def update_pattern(data):
    # data['r']
    global settingsdata
    zmqSocket.send_string(f"mode:{data['mode']}\nspeed:{data['speed']}\nr:{data['r']}\ng:{data['g']}\nb:{data['b']}\ncustomtext:{data['customtext']}")
    print('updated with', data)
    settingsdata = data
    settingsdata['nodata'] = False
    emit("update", {"msg":data})
    emit("settings", {"msg":data}, broadcast=True)


if __name__ == '__main__':
    """
    launch server
    """
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

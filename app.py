from flask import Flask, render_template
from flask_socketio import SocketIO

from flask import request
from actions import *
from utils import *
from sessiondata import *
from pymongo import MongoClient

app = Flask(__name__)
socketio = SocketIO(app)
mongo_client = MongoClient("mongodb://localhost:27017")

sid_data = {}


# When a new connection occurs
def on_new_connection():
    request_sid = request.sid
    sid_data[request_sid] = SessionData()

# When a connection closes
def on_connection_close():
    request_sid = request.sid
    if request_sid in sid_data:
        del sid_data[request_sid]

startFile = 'welcome'


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    
    socketio.emit('initPage',  [
        {'minWidth': 0, 'x': 40, 'y': 25},
        {'minWidth': 640, 'x': 80, 'y': 50},
        {'minWidth': 960, 'x': 120, 'y': 80}
    ], room=request.sid)



def oneliners():
    print("oneliners")
    
    
@socketio.on('onload')
def onload(data):
    on_new_connection()
    init_utils_listeners(socketio, mongo_client, sid_data)
    init_action_listeners(socketio, mongo_client, sid_data)
    x = data.get('x')
    sid_data[request.sid].setXWidth(x)
    y = data.get('y')
    sid_data[request.sid].setYHeight(y)
    data2 = { 'filename' : startFile+'-'+str(x)+'x'+str(y), 'x' : x, 'y': y}
    show_file(data2)
    goto_next_line()
    output("Please enter your name: ", 3, 0)
    ask(40, usernameCallback)


@socketio.on('disconnect')
def disconnect(data):
    on_connection_close()


if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=5000, debug=True)
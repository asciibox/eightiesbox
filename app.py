from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import bson.binary
from flask_socketio import SocketIO

from flask import jsonify
from flask import request
from actions import *
from utils import *
from sessiondata import *
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from menubox import *
from ansieditor import *
import time

app = Flask(__name__)
socketio = SocketIO(app)
MAX_FILE_SIZE = 1024 * 1024  # 1MB in bytes
server_available = True
try:
    mongo_client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    mongo_client.admin.command('ping')  # This should force a connection attempt
except ServerSelectionTimeoutError:
    print("Server not available")
    server_available = False
except ConnectionFailure:
    print("Failed to connect to server")
    server_available = False

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

@socketio.on('upload_finished')
def upload_finished():
    print("UPLOAD FINISHED")  
    


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
    if server_available == False:
        output("* Database connection could not get established *", 1,0)
        print(server_available)
        time.sleep(3)
    sid_data[request.sid].setANSIEditor(ANSIEditor(sid_data[request.sid], output, ask, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file_content, emit_upload))
    #data2 = { 'filename' : startFile+'-'+str(x)+'x'+str(y), 'x' : x, 'y': y}
    #show_file(data2, emit_current_string)
    #goto_next_line()
    #output("Please enter your name: ", 3, 0)
    #ask(40, usernameCallback)

@socketio.on('disconnect')
def disconnect(data):
    on_connection_close()

db = mongo_client["bbs"]  # You can replace "mydatabase" with the name of your database
uploads_collection = db["uploads"]

ALLOWED_EXTENSIONS = {'ans'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if server_available:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            file_data = file.read()

            # Check file size
            if len(file_data) > MAX_FILE_SIZE:
                return jsonify({"error": "File size exceeds 1MB"}), 400
            
            # Save file data and filename to MongoDB
            new_file = {
                "filename": file.filename,
                "file_data": bson.binary.Binary(file_data)
            }
            uploads_collection.insert_one(new_file)
            return jsonify({"success": f"File {file.filename} uploaded successfully"}), 200
        else:
            return jsonify({"error": "Wrong file extension (.ANS only)"}), 400
    else:
        return jsonify({"error": "Database server not available"}), 500
    

if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=5000, debug=True)
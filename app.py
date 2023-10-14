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
import base64

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

        data = request.json
        base64_string = data.get('file_data')
        filename = data.get('filename')  # Retrieve the filename here

        if not base64_string or not filename:
            return jsonify({"error": "Missing file data or filename"}), 400

        # Decode the Base64 string
        file_data = base64.b64decode(base64_string)

        file_data = convert_current_string(file_data)

        file_data = file_data.decode('cp1252')

        # Check file size
        if len(file_data) > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 1MB"}), 400
        
        # Save file data and filename to MongoDB
        new_file = {
            "filename": filename,
            "file_data": bson.binary.Binary(bytes(file_data, 'cp1252'))
        }

        #with open('output_app.ans', "w", encoding='cp1252') as ansi_file:
        #
        #     ansi_file.write(file_data)

        uploads_collection.insert_one(new_file)
        return jsonify({"success": f"File {filename} uploaded successfully"}), 200
      
    
def convert_current_string(currentBytes):

    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]

    if currentBytes:
        ascii_codes = [b for b in currentBytes]
        print(ascii_codes)
        mapped_ascii_codes = [map_value(code, list2, list1) for code in ascii_codes]

        # Convert the mapped ASCII codes back into a byte array
        new_bytes = bytes(mapped_ascii_codes)

        return new_bytes
    return bytes([])  # Return an empty byte array if there's no data


if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=5000, debug=True)
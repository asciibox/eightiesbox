from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import bson.binary
from flask_socketio import SocketIO

from flask import jsonify
from flask import request
from utils import *
from sessiondata import *
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from menubox import *
from ansieditor import *
from sauce import Sauce
import time
import base64
from f10actionhandler import F10ActionHandler
import asyncio
from threading import Timer
app = Flask(__name__)
socketio = SocketIO(app, logger=False, engineio_logger=False)
from flask import jsonify, request
from google.cloud import storage, pubsub_v1
from google.oauth2 import service_account
import google.auth.iam
from google.auth.transport.requests import Request
import uuid
from datetime import date, timedelta
import re

from uploadeditor import UploadEditor


MAX_FILE_SIZE = 1024 * 102  # 1MB in bytes
util = None
try:
    mongo_client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    # mongo_client.admin.command('ping')  # This should force a connection attempt
except ServerSelectionTimeoutError:
    print("Server not available")
    server_available = False
except ConnectionFailure:
    print("Failed to connect to server")
    server_available = False

sid_data = {}
list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]
menu_structure = {
            'Goto & Gosub': ['Goto new menu', 'Gosub new menu', 'Return from gosub'],
            'Message base': ['Read message', 'Write message', 'Area change'],
            'File base': ['Download files', 'Upload files', 'List visible files', 'Select file area', 'Comment uploaded files', 'List invisible files [admin]', 'Download invisible files [admin]', 'Delete files [admin]'],
            'Other options': ['Change profile'],
            'Login/Logout': ['Logout', 'Show oneliners'],
            'Multiline options': ['Users online', 'Chat between nodes', 'Add conference', 'Join conference', 'Delete conference', 'Watch other lines'],
            'Text': ['Display ANS / ASC', 'Display ANS / ASC and wait', 'Display text from Data and wait', 'Modify start ANSI [admin]'],
            'BBS List': ['Long list display', 'Short list display', 'Add BBS'],
            'MOD Editor': ['Start MOD editor in textmode', 'Start MOD editor in graphic mode'],
            'Administration': ['Setup message areas', 'Setup file base', 'User editor', 'ANSI Editor', 'Menu editor', 'Edit uploaded files', 'Delete file', 'Group editor']
        }


target_values = [223, 176, 177, 178, 220, 191, 250]
for i, value in enumerate(list2):
    if value in target_values:
        list2[i] = -1
    
#list1.append(220)
#list2.append(223)

# When a new connection occurs
def on_new_connection():
    global sid_data
    request_sid = request.sid
    sid_data[request_sid] = SessionData()
    global util
    sid_data[request_sid].util = Utils(socketio, mongo_client, list1, list2, sid_data, Sauce, request_sid, menu_structure)
    

# When a connection closes
def on_connection_close():
    global sid_data
    request_sid = request.sid
    if request_sid in sid_data:
        del sid_data[request_sid]



@socketio.on('custom_disconnect')
def custom_disconnect(data):
    on_connection_close()


@socketio.on('upload_finished')
def upload_finished(data):
    siddata = sid_data[request.sid]
    siddata.current_action = 'wait_for_uploadeditor'
    siddata.setUploadEditor(UploadEditor(siddata.util)) 
    siddata.upload_editor.start()


    

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    
    on_new_connection()
    request_sid = request.sid
    Timer(1, sid_data[request_sid].util.update_status_bar_periodically).start()
    socketio.emit('initPage',  [
        {'minWidth': 0, 'x': 36, 'y': 20},
        {'minWidth': 640, 'x': 80, 'y': 50},
        {'minWidth': 1280, 'x': 120, 'y': 60}
    ], room=request.sid)

@socketio.on('onload')
def onload(data):
    #login(data)
    x = data.get('x')
    sid_data[request.sid].setXWidth(x)
    y = data.get('y')
    sid_data[request.sid].setYHeight(y)
    sid_data[request.sid].util.choose_bbs(data)
    return

@socketio.on('pointerdown')
def pointerdown(data):
    #login(data)
    global sid_data
    siddata = sid_data[request.sid]
    x = data.get('x')
    y = data.get('y')
    if (siddata.current_action=='wait_for_profile_renderer'):
        siddata.profile_renderer.handle_click(x, y)
    return




@socketio.on('disconnect')
def disconnect():
    on_connection_close()

db = mongo_client["bbs"]  # You can replace "mydatabase" with the name of your database
uploads_collection = db["uploads_ansi"]

ALLOWED_EXTENSIONS = {'ans'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    global sid_data
    
    data = request.json
    base64_string = data.get('file_data')
    filename = data.get('filename')  # Retrieve the filename here
    chosen_bbs = data.get('chosen_bbs')

    if not base64_string or not filename or not chosen_bbs:
        return jsonify({"error": "Missing file data or filename or no chosen_bbs"}), 400

    # Decode the Base64 string
    
    # Check file size
    if len(base64_string) > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 100KB"}), 400
    
    filename = generate_unique_filename(filename, chosen_bbs)

    # Save file data and filename to MongoDB
    new_file = {
        "filename": filename,
        "file_data": base64_string,
        "chosen_bbs" : chosen_bbs
    }

    #with open('output_app.ans', "w", encoding='cp1252') as ansi_file:
    #
    #     ansi_file.write(file_data)

    uploads_collection.insert_one(new_file)
    return jsonify({"success": f"File {filename} uploaded successfully"}), 200

def generate_unique_filename(filename, chosen_bbs):
    global sid_data
    base, ext = os.path.splitext(filename)
    
    # If the filename (including its extension) is longer than 11 characters, truncate it.
    if len(filename) > 11:
        base = base[:11-len(ext)]  # Adjust so that the total length remains 11 characters
    
    original_base = base
    counter = 1

    # Check if file exists and modify the filename accordingly
    while uploads_collection.find_one({"filename": base + ext, "chosen_bbs" : chosen_bbs}):
        # Adjust the base name to accommodate the counter
        base = original_base[:11-len(ext)-len(str(counter))] + str(counter)
        counter += 1

    return base + ext
  
@socketio.on('download_close')
def download_close(data):
    global sid_data
    siddata = sid_data[request.sid]
    siddata.menu.return_from_gosub()
    siddata.setCurrentAction("wait_for_menu")


@socketio.on('input_keypress')
def handle_keypress(data):
    global sid_data
    siddata = sid_data[request.sid]

    shiftPressed=data['shiftPressed']
    ctrlKeyPressed = data['ctrlKeyPressed']
    altgrPressed = data['altgrPressed']
    
    # Create an array (list in Python) with these values
    keyStatusArray = [shiftPressed, ctrlKeyPressed, altgrPressed]

    key = data['key']
    if key == 'F10':
       siddata.setF10ActionHandler(F10ActionHandler(siddata.util))
       siddata.f10actionhandler.handle_F10()
       return
    if key == 'F12':
        siddata.util.emit_toggle_keyboard()
        return
    elif siddata.current_action == "in_chat" and siddata.chat_partner:
        partner_sid_data = siddata.chat_partner
        partner_util = partner_sid_data.util  # Assume util is accessible from sid_data

        if key == 'Escape':
            siddata.current_action = siddata.previous_action
            siddata.copy_action = False
            
            siddata.util.clear_screen()
            basicANSI = BasicANSI(siddata.util)
            basicANSI.display_editor(siddata.copy_color_array, siddata.copy_color_bgarray, siddata.copy_input_values, None) # None: just restore the original ANSI, no matter what menu points
            siddata.copy_action = True

            partner_sid_data.current_action = partner_sid_data.previous_action

            partner_sid_data.copy_action = False

            partner_sid_data.util.clear_screen()
            basicANSI = BasicANSI(partner_sid_data.util)
            basicANSI.setYOffsetOnDraw(-1)
            basicANSI.display_editor(partner_sid_data.copy_color_array, partner_sid_data.copy_color_bgarray, partner_sid_data.copy_input_values, None) # None: just restore the original ANSI, no matter what menu points
            partner_sid_data.copy_action = True
            if siddata.chat_callback != None:
                siddata.chat_callback()
                siddata.chat_callback = None

            if partner_sid_data.chat_callback != None:
                partner_sid_data.chat_callback()
                partner_sid_data.chat_callback = None

            return


        if key == 'Enter':
            siddata.cursorY += 1
            siddata.cursorX = 0
            siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)
            siddata.startX = siddata.cursorX
            siddata.startY = siddata.cursorY
            
            partner_sid_data.cursorY += 1
            partner_sid_data.cursorX = 0
            partner_util.emit_gotoXY(partner_sid_data.cursorX, partner_sid_data.cursorY)
            partner_sid_data.startX = partner_sid_data.cursorX
            partner_sid_data.startY = partner_sid_data.cursorY
            
            
        if key == 'Backspace':
            siddata.startX = siddata.startX -1
            siddata.util.output(" ", 6,0)
            siddata.cursorX = siddata.cursorX - 2
            siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)
            siddata.startX = siddata.startX -1
            
            partner_sid_data.startX = partner_sid_data.startX - 1
            partner_util.output(" ", 6,0)
            partner_sid_data.cursorX = partner_sid_data.cursorX - 2
            partner_util.emit_gotoXY(partner_sid_data.cursorX, partner_sid_data.cursorY)
            partner_sid_data.startX = partner_sid_data.startX - 1
            
        if len(key) == 1:
            # Update partner's screen
            partner_util.output(key, 14, 0)
            # Update your own screen
            siddata.util.output(key, 11, 0)
        return
    elif siddata.current_action == "wait_for_f10_action":
        key = data['key']
        siddata.f10actionhandler.handle_key(key)
        return
    elif siddata.current_action == "wait_for_multi_line_chat":
        siddata.multi_line_chat.stop_waiting_for_request() 
        return
    elif siddata.current_action == "wait_for_userpicker":
        key = data['key']
        siddata.user_picker.handle_key(key)
        return
    elif siddata.current_action == "wait_for_bbschooser":
        key = data['key']
        siddata.bbschooser.handle_key(key)
        return
    elif siddata.current_action == "wait_for_watching_escape":
        key = data['key']
        if key == 'Escape':
            siddata.watchlines.stop_watching()
    elif siddata.current_action == "wait_for_menu":
        key = data['key']
        siddata.menu.handle_key(key)
        return
    elif siddata.current_action == "wait_for_group_chooser":
        key = data['key']
        siddata.group_chooser.handle_key(key)
        return
    elif siddata.current_action == "wait_for_layered_menu":
        key = data['key']
        if siddata.menu_box.in_sub_menu:  # in_sub_menu is a new attribute to check if you're in a sub-menu
            if key == 'ArrowUp': 
                siddata.menu_box.sub_menu_arrow_up()
                
            elif key == 'ArrowDown':
                siddata.menu_box.sub_menu_arrow_down()
                
            elif key == 'Enter':
                siddata.menu_box.select_sub_menu_item()
                siddata.menu_box.hide_menu()
                siddata.menu_box.in_sub_menu = False
                return
                
            elif key == 'Escape':
                siddata.menu_box.hide_sub_menu()
                siddata.menu_box.in_sub_menu = False
                return
        else:
            if key == 'ArrowLeft':
                siddata.menu_box.main_arrow_left()
                
            elif key == 'ArrowRight':
                siddata.menu_box.main_arrow_right()
                
            elif key == 'ArrowUp':
                siddata.menu_box.main_arrow_up()
                
            elif key == 'ArrowDown':
                siddata.menu_box.main_arrow_down()
                
            elif key == 'Enter':
                selected_main_menu = siddata.menu_box.get_selected_main_menu()
                siddata.menu_box.show_sub_menu()
                siddata.menu_box.in_sub_menu = True
                return
                
            elif key == 'Escape':
                siddata.menu_box.hide_menu()
                return

    if siddata.current_action == "wait_for_menubox":
        key = data['key']
        
        if key == 'ArrowLeft':
            siddata.menu_box.arrow_left()
            
        elif key == 'ArrowRight':
            siddata.menu_box.arrow_right()
            
        elif key == 'ArrowUp':
            siddata.menu_box.arrow_up()
            
        elif key == 'ArrowDown':
            siddata.menu_box.arrow_down()
            
        elif key == 'Enter':
            siddata.menu_box.edit_field()
            return
        
        elif key == 'Delete':
            siddata.menu_box.delete_current_row()

        elif key == 'F1':
            siddata.menu_box.draw_all_rows_and_output_json()

        elif key == 'Escape':
            sub_menus = {
                'File': ['Load menu', 'Save menu', 'New menu', 'Delete menu'],
                'Edit': ['Edit text', 'Simulate text', 'Clear text', 'View text', 'Leave menu bar'],
            }
            
            siddata.setMenuBar(MenuBarMenuEditor(sub_menus, siddata.util))
            return
        
        return

    if siddata.current_action == "wait_for_menubar_menueditor" or siddata.current_action == "wait_for_menubar_ansieditor" or siddata.current_action == "wait_for_menubar_menutexteditor" or siddata.current_action == "wait_for_menubar_messageeditor":
        key = data['key']
        
        if key == 'ArrowLeft':
            siddata.menu_bar.arrow_left()
            
        elif key == 'ArrowRight':
            siddata.menu_bar.arrow_right()
            
        elif key == 'ArrowUp':
            siddata.menu_bar.arrow_up()
            
        elif key == 'ArrowDown':
            siddata.menu_bar.arrow_down()
            
        elif key == 'Enter':
            siddata.menu_bar.choose_field()
            return

        elif key == 'Escape':
            siddata.menu_bar.leave_menu_bar()
            return
        
        return
    if (siddata.current_action == "wait_for_yes_no"):
        key = data['key']
        if key=='Y' or key == 'y' or key == 'n' or key == 'N':
            siddata.callback(key)
        return
    elif (siddata.current_action == "wait_for_any_button"):
        siddata.callback()
        return
    elif (siddata.current_action == "wait_for_menutexteditor"):
        siddata.menutexteditor.handle_key(data['key'], [False, False, False])
        return
    elif (siddata.current_action == "wait_for_ansieditor"):
        siddata.ansi_editor.handle_key(data['key'], keyStatusArray)
        return
    elif (siddata.current_action == "wait_for_uploadeditor"):
        siddata.upload_editor.handle_key(data['key'], [False, False, False])
        return
    elif (siddata.current_action == "wait_for_editfile"):
        siddata.edit_file.handle_key(data['key'], [False, False, False])
        return
    elif (siddata.current_action == "wait_for_messageeditor"):
        siddata.message_editor.handle_key(data['key'], [False, False, False])
        return
    elif (siddata.current_action == "wait_for_input") or (siddata.current_action == "wait_for_profile_renderer"):
        key = data['key']


        if key == 'Tab' and siddata.current_action == "wait_for_profile_renderer":
            siddata.callback(siddata.localinput)
            if shiftPressed==False:
                siddata.profile_renderer.focus_next_element()
            else:
                siddata.profile_renderer.focus_previous_element()
            return
        elif key == 'Enter' and siddata.current_action == "wait_for_profile_renderer":
            siddata.profile_renderer.enter()
            return
        elif key == 'ArrowDown' and siddata.current_action == "wait_for_profile_renderer":
            siddata.profile_renderer.focus_next_element()
            return
        elif key == 'ArrowUp' and siddata.current_action == "wait_for_profile_renderer":
            siddata.profile_renderer.focus_previous_element()
            return
        elif key == "ä":
            # Handle ä
            siddata.util.keydown(chr(132))
            return
        elif key == "ö":
            # Handle ö
            siddata.util.keydown(chr(148))
            return
        elif key == "ü":
            # Handle ü
            siddata.util.keydown(chr(129))
            return
        elif key == "ß":
            # Handle ß
            siddata.util.keydown(chr(223))
            return
        elif key == "Ä":
            # Handle ß
            siddata.util.keydown(chr(142))
            return
        elif key == "Ö":
            # Handle ß
            siddata.util.keydown(chr(153))
            return
        elif key == "Ü":
            # Handle ß
            siddata.util.keydown(chr(154))
            return

        
        if key == 'Alt' or key=='Escape' or key =='AltGraph' or key =='Shift' or key == 'Control' or key == 'Dead' or key == 'ArrowDown' or key =='ArrowUp' or key =='CapsLock' or key=='Tab':
            return
            
        if key == 'Enter':
            siddata.callback(siddata.localinput)
            return

        if key == 'Insert':
            siddata.setInsert(not siddata.insert)
            return

        # Handle Delete
        if key == 'Delete':
            if siddata.currentPos < len(siddata.localinput):
                siddata.setLocalInput(siddata.localinput[:siddata.currentPos] + siddata.localinput[siddata.currentPos+1:])
                visible_str = siddata.localinput[siddata.view_start:siddata.view_start + siddata.maxLength]
                myoutput = visible_str
                if siddata.inputType=='password':
                    myoutput = "*"*len(visible_str)
                siddata.util.emit_current_string(myoutput+" ", 14, 4, False, siddata.startX, siddata.startY)
                siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)

        # Handle cursor left
        elif key == 'ArrowLeft' and siddata.currentPos > 0:
            # Scroll by one if cursor reaches the start of the input field
            if siddata.currentPos - siddata.view_start == 0 and siddata.view_start > 0:
                siddata.view_start -= 1
                visible_str = siddata.localinput[siddata.view_start:siddata.view_start + siddata.maxLength]
                myoutput = visible_str
                if siddata.inputType == 'password':
                    myoutput = "*"*len(visible_str)
                siddata.util.emit_current_string(myoutput, 14, 4, False, siddata.startX, siddata.startY)
                siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)  # Adjust cursor to the same position since content has shifted
            else:
                siddata.util.emit_gotoXY(siddata.cursorX - 1, siddata.cursorY)
            siddata.setCurrentPos(siddata.currentPos - 1)

        # Handle cursor right
        elif key == 'ArrowRight' and siddata.currentPos < len(siddata.localinput):
            if (siddata.currentPos >= len(siddata.localinput)-1):
                siddata.util.emit_current_string(" ", 14, 4, False, siddata.startX+siddata.maxLength-1, siddata.startY)
            if siddata.currentPos - siddata.view_start == siddata.maxLength - 1:
                siddata.view_start += 1
                visible_str = siddata.localinput[siddata.view_start:siddata.view_start + siddata.maxLength]
                myoutput = visible_str
                if siddata.inputType=='password':
                    myoutput = "*"*len(visible_str)
                siddata.util.emit_current_string(myoutput, 14, 4, False, siddata.startX, siddata.startY)
                siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)  # Adjust cursor to the same position since content has shifted
            else:
                siddata.util.emit_gotoXY(siddata.cursorX + 1, siddata.cursorY)

            siddata.setCurrentPos(siddata.currentPos + 1)

        # Handle backspace
        elif key == 'Backspace' and siddata.currentPos > 0:
            siddata.setLocalInput(siddata.localinput[:siddata.currentPos-1] + siddata.localinput[siddata.currentPos:])

            # Decrease view_start if it's greater than 0
            if siddata.view_start > 0:
                siddata.view_start -= 1

            visible_str = siddata.localinput[siddata.view_start:siddata.view_start + siddata.maxLength]
            myoutput = visible_str
            if siddata.inputType == 'password':
                myoutput = "*"*len(visible_str)
            
            # Emit the current string with an extra space at the end to overwrite the previous character
            siddata.util.emit_current_string(myoutput + " ", 14, 4, False, siddata.startX, siddata.startY)

            # Move the cursor back by one position
            if siddata.view_start == 0:
                siddata.util.emit_gotoXY(siddata.cursorX-1, siddata.cursorY)
            else:
                siddata.util.emit_gotoXY(siddata.cursorX, siddata.cursorY)
            siddata.setCurrentPos(siddata.currentPos - 1)



        # Handle character input
        elif len(key) == 1:
            siddata.util.keydown(key)
            



# Initialize Google Cloud
storage_client = storage.Client()
bucket = storage_client.get_bucket('eightiesbox')

# Initialize Pub/Sub client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path('animated-moon-403620', 'projects/animated-moon-403620/subscriptions/bbs-file-upload-notification')

#def callback(message):
#    print(f"Received message: {message}")
#    message.ack()
#    
#    # Update MongoDB
#    file_name = message.attributes.get('objectId')
#    collection.insert_one({"file_name": file_name})

@app.route('/getSignedUrl', methods=['GET'])

def get_signed_url():
    global mongo_client
    bucket_name = "eightiesbox"
     # Split the filename into name and extension
    object_name = request.args.get('filename')
    file_name, file_extension = os.path.splitext(object_name)

    chosen_bbs = request.args.get('chosen_bbs')
    current_file_area = request.args.get('current_file_area')

    db = mongo_client['bbs']
    upload_token_collection = db['upload_token']

    upload_token = request.args.get('uploadToken')

    # Query the 'upload_token_collection' for the document with the matching 'token'
    token_document = upload_token_collection.find_one({"token": upload_token})

    # Initialize an empty string for user_id
    user_id_str = "nouserid"

    # Check if the document was found
    if token_document:
        # Extract the 'user_id' from the document and convert it to a string
        user_id_str = str(token_document.get('user_id', ''))

    # Append the UUID before the extension
    current_time_millis = time.time_ns() // 1_000_000
    
    new_object_name = f"{chosen_bbs}/{user_id_str}/{current_file_area}_{file_name}_{current_time_millis}{file_extension}"
    print(new_object_name)
    file_size = request.args.get('filesize')
    
    # Load the service account credentials
    credentials = service_account.Credentials.from_service_account_file(
    "animated-moon-403620-a91bc66243a8.json",
    scopes=["https://www.googleapis.com/auth/iam", "https://www.googleapis.com/auth/cloud-platform"]
    )
    googleAccessId = credentials.service_account_email
    
    # The URL will be valid for 10 minutes
    expiration = int(time.time()) + 600

    # Create the policy document
    policy_document = {
        "expiration": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(expiration)),
        "conditions": [
            {"bucket": bucket_name},
            {"key": new_object_name},
            ["content-length-range", 1, 10000]
        ]
    }
    
    # Encode the policy document to base64
    policy = base64.b64encode(json.dumps(policy_document).encode('utf-8')).decode('utf-8')
    
    # Create a signing key for the policy document
    signer = google.auth.iam.Signer(
        Request(),
        credentials,
        googleAccessId
    )    
    # Generate the signature
    signature_bytes = signer.sign(policy.encode('utf-8'))
    signature = base64.b64encode(signature_bytes).decode('utf-8')
    
    uploads_collection = db['upload_requests']

    # Now, create the document to insert
    upload_document = {
        "chosen_bbs" : chosen_bbs,
        "area_id" : current_file_area.split("-")[0],
        "user_id": user_id_str.split("_")[0],
        "filename": file_name+file_extension,
        "current_time_millis" : current_time_millis,
        "timestamp" : int(time.time()),
        "uploadID": request.args.get('uploadID'),
        "new_object_name" : new_object_name
    }

    # Insert the document into the collection
    result = uploads_collection.insert_one(upload_document)

    # 'result' will contain information about the insertion
    if result.acknowledged:
        print("Upload inserted successfully.")
    else:
        print("Failed to insert upload.")

    # Return the generated values
    return jsonify({
        "policy": policy,
        "signature": signature,
        "GoogleAccessId": googleAccessId,
        "bucket": bucket_name,
        "key": new_object_name,
        "contentType": "image/png",
        "Access-Control-Allow-Origin": "*",
        "content-length-range": "1,100000"
    })

@app.route('/checkUpload', methods=['GET'])

def check_upload_and_process():
    global mongo_client
    upload_id = request.args.get('uploadID')
    db = mongo_client['bbs']
    uploads_collection = db['upload_requests']

    # Retrieve the specific document
    specific_document = uploads_collection.find_one({"uploadID": upload_id})

    if specific_document:
        print("Document found:", specific_document)
        file_path = specific_document['new_object_name']

        storage_client = storage.Client()

        # Define the "processed" bucket
        processed_bucket_name = "eightiesbox_uploaded"
        processed_bucket = storage_client.bucket(processed_bucket_name)

        # Try with today's, previous and next date
        for offset in (0, -1, 1):
            check_date = date.today() + timedelta(days=offset)
            status = check_upload_date(check_date.strftime('%d-%m-%Y'), processed_bucket, file_path, processed_bucket_name, specific_document)
            if status:
                break

        return jsonify({'success': status})
    else:
        print("No document found with the provided uploadID")
    return jsonify({'success': False})



def check_upload_date(today, processed_bucket, file_path, processed_bucket_name, specific_document):
    chosen_bbs = request.args.get('chosen_bbs', default=None, type=str)
    status = False
    # Check if there's a directory for the current day in the "processed" bucket
    daily_directory = None
    blobs = processed_bucket.list_blobs(prefix=today)
    for b in blobs:
        if b.name.startswith(today) and '/' in b.name:
            daily_directory = b.name.split('/')[0]
            break

    # If no directory for today was found, create one with a new UUID
    if not daily_directory:
        daily_uuid = str(uuid.uuid4())
        daily_directory = f"{today}_{daily_uuid}"

    # Define the pattern for the timestamp in the filename
    timestamp_pattern = re.compile(r'_(\d{13})(?=\.)') 

    # Extract the base directory name and the original filename
    base_directory_name = os.path.dirname(file_path).split('/')[-1]
    original_filename = os.path.basename(file_path)

    # Search for the timestamp in the original filename
    timestamp_match = timestamp_pattern.search(original_filename)
    if timestamp_match:
        # Extract the timestamp
        timestamp = timestamp_match.group(0)
        timestamp = timestamp[1:]
        # Remove the timestamp from the original filename
        clean_filename = timestamp_pattern.sub('', original_filename)

        # New regex pattern to extract the category string
        category_pattern = re.compile(r'^[a-fA-F0-9]{24}-(.{20})')
        category_match = category_pattern.search(clean_filename)

        # Initialize an empty category string
        category_string = 'default_no_category'

        if category_match:
            # Extract the category string
            category_string = category_match.group(1)
            # Remove the category string from the clean_filename
            clean_filename = category_pattern.sub('', clean_filename)
            clean_filename = clean_filename[1:]
        else:
            print(f"Category not found in {clean_filename}")

        # Extract the file extension
        file_extension = os.path.splitext(clean_filename)[1]  # This will give you '.png' from your example

        # Ensure we only get the first 20 characters of the filename without the extension
        filename_prefix = os.path.splitext(clean_filename[:20])[0]

        # Construct the new file path
        new_file_path = f"{daily_directory}/{category_string}/{base_directory_name}/{timestamp}_{filename_prefix}{file_extension}/{clean_filename}"

    else:
        # If no timestamp is found, we keep the original structure
        new_file_path = f"{daily_directory}/{base_directory_name}/{original_filename}"
    incoming_bucket = storage_client.bucket(processed_bucket_name)
    blob = incoming_bucket.blob(new_file_path)

    # Check if the file exists in the incoming bucket
    if blob.exists():
        status = True
        # Get the file size
        blob.reload()  # Reload the blob properties
        file_size = blob.size

        files_collection = db['files']
        to_be_edited_collection = db['to_be_edited']

        # Insert into 'files' collection
        file_document = {
            "filename": clean_filename,
            "file_size": file_size,
            "area_id": specific_document['area_id'],
            "uploaded_by_user_id" : specific_document['user_id'],
            "description": "",
            "path": new_file_path,
            "visible_file" : False,
            "chosen_bbs" : chosen_bbs
        }
        file_result = files_collection.insert_one(file_document)
        
        # Insert into 'to_be_edited' collection
        edit_document = {
            "file_id": file_result.inserted_id,
            "filename": clean_filename,
            "file_size" : file_size,
            "area_id": specific_document['area_id'],
            "uploaded_by_user_id" : specific_document['user_id'],
            "description_empty": True,
            "chosen_bbs" : chosen_bbs
        }
        edit_result = to_be_edited_collection.insert_one(edit_document)
    else:
        print(f"File {new_file_path} does not exist in the bucket.")
    return status


if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=True)
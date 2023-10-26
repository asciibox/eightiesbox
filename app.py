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

app = Flask(__name__)
socketio = SocketIO(app, logger=False, engineio_logger=False)




MAX_FILE_SIZE = 1024 * 102  # 1MB in bytes
server_available = True
util = None
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
list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]
menu_structure = {
            'Goto & Gosub': ['Goto new menu', 'Gosub new menu', 'Return from gosub'],
            'Message base': ['Read message', 'Write message', 'Area change'],
            'File base': ['Download files', 'Upload files', 'List files', 'Select file area'],
            'User options': ['Change password', 'Change email', 'Change interests/hobbies'],
            'Login/Logout': ['Logout', 'Show oneliners'],
            'Multiline options': ['Users online', 'Chat between nodes', 'Add conference', 'Join conference', 'Delete conference'],
            'Display text': ['Display ANS / ASC', 'Display ANS / ASC and wait'],
            'BBS List': ['Long list display', 'Short list display', 'Add BBS'],
            'Administration': ['Setup message areas', 'Setup file base', 'User editor', 'ANSI Editor', 'Menu editor']
        }


def load_json_data():
    with open("main.json", "r") as f:
        return json.load(f)

def create_main_menus():
    global mongo_client
    num_rows = 50
    fields = ['Type', 'Data', 'Key', 'Sec', 'Flags']
    values = [["" for _ in fields] for _ in range(num_rows)]

    json_data = load_json_data()

    collection = mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection

    # Check if file already exists
    existing_file = collection.find_one({"filename": 'MAIN.MNU'})
    if existing_file:
        return

    non_empty_values = [
        {"y": index, "row_data": {str(fields.index(key)): value for key, value in row.items()}}
        for index, row in enumerate(json_data["table"])
    ]

    print("NON_EMPTY_VALUES")
    print(non_empty_values)
    # Save the new file
    menu_box_data = {
        "fields": fields,
        "values": non_empty_values,
    }

    new_file_data = {
        "filename": 'MAIN.MNU',
        "menu_box_data": menu_box_data,
        "ansi_code_base64": json_data.get("ansi_data", "")  # Assuming ansi_data is the field in your JSON
        # Add other file details here
    }

    collection.insert_one(new_file_data)




create_main_menus()

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

startFile = 'welcome'


@socketio.on('custom_disconnect')
def custom_disconnect(data):
    print("custom disconnect")
    on_connection_close()



    

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    
    on_new_connection()
    
    socketio.emit('initPage',  [
        {'minWidth': 0, 'x': 40, 'y': 25},
        {'minWidth': 640, 'x': 80, 'y': 50},
        {'minWidth': 960, 'x': 120, 'y': 80}
    ], room=request.sid)

@socketio.on('upload_finished')
def upload_finished():
    print("UPLOAD FINISHED")  
    
@socketio.on('onload')
def onload(data):
    x = data.get('x')
    sid_data[request.sid].setXWidth(x)
    y = data.get('y')
    sid_data[request.sid].setYHeight(y)
    if server_available == False:
        sid_data[request.sid].util.output_wrap("* Database connection could not get established *", 1,0)
        print(server_available)
        time.sleep(3)
    
    data2 = { 'filename' : startFile+'-'+str(x)+'x'+str(y), 'x' : x, 'y': y}
    
    sid_data[request.sid].util.show_file(data2, sid_data[request.sid].util.emit_current_string)
    sid_data[request.sid].util.goto_next_line()
    
    sid_data[request.sid].util.output_wrap("Please enter your name: ", 3, 0)
    sid_data[request.sid].util.ask(40, sid_data[request.sid].util.usernameCallback)

@socketio.on('disconnect')
def disconnect():
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
       
        # Check file size
        if len(base64_string) > MAX_FILE_SIZE:
            return jsonify({"error": "File size exceeds 100KB"}), 400
        
        filename = generate_unique_filename(filename)

        # Save file data and filename to MongoDB
        new_file = {
            "filename": filename,
            "file_data": base64_string
        }

        #with open('output_app.ans', "w", encoding='cp1252') as ansi_file:
        #
        #     ansi_file.write(file_data)

        uploads_collection.insert_one(new_file)
        return jsonify({"success": f"File {filename} uploaded successfully"}), 200

def generate_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    
    # If the filename (including its extension) is longer than 11 characters, truncate it.
    if len(filename) > 11:
        base = base[:11-len(ext)]  # Adjust so that the total length remains 11 characters
    
    original_base = base
    counter = 1

    # Check if file exists and modify the filename accordingly
    while uploads_collection.find_one({"filename": base + ext}):
        # Adjust the base name to accommodate the counter
        base = original_base[:11-len(ext)-len(str(counter))] + str(counter)
        counter += 1

    return base + ext
  
@socketio.on('input_keypress')
def handle_keypress(data):
    print("HANDLE")
    print(request.sid)
    global sid_data
    siddata = sid_data[request.sid]
    print(siddata.current_action)

    key = data['key']
    print("KEY: *"+key+"*")
    if key == 'F10':
       siddata.setF10ActionHandler(F10ActionHandler(siddata.util))
       siddata.f10actionhandler.handle_F10()
       return
    elif siddata.current_action == "in_chat" and siddata.chat_partner:
        partner_sid_data = siddata.chat_partner
        partner_util = partner_sid_data.util  # Assume util is accessible from sid_data

        if key == 'Escape':
            print("Debug siddata: ", siddata.__dict__)
            print("Debug partner_sid_data: ", partner_sid_data.__dict__)
            siddata.current_action = siddata.previous_action
            siddata.copy_action = False
            
            siddata.util.clear_screen()
            basicANSI = BasicANSI(siddata.util)
            basicANSI.display_editor(siddata.copy_color_array, siddata.copy_color_bgarray, siddata.copy_input_values, None) # None: just restore the original ANSI, no matter what menu points
            siddata.copy_action = True

            print("Debug siddata after: ", siddata.__dict__)
            print("Debug partner_sid_data: ", partner_sid_data.__dict__)
            partner_sid_data.current_action = partner_sid_data.previous_action

            partner_sid_data.copy_action = False

            partner_sid_data.util.clear_screen()
            basicANSI = BasicANSI(partner_sid_data.util)
            basicANSI.display_editor(partner_sid_data.copy_color_array, partner_sid_data.copy_color_bgarray, partner_sid_data.copy_input_values, None) # None: just restore the original ANSI, no matter what menu points
            partner_sid_data.copy_action = True
            print("Debug partner_sid_data after: ", partner_sid_data.__dict__)
            #if siddata.chat_callback != None:
            #    print("CALLBACK FOR SIDDATA")
            #    print(siddata.chat_callback)
            #    siddata.chat_callback()
            #    siddata.chat_callback = None
#
            #if partner_sid_data.chat_callback != None:
            #    print("CALLBACK FOR PARTNER_SIDDATA")
            #    print(partner_sid_data.chat_callback)
            #    partner_sid_data.chat_callback()
            #    partner_sid_data.chat_callback = None

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
        print("WAIT FOR F10 ACTION")
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
    elif siddata.current_action == "wait_for_menu":
        key = data['key']
        siddata.menu.handle_key(key)
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
        siddata.menutexteditor.handle_key(data['key'])
        return
    elif (siddata.current_action == "wait_for_ansieditor"):
        siddata.ansi_editor.handle_key(data['key'])
        return
    elif (siddata.current_action == "wait_for_messageeditor"):
        siddata.message_editor.handle_key(data['key'])
        return
    elif (siddata.current_action == "wait_for_input"):
        key = data['key']

        if key == "ä":
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
            





if __name__ == '__main__':
   socketio.run(app, host='0.0.0.0', port=5000, debug=True)
from flask import request
from userregistration import *
from oneliners import *
from datetime import datetime

socketio = None  # Declare as a global variable
mongo_client = None
sid_data = None

def init_utils_listeners(sio, my_client, sdata):
    global socketio, mongo_client, sid_data
    socketio = sio
    mongo_client = my_client
    sid_data = sdata.get(request.sid)
    
def askinput(mylen, callback, accept_keys):
    sid_data.setCurrentAction("wait_for_input")
    sid_data.setCurrentPos(0)
    sid_data.setMaxLength(mylen)
    sid_data.setLocalInput("")
    sid_data.setAcceptKeys(accept_keys)
    sid_data.setCallback(callback)
    mystr = " "*(mylen)
    #current_time = datetime.now().strftime("%H:%M:%S")
    #emit_current_string(str(len(sid_data.localinput))+current_time, 1, 0, False, 0, 0)
    emit_current_string(mystr, 14, 4, False, sid_data.startX, sid_data.startY)
    emit_gotoXY(sid_data.startX, sid_data.startY)

def ask(mylen, callback, accept_keys = []):
    sid_data.setInputType("text")
    askinput(mylen, callback, accept_keys)
    

def askPassword(mylen, callback, accept_keys = []):
    sid_data.setInputType("password")
    askinput(mylen, callback, accept_keys)

def askYesNo(question, callback):
    sid_data.setCurrentAction("wait_for_yes_no")
    emit_current_string(question+" (Y/N)", 6, 0, False, sid_data.startX, sid_data.startY)
    sid_data.setCallback(callback)

def wait(callback):
    sid_data.setCurrentAction("wait_for_any_button")
    sid_data.setCallback(callback)
    
def goto_next_line():
    sid_data.setStartX(0)
    sid_data.setStartY(sid_data.startY+1)
    sid_data.setCursorX(0)
    sid_data.setCursorY(sid_data.startY)

def output(currentString, currentColor, backgroundColor):
    emit_current_string(currentString, currentColor, backgroundColor, False, sid_data.startX, sid_data.startY)
    mylen = len(currentString)
    sid_data.setStartX(sid_data.startX+mylen)
    sid_data.setCursorX(sid_data.startX+mylen)
    sid_data.setCursorY(sid_data.startY)



def passwordCallback(input):
    goto_next_line()
    bbs = OnelinerBBS(mongo_client, sid_data, goto_next_line, output, askYesNo, ask, wait, launchMenuCallback)
    bbs.show_oneliners()

def usernameCallback(input):
    db = mongo_client['bbs']
    users_collection = db['users']
    print("usernameCallback")
    if input == '':
        goto_next_line()
        output("Please enter your name: ", 3, 0)
        ask(40, usernameCallback)
        return
    print("MONGO"+input)
    user_document = users_collection.find_one({"username": input})
    print("MONGO")
    goto_next_line()

    print("MONGO2")
    if user_document:
        # User exists in the database
        print("password")
        goto_next_line()
        sid_data.setInputType("password")
        output("Please enter your password: ", 3, 0)
        # You might want to pass along the expected password as an argument for the next callback
        askPassword(40, passwordCallback)
    else:
        # User doesn't exist in the database
        goto_next_line()
        print("askYesNo")
        registration = UserRegistration(goto_next_line, ask, askPassword, askYesNo, output, usernameCallback, mongo_client, sid_data, wait, launchMenuCallback)
    print("MONGO DONE")

def map_value(value, list1, list2):
    try:
        index = list1.index(value)
        return list2[index]
    except ValueError:
        return value
    except IndexError:
        return "Index out of range in list2"

def launchMenuCallback():
    output("MENU", 3,0)
    
def emit_gotoXY(x, y):
    sid = request.sid  # Get the Session ID
    socketio.emit('draw', {
            'ascii_codes': [],
            'x': x,
            'y': y
    }, room=sid)
    sid_data.setCursorX(x)
    sid_data.setCursorY(y)

def emit_current_string(currentString, currentColor, backgroundColor, blink, x, y):
    #  input("Press Enter to continue...")
    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]

    sid = request.sid  # Get the Session ID
    if currentString:
        ascii_codes = [ord(char) for char in currentString]
        mapped_ascii_codes = [map_value(code, list2, list1) for code in ascii_codes]
        
        socketio.emit('draw', {
            'ascii_codes': mapped_ascii_codes,
            'currentColor': currentColor,
            'backgroundColor': backgroundColor,
            'blink': blink,
            'x': x,
            'y': y
        }, room=sid)
    return []

def strip_sauce(text):
    sauce_start = text.rfind("\x1ASAUCE00")
    if sauce_start != -1:
        return text[:sauce_start]
    return text

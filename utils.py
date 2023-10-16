from flask import request
from userregistration import *
from oneliners import *
from datetime import datetime
from menubox import *

socketio = None  # Declare as a global variable
mongo_client = None
sid_data = None
list2 = None
list1 = None

def init_utils_listeners(sio, my_client, sdata, mylist1, mylist2):
    global socketio, mongo_client, sid_data, list1, list2
    socketio = sio
    mongo_client = my_client
    sid_data = sdata.get(request.sid)
    list1 = mylist1
    list2 = mylist2
    
def askinput(mylen, callback, accept_keys):
    print("Switched to wait_for_inpu")
    sid_data.setCurrentAction("wait_for_input")
    sid_data.setCurrentPos(0)
    sid_data.setMaxLength(mylen)
    sid_data.setLocalInput("")
    sid_data.setAcceptKeys(accept_keys)
    sid_data.setCallback(callback)
    mystr = " "*(mylen)
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
    db = mongo_client['bbs']
    users_collection = db['users']
    
    # Retrieve the user document based on the username saved in sid_data
    user_document = users_collection.find_one({"username": sid_data.user_name})
    
    if user_document:
        # Check if the password matches
        if input == user_document.get('password'):  # Replace 'password' with the actual field name in your MongoDB document
            goto_next_line()
            bbs = OnelinerBBS(mongo_client, sid_data, goto_next_line, output, askYesNo, ask, wait, launchMenuCallback)
            bbs.show_oneliners()
        else:
            goto_next_line()
            output("Incorrect password. Try again: ", 3, 0)
            askPassword(40, passwordCallback)  # Prompt again for the password
    else:
        # This should not happen, but just in case
        goto_next_line()
        output("User not found. Please re-enter username: ", 3, 0)
        ask(40, usernameCallback)

def usernameCallback(input):
    db = mongo_client['bbs']
    users_collection = db['users']
    if input == '':
        goto_next_line()
        output("Please enter your name: ", 3, 0)
        ask(40, usernameCallback)
        return
    user_document = users_collection.find_one({"username": input})
    sid_data.setUserName(input)
    goto_next_line()

    if user_document:
        # User exists in the database
        goto_next_line()
        sid_data.setInputType("password")
        output("Please enter your password: ", 3, 0)
        # You might want to pass along the expected password as an argument for the next callback
        askPassword(40, passwordCallback)
    else:
        # User doesn't exist in the database
        goto_next_line()
        registration = UserRegistration(goto_next_line, ask, askPassword, askYesNo, output, usernameCallback, mongo_client, sid_data, wait, launchMenuCallback)

def map_value(value, list1, list2):
    try:
        index = list1.index(value)
        return list2[index]
    except ValueError:
        return value  # returns the original value if not found in list1
    except IndexError:
        print(f"Index out of range in list2 for value {value}")
        return value  # returns the original value if index out of range in list2

def launchMenuCallback():
    sid_data.setMenuBox(MenuBox(sid_data, output, ask, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line))
    
def emit_gotoXY(x, y):
    sid = request.sid  # Get the Session ID
    socketio.emit('draw', {
            'ascii_codes': [],
            'x': x,
            'y': y
    }, room=sid)
    sid_data.setCursorX(x)
    sid_data.setCursorY(y)

def clear_screen():
    sid = request.sid  # Get the Session ID
    socketio.emit('clear', {}, room=sid)

def clear_line(y):
    sid = request.sid  # Get the Session ID
    socketio.emit('clearline', {'y': y}, room=sid)

def emit_upload():
    sid = request.sid  # Get the Session ID
    socketio.emit('upload', {}, room=sid)

def emit_current_string(currentString, currentColor, backgroundColor, blink, x, y):
    #  input("Press Enter to continue...")

    sid = request.sid  # Get the Session ID
    if currentString:
        ascii_codes = [ord(char) for char in currentString]

        if sid_data.map_character_set == True:
            mapped_ascii_codes = [map_value(code, list2, list1) for code in ascii_codes]
            
            socketio.emit('draw', {
                'ascii_codes': mapped_ascii_codes,
                'currentColor': currentColor,
                'backgroundColor': backgroundColor,
                'blink': blink,
                'x': x,
                'y': y
            }, room=sid)
        else:
            socketio.emit('draw', {
                'ascii_codes': ascii_codes,
                'currentColor': currentColor,
                'backgroundColor': backgroundColor,
                'blink': blink,
                'x': x,
                'y': y
            }, room=sid)

    return []


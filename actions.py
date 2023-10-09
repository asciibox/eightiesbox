import os
import codecs
from utils import strip_sauce 
from stransi import Ansi, SetAttribute, SetColor, SetCursor
from stransi.attribute import Attribute, SetAttribute
from stransi.color import ColorRole, SetColor
from stransi.cursor import CursorMove, SaveCursor, RestoreCursor
from ochre import ansi256  # Assuming this is where the colors list is defined
from utils import *
from flask import request
from sessiondata import *

socketio = None  # Declare as a global variable
mongo_client = None

current_action = None
sid_data = None

def code():
    codestring = ""
    for i in range(128, 256):
        codestring += f"{i}:{chr(i)} "
    
    startX = 0  # Assuming startX starts at 0, change as needed
    startY = 0  # Assuming startY starts at 0, change as needed
    
    slice_length = 10  # Number of codes per slice
    for i in range(0, len(codestring), slice_length * 4):  # 4 characters per code (e.g., "128:A ")
        slice_str = codestring[i:i + slice_length * 4]
        emit_current_string(slice_str, 14, 4, False, startX, startY)
        startY += 1  # Increment startY by 1


def keydown(key):
    print("KEY:"+key)
    if len(sid_data.accept_keys)>0 and key.upper() not in sid_data.accept_keys:
        return 
    if (sid_data.localinput == ''):
        sid_data.setLocalInput(sid_data.localinput + key)
        sid_data.setCurrentPos(sid_data.currentPos + 1)
        output = sid_data.localinput
        if sid_data.inputType=='password':
            output = "*"*len(output)
        emit_current_string(output, 14, 4, False, sid_data.startX, sid_data.startY)
        sid_data.setCursorX(sid_data.cursorX + 1)
        emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
            

    elif sid_data.insert:
        # Insert the new character at cursorX position
        print("IF INSERT")
        if len(sid_data.localinput) < sid_data.maxLength:
            print("INSERT")
            sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos] + key + sid_data.localinput[sid_data.currentPos:])
            sid_data.setCurrentPos(sid_data.currentPos+ 1)
            output = sid_data.localinput
            if sid_data.inputType=='password':
                output = "*"*len(output)
            emit_current_string(output, 14, 4, False, sid_data.startX, sid_data.startY)
            sid_data.setCursorX(sid_data.cursorX + 1)
            emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
            
            print("INSERT:"+sid_data.localinput)
       
    else:
        print("IF OVERWRITE")
        # Overwrite the character at cursorX position
        if sid_data.currentPos < sid_data.maxLength:
            print("OVERWRITE")
            sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos] + key + sid_data.localinput[sid_data.currentPos + 1:])
            print("local input:"+sid_data.localinput)
            sid_data.setCurrentPos(sid_data.currentPos + 1)
            output = sid_data.localinput
            if sid_data.inputType=='password':
                output = "*"*len(output)
            emit_current_string(output, 14, 4, False, sid_data.startX, sid_data.startY)
            sid_data.setCursorX(sid_data.cursorX + 1)
            emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
      

def init_action_listeners(sio, my_client, sdata):
    global socketio, mongo_client, sid_data
    socketio = sio
    mongo_client = my_client
    sid_data = sdata.get(request.sid)

    @socketio.on('input_keypress')
    def handle_keypress(data):
        print(data)
        print(sid_data.current_action)
        if (sid_data.current_action == "wait_for_yes_no"):
            key = data['key']
            if key=='Y' or key == 'y' or key == 'n' or key == 'N':
                sid_data.callback(key)
            return
        elif (sid_data.current_action == "wait_for_any_button"):
            sid_data.callback(key)
        elif (sid_data.current_action == "wait_for_input"):
            print("KEY PRESSED")
            key = data['key']

            if key == "ä":
                # Handle ä
                print("You pressed the ä key")
                keydown(chr(132))
                return
            elif key == "ö":
                # Handle ö
                keydown(chr(148))
                return
            elif key == "ü":
                # Handle ü
                keydown(chr(129))
                return
            elif key == "ß":
                # Handle ß
                keydown(chr(223))
                return
            elif key == "Ä":
                # Handle ß
                keydown(chr(142))
                return
            elif key == "Ö":
                # Handle ß
                keydown(chr(153))
                return
            elif key == "Ü":
                # Handle ß
                keydown(chr(154))
                return

            
            if key == 'Alt' or key =='AltGraph' or key =='Shift' or key == 'Control' or key == 'Dead' or key == 'ArrowDown' or key =='ArrowUp':
                return
                
            if key == 'Enter':
                print("CALLING CALLBACK")
                sid_data.callback(sid_data.localinput)
                return

            if key == 'Insert':
                sid_data.setInsert(not sid_data.insert)
                return

            if key == 'Delete':
                sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos ] + sid_data.localinput[sid_data.currentPos+1:])
                output = sid_data.localinput
                if sid_data.inputType=='password':
                    output = "*"*len(sid_data.localinput)
                emit_current_string(output+" ", 14, 4, False, sid_data.startX, sid_data.startY)
                emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
                return
                
            # Handle cursor left
            if key == 'ArrowLeft':
                if (sid_data.currentPos > 0):
                    emit_gotoXY(sid_data.cursorX-1, sid_data.cursorY)
                    sid_data.setCurrentPos(sid_data.currentPos - 1)
                return

            # Handle cursor right
            elif key == 'ArrowRight':
                if (sid_data.currentPos < len(sid_data.localinput)):
                    emit_gotoXY(sid_data.cursorX+1, sid_data.cursorY)
                    sid_data.setCurrentPos(sid_data.currentPos + 1)
                return

            # Handle backspace
            elif key == 'Backspace':
                # Your backspace logic here
                if (sid_data.currentPos > 0):
                    sid_data.setLocalInput(sid_data.localinput[:-1])
                    output = sid_data.localinput
                    if sid_data.inputType=='password':
                        output = "*"*len(sid_data.localinput)
                    emit_current_string(output+" ", 14, 4, False, sid_data.startX, sid_data.startY)
                    emit_gotoXY(sid_data.cursorX-1, sid_data.cursorY)
                    sid_data.setCurrentPos(sid_data.currentPos - 1)
                return
            # Handle character input
            else:
                keydown(key)
                
                
                
                




def show_file(data):

    currentColor = 15
    backgroundColor = 0
    current_action = "show_file"
    filename = data.get('filename', '') + '.ans'
   
    filepath = os.path.join('ansi', filename)

    if os.path.exists(filepath):
        with codecs.open(filepath, 'r', 'cp437') as f:
            text_content = f.read()

        text_content = strip_sauce(text_content)

        # Filter out the specific ANSI escape code
        filtered_content = text_content.replace("[?7h", "")

        posX, posY = 0, 0
        
        blink = False
        isBold = False
        currentString = []
        storedCursorY = 0
        storedCursorX = 0

        text = Ansi(filtered_content)
        
        for instruction in text.instructions():

            if isinstance(instruction, SetColor):
                newColor = instruction.color.code if instruction.role == ColorRole.FOREGROUND else None
                newBackground = instruction.color.code if instruction.role == ColorRole.BACKGROUND else None

                # Check if the color has changed before updating currentColor
                if newColor is not None and newColor != currentColor:
                    # Emit the string because the color has changed
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                    sid_data.setStartX(posX)
                    sid_data.setStartY(posY)
                    if isBold:
                        currentColor = newColor+8  # Now update the currentColor
                    else:
                        currentColor = newColor  # Now update the currentColor

                # Similarly for background color
                if newBackground is not None and newBackground != backgroundColor:
                    # Emit the string because the background color has changed
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                    sid_data.setStartX(posX)
                    sid_data.setStartY(posY)
                    backgroundColor = newBackground  # Now update the backgroundColor

            if isinstance(instruction, str):
                for char in instruction:
                    if char != '\r' and char != '\l':
                        if char == '\n':
                            posY += 1
                            posX = 0
                            currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                            sid_data.setStartX(posX)
                            sid_data.setStartY(posY)
                            continue
                        elif posX >= data.get('x'):
                            posY += 1
                            posX = 1
                            currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                            currentString.append(char)
                            sid_data.setStartX(posX-1)
                            sid_data.setStartY(posY)
                            continue
                        else:
                            currentString.append(char)
                            posX += 1
                            continue
                

            elif isinstance(instruction, SetAttribute):
                if instruction.attribute == Attribute.BLINK:
                    blink = True
                elif instruction.attribute == Attribute.NOT_BLINK:
                    blink = False
                elif instruction.attribute == Attribute.BOLD:  # Add this line
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                    sid_data.setStartX(posX)
                    sid_data.setStartY(posY)
                    isBold = True  # Add this line
                elif instruction.attribute == Attribute.NORMAL:  # Add this line
                    isBold = False  # Add this line
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                    sid_data.setStartX(posX)
                    sid_data.setStartY(posY)
                    backgroundColor = 0

            elif isinstance(instruction, SetCursor):
                move = instruction.move
                if move.relative:
                    posX += move.x
                    posY += move.y
                    if posX > 80:
                        posX = posX-80
                        posY = posY + 1
                else:
                    posX = move.x
                    posY = move.y
                    posX = max(0, posX)
                    posY = max(0, posY)

                # Handle specific CursorMove methods
                if move == CursorMove.to_home():
                    posX, posY = 0, 0
                elif move == CursorMove.up():
                    posY -= 1
                elif move == CursorMove.up(1):
                    posY -= 1
                elif move == CursorMove.to(0, 0):  # Assuming (0, 0) is home
                    posX, posY = 0, 0
               
                currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
               
                sid_data.setStartX(posX)
                sid_data.setStartY(posY)
                if posX>80:
                    posX=80

            elif isinstance(instruction, SaveCursor):
                storedCursorX = posX
                storedCursorY = posY
                continue


            elif isinstance(instruction, RestoreCursor):
                currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
                posX = storedCursorX
                posY = storedCursorY
                sid_data.setStartX(posX)
                sid_data.setStartY(posY)
                continue
                




        emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY)
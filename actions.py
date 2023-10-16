import os
import codecs
from stransi import Ansi, SetAttribute, SetColor, SetCursor
from stransi.attribute import Attribute, SetAttribute
from stransi.color import ColorRole, SetColor
from stransi.cursor import CursorMove, SaveCursor, RestoreCursor
from ochre import ansi256  # Assuming this is where the colors list is defined
from utils import *
from flask import request
from sessiondata import *
import random
from menubar_menueditor import *
from sauce import *

socketio = None  # Declare as a global variable
mongo_client = None

current_action = None
sid_data = None




def keydown(key):
    if len(sid_data.accept_keys)>0 and key.upper() not in sid_data.accept_keys:
        return 
    if (sid_data.localinput == ''):
        sid_data.setLocalInput(sid_data.localinput + key)
        sid_data.setCurrentPos(sid_data.currentPos + 1)
        myoutput = sid_data.localinput
        if sid_data.inputType=='password':
            myoutput = "*"*len(myoutput)
        emit_current_string(myoutput, 14, 4, False, sid_data.startX, sid_data.startY)
        sid_data.setCursorX(sid_data.cursorX + 1)
        emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
            

    elif sid_data.insert:
        # Insert the new character at cursorX position
        if len(sid_data.localinput) < sid_data.maxLength:
            sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos] + key + sid_data.localinput[sid_data.currentPos:])
            sid_data.setCurrentPos(sid_data.currentPos+ 1)
            myoutput = sid_data.localinput
            if sid_data.inputType=='password':
                myoutput = "*"*len(myoutput)
            emit_current_string(myoutput, 14, 4, False, sid_data.startX, sid_data.startY)
            sid_data.setCursorX(sid_data.cursorX + 1)
            emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
       
    else:
        # Overwrite the character at cursorX position
        if sid_data.currentPos < sid_data.maxLength:
            sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos] + key + sid_data.localinput[sid_data.currentPos + 1:])
            sid_data.setCurrentPos(sid_data.currentPos + 1)
            myoutput = sid_data.localinput
            if sid_data.inputType=='password':
                myoutput = "*"*len(myoutput)
            emit_current_string(myoutput, 14, 4, False, sid_data.startX, sid_data.startY)
            sid_data.setCursorX(sid_data.cursorX + 1)
            emit_gotoXY(sid_data.cursorX, sid_data.cursorY)
      

def init_action_listeners(sio, my_client, sdata):
    global socketio, mongo_client, sid_data
    socketio = sio
    mongo_client = my_client
    sid_data = sdata.get(request.sid)

    @socketio.on('input_keypress')
    def handle_keypress(data):
        print(sid_data.current_action)
        if sid_data.current_action == "wait_for_layered_menu":
            key = data['key']
            if sid_data.menu_box.in_sub_menu:  # in_sub_menu is a new attribute to check if you're in a sub-menu
                if key == 'ArrowUp': 
                    sid_data.menu_box.sub_menu_arrow_up()
                    
                elif key == 'ArrowDown':
                    sid_data.menu_box.sub_menu_arrow_down()
                    
                elif key == 'Enter':
                    sid_data.menu_box.select_sub_menu_item()
                    sid_data.menu_box.hide_menu()
                    sid_data.menu_box.in_sub_menu = False
                    return
                    
                elif key == 'Escape':
                    sid_data.menu_box.hide_sub_menu()
                    sid_data.menu_box.in_sub_menu = False

            else:
                if key == 'ArrowLeft':
                    sid_data.menu_box.main_arrow_left()
                    
                elif key == 'ArrowRight':
                    sid_data.menu_box.main_arrow_right()
                    
                elif key == 'ArrowUp':
                    sid_data.menu_box.main_arrow_up()
                    
                elif key == 'ArrowDown':
                    sid_data.menu_box.main_arrow_down()
                    
                elif key == 'Enter':
                    selected_main_menu = sid_data.menu_box.get_selected_main_menu()
                    sid_data.menu_box.show_sub_menu()
                    sid_data.menu_box.in_sub_menu = True
                    return
                    
                elif key == 'Escape':
                    sid_data.menu_box.hide_menu()

        if sid_data.current_action == "wait_for_menu":
            key = data['key']
            
            if key == 'ArrowLeft':
                sid_data.menu_box.arrow_left()
                
            elif key == 'ArrowRight':
                sid_data.menu_box.arrow_right()
                
            elif key == 'ArrowUp':
                sid_data.menu_box.arrow_up()
                
            elif key == 'ArrowDown':
                sid_data.menu_box.arrow_down()
                
            elif key == 'Enter':
                sid_data.menu_box.edit_field()
                return

            elif key == 'Escape':
                sub_menus = {
                    'File': ['Load menu', 'Save menu', 'New menu', 'Delete menu'],
                    'Edit': ['Edit text', 'Simulate text', 'Clear text', 'View text', 'Leave menu bar'],
                }
                
                sid_data.setMenuBar(MenuBarMenuEditor(sub_menus, sid_data, output, ask, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file_content, emit_upload))
                return
            
            return

        if sid_data.current_action == "wait_for_menubar":
            key = data['key']
            
            if key == 'ArrowLeft':
                sid_data.menu_bar.arrow_left()
                
            elif key == 'ArrowRight':
                sid_data.menu_bar.arrow_right()
                
            elif key == 'ArrowUp':
                sid_data.menu_bar.arrow_up()
                
            elif key == 'ArrowDown':
                sid_data.menu_bar.arrow_down()
                
            elif key == 'Enter':
                sid_data.menu_bar.choose_field()
                return

            elif key == 'Escape':
                sid_data.menu_bar.leave_menu_bar()
                return
            
            return

        if (sid_data.current_action == "wait_for_yes_no"):
            key = data['key']
            if key=='Y' or key == 'y' or key == 'n' or key == 'N':
                sid_data.callback(key)
            return
        elif (sid_data.current_action == "wait_for_any_button"):
            sid_data.callback()
            return
        elif (sid_data.current_action == "wait_for_menutexteditor"):
            print(sid_data)
            sid_data.menutexteditor.handle_key(data['key'])
            return
        elif (sid_data.current_action == "wait_for_ansieditor"):
            sid_data.ansi_editor.handle_key(data['key'])
            return
        elif (sid_data.current_action == "wait_for_input"):
            key = data['key']

            if key == "ä":
                # Handle ä
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

            
            if key == 'Alt' or key=='Escape' or key =='AltGraph' or key =='Shift' or key == 'Control' or key == 'Dead' or key == 'ArrowDown' or key =='ArrowUp' or key =='CapsLock' or key=='Tab':
                return
                
            if key == 'Enter':
                sid_data.callback(sid_data.localinput)
                return

            if key == 'Insert':
                sid_data.setInsert(not sid_data.insert)
                return

            if key == 'Delete':
                sid_data.setLocalInput(sid_data.localinput[:sid_data.currentPos ] + sid_data.localinput[sid_data.currentPos+1:])
                myoutput = sid_data.localinput
                if sid_data.inputType=='password':
                    myoutput = "*"*len(sid_data.localinput)
                emit_current_string(myoutput+" ", 14, 4, False, sid_data.startX, sid_data.startY)
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
                    myoutput = sid_data.localinput
                    if sid_data.inputType=='password':
                        myoutput = "*"*len(sid_data.localinput)
                    emit_current_string(myoutput+" ", 14, 4, False, sid_data.startX, sid_data.startY)
                    emit_gotoXY(sid_data.cursorX-1, sid_data.cursorY)
                    sid_data.setCurrentPos(sid_data.currentPos - 1)
                return
            # Handle character input
            else:
                keydown(key)
                
                
                
                




def show_file(data, emit_current_string):

    sid_data.setMapCharacterSet(True)
    
    filename = data.get('filename', '') + '.ans'
   
    filepath = os.path.join('ansi', filename)

    if os.path.exists(filepath):
        with codecs.open(filepath, 'r', 'cp437') as f:
            text_content = f.read()
            show_file_content(text_content, emit_current_string)



def show_file_content(text_content, emit_current_string):
    currentColor = 15
    backgroundColor = 0
    terminalWidth = 80

   
    terminalWidth = sid_data.sauceWidth

    # text_content = strip_sauce(text_content)

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
                    elif posX >= terminalWidth: # sid_data.xWidth:
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
                
                #currentColor = currentColor + 8
                sid_data.setStartX(posX)
                sid_data.setStartY(posY)
                isBold = True  # Add this line
            elif instruction.attribute == Attribute.NORMAL:  # Add this line
                isBold = False  # Add this line
                #currentColor = currentColor + 8
                currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, sid_data.startX, sid_data.startY) #modified 0, backgroundColor?
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

    sid_data.setMapCharacterSet(False)

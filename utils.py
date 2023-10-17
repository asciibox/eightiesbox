from flask import request
from userregistration import *
from oneliners import *
from datetime import datetime
from menubox import *
import codecs
from stransi import Ansi, SetAttribute, SetColor, SetCursor
from stransi.attribute import Attribute, SetAttribute
from stransi.color import ColorRole, SetColor
from stransi.cursor import CursorMove, SaveCursor, RestoreCursor
from ochre import ansi256  # Assuming this is where the colors list is defined

class Utils:
    def __init__(self, sio, my_client, mylist1, mylist2, sdata):
        self.socketio = sio
        self.mongo_client = my_client
        self.sid_data = sdata.get(request.sid)
        self.list1 = mylist1
        self.list2 = mylist2
    
    def askinput(self, mylen, callback, accept_keys):
        print("Switched to wait_for_inpu")
        self.sid_data.setCurrentAction("wait_for_input")
        self.sid_data.setCurrentPos(0)
        self.sid_data.setMaxLength(mylen)
        self.sid_data.setLocalInput("")
        self.sid_data.setAcceptKeys(accept_keys)
        self.sid_data.setCallback(callback)
        mystr = " "*(mylen)
        self.emit_current_string(mystr, 14, 4, False, self.sid_data.startX, self.sid_data.startY)
        self.emit_gotoXY(self.sid_data.startX, self.sid_data.startY)

    def ask(self, mylen, callback, accept_keys = []):
        self.sid_data.setInputType("text")
        self.askinput(mylen, callback, accept_keys)
        

    def askPassword(self, mylen, callback, accept_keys = []):
        self.sid_data.setInputType("password")
        self.askinput(mylen, callback, accept_keys)

    def askYesNo(self, question, callback):
        self.sid_data.setCurrentAction("wait_for_yes_no")
        self.emit_current_string(question+" (Y/N)", 6, 0, False, self.sid_data.startX, self.sid_data.startY)
        self.sid_data.setCallback(callback)

    def wait(self, callback):
        self.sid_data.setCurrentAction("wait_for_any_button")
        self.sid_data.setCallback(callback)
        
    def goto_next_line(self, ):
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(self.sid_data.startY+1)
        self.sid_data.setCursorX(0)
        self.sid_data.setCursorY(self.sid_data.startY)

    def output(self, currentString, currentColor, backgroundColor):
        self.emit_current_string(currentString, currentColor, backgroundColor, False, self.sid_data.startX, self.sid_data.startY)
        mylen = len(currentString)
        self.sid_data.setStartX(self.sid_data.startX+mylen)
        self.sid_data.setCursorX(self.sid_data.startX+mylen)
        self.sid_data.setCursorY(self.sid_data.startY)



    def passwordCallback(self, input):
        db = self.mongo_client['bbs']
        users_collection = db['users']
        
        # Retrieve the user document based on the username saved in self.sid_data
        user_document = users_collection.find_one({"username": self.sid_data.user_name})
        
        if user_document:
            # Check if the password matches
            if input == user_document.get('password'):  # Replace 'password' with the actual field name in your MongoDB document
                self.goto_next_line()
                bbs = OnelinerBBS(self)
                bbs.show_oneliners()
            else:
                self.goto_next_line()
                self.output("Incorrect password. Try again: ", 3, 0)
                self.askPassword(40, passwordCallback)  # Prompt again for the password
        else:
            # This should not happen, but just in case
            self.goto_next_line()
            self.output("User not found. Please re-enter username: ", 3, 0)
            ask(40, self.usernameCallback)

    def usernameCallback(self, input):
        db = self.mongo_client['bbs']
        users_collection = db['users']
        if input == '':
            self.goto_next_line()
            self.output("Please enter your name: ", 3, 0)
            ask(40, self.usernameCallback)
            return
        user_document = users_collection.find_one({"username": input})
        self.sid_data.setUserName(input)
        self.goto_next_line()

        if user_document:
            # User exists in the database
            self.goto_next_line()
            self.sid_data.setInputType("password")
            self.output("Please enter your password: ", 3, 0)
            # You might want to pass along the expected password as an argument for the next callback
            self.askPassword(40, self.passwordCallback)
        else:
            # User doesn't exist in the database
            self.goto_next_line()
            registration = UserRegistration(self, self.launchMenuCallback)

    def map_value(self, value, list1, list2):
        try:
            index = list1.index(value)
            return list2[index]
        except ValueError:
            return value  # returns the original value if not found in list1
        except IndexError:
            print(f"Index out of range in list2 for value {value}")
            return value  # returns the original value if index out of range in list2

    def launchMenuCallback(self):
        self.sid_data.setMenuBox(MenuBox(self))
        
    def emit_gotoXY(self, x, y):
        sid = request.sid  # Get the Session ID
        self.socketio.emit('draw', {
                'ascii_codes': [],
                'x': x,
                'y': y
        }, room=sid)
        self.sid_data.setCursorX(x)
        self.sid_data.setCursorY(y)

    def clear_screen(self):
        sid = request.sid  # Get the Session ID
        self.socketio.emit('clear', {}, room=sid)

    def clear_line(self, y):
        sid = request.sid  # Get the Session ID
        self.socketio.emit('clearline', {'y': y}, room=sid)

    def emit_upload(self):
        sid = request.sid  # Get the Session ID
        self.socketio.emit('upload', {}, room=sid)

    def emit_current_string(self, currentString, currentColor, backgroundColor, blink, x, y):
        #  input("Press Enter to continue...")

        sid = request.sid  # Get the Session ID
        if currentString:
            ascii_codes = [ord(char) for char in currentString]

            if self.sid_data.map_character_set == True:
                mapped_ascii_codes = [self.map_value(code, self.list2, self.list1) for code in ascii_codes]
                
                self.socketio.emit('draw', {
                    'ascii_codes': mapped_ascii_codes,
                    'currentColor': currentColor,
                    'backgroundColor': backgroundColor,
                    'blink': blink,
                    'x': x,
                    'y': y
                }, room=sid)
            else:
                self.socketio.emit('draw', {
                    'ascii_codes': ascii_codes,
                    'currentColor': currentColor,
                    'backgroundColor': backgroundColor,
                    'blink': blink,
                    'x': x,
                    'y': y
                }, room=sid)

        return []

    def keydown(self, key):
        if len(self.sid_data.accept_keys)>0 and key.upper() not in self.sid_data.accept_keys:
            return 
        if (self.sid_data.localinput == ''):
            self.sid_data.setLocalInput(self.sid_data.localinput + key)
            self.sid_data.setCurrentPos(self.sid_data.currentPos + 1)
            myoutput = self.sid_data.localinput
            if self.sid_data.inputType=='password':
                myoutput = "*"*len(myoutput)
            self.emit_current_string(myoutput, 14, 4, False, self.sid_data.startX, self.sid_data.startY)
            self.sid_data.setCursorX(self.sid_data.cursorX + 1)
            self.emit_gotoXY(self.sid_data.cursorX, self.sid_data.cursorY)
                

        elif self.sid_data.insert:
            # Insert the new character at cursorX position
            if len(self.sid_data.localinput) < self.sid_data.maxLength:
                self.sid_data.setLocalInput(self.sid_data.localinput[:self.sid_data.currentPos] + key + self.sid_data.localinput[self.sid_data.currentPos:])
                self.sid_data.setCurrentPos(self.sid_data.currentPos+ 1)
                myoutput = self.sid_data.localinput
                if self.sid_data.inputType=='password':
                    myoutput = "*"*len(myoutput)
                self.emit_current_string(myoutput, 14, 4, False, self.sid_data.startX, self.sid_data.startY)
                self.sid_data.setCursorX(self.sid_data.cursorX + 1)
                self.emit_gotoXY(self.sid_data.cursorX, self.sid_data.cursorY)
        
        else:
            # Overwrite the character at cursorX position
            if self.sid_data.currentPos < self.sid_data.maxLength:
                self.sid_data.setLocalInput(self.sid_data.localinput[:self.sid_data.currentPos] + key + self.sid_data.localinput[self.sid_data.currentPos + 1:])
                self.sid_data.setCurrentPos(self.sid_data.currentPos + 1)
                myoutput = self.sid_data.localinput
                if self.sid_data.inputType=='password':
                    myoutput = "*"*len(myoutput)
                self.emit_current_string(myoutput, 14, 4, False, self.sid_data.startX, self.sid_data.startY)
                self.sid_data.setCursorX(self.sid_data.cursorX + 1)
                self.emit_gotoXY(self.sid_data.cursorX, self.sid_data.cursorY)
        
    def show_file(self, data, emit_current_string):

        self.sid_data.setMapCharacterSet(True)
        
        filename = data.get('filename', '') + '.ans'
    
        filepath = os.path.join('ansi', filename)

        if os.path.exists(filepath):
            with codecs.open(filepath, 'r', 'cp437') as f:
                text_content = f.read()
                self.show_file_content(text_content, emit_current_string)



    def show_file_content(self, text_content, emit_current_string):
        currentColor = 15
        backgroundColor = 0
        terminalWidth = 80

    
        terminalWidth = self.sid_data.sauceWidth

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
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                    self.sid_data.setStartX(posX)
                    self.sid_data.setStartY(posY)
                    if isBold:
                        currentColor = newColor+8  # Now update the currentColor
                    else:
                        currentColor = newColor  # Now update the currentColor

                # Similarly for background color
                if newBackground is not None and newBackground != backgroundColor:
                    # Emit the string because the background color has changed
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                    self.sid_data.setStartX(posX)
                    self.sid_data.setStartY(posY)
                    backgroundColor = newBackground  # Now update the backgroundColor

            if isinstance(instruction, str):
                for char in instruction:
                    if char != '\r' and char != '\l':
                        if char == '\n':
                            posY += 1
                            posX = 0
                            currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                            self.sid_data.setStartX(posX)
                            self.sid_data.setStartY(posY)
                            continue
                        elif posX >= terminalWidth: # self.sid_data.xWidth:
                            posY += 1
                            posX = 1
                            currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                            currentString.append(char)
                            self.sid_data.setStartX(posX-1)
                            self.sid_data.setStartY(posY)
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
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                    
                    #currentColor = currentColor + 8
                    self.sid_data.setStartX(posX)
                    self.sid_data.setStartY(posY)
                    isBold = True  # Add this line
                elif instruction.attribute == Attribute.NORMAL:  # Add this line
                    isBold = False  # Add this line
                    #currentColor = currentColor + 8
                    currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY) #modified 0, backgroundColor?
                    self.sid_data.setStartX(posX)
                    self.sid_data.setStartY(posY)
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
                
                currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                
                self.sid_data.setStartX(posX)
                self.sid_data.setStartY(posY)
                if posX>80:
                    posX=80

            elif isinstance(instruction, SaveCursor):
                storedCursorX = posX
                storedCursorY = posY
                continue


            elif isinstance(instruction, RestoreCursor):
                currentString = emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)
                posX = storedCursorX
                posY = storedCursorY
                self.sid_data.setStartX(posX)
                self.sid_data.setStartY(posY)
                continue
        
        emit_current_string(currentString, currentColor, backgroundColor, blink, self.sid_data.startX, self.sid_data.startY)

        self.sid_data.setMapCharacterSet(False)

    def strip_sauce(bytes):
        if len(bytes) < 128:
            return bytes

        # Check the SAUCE ID
        sauce_id = bytes[-128:][:7].decode("cp1252", errors="ignore")
        if sauce_id == "SAUCE00":
            # If there are comments, their length would be indicated in byte 104
            number_of_comments = bytes[-128:][104]
            additional_length = number_of_comments * 64 + 5 if number_of_comments else 0

            # Remove SAUCE and comments
            return bytes[:-(128 + additional_length)]
        else:
            return bytes

    def get_sauce(bytes):
        print("Total length of bytes:", len(bytes))
        print("Last 128 bytes:", bytes[-128:])
        
        print("Last 128 bytes before reading SAUCE:", bytes[-128:])


        if len(bytes) >= 128:
            sauce_bytes = bytes[-128:]
            print("SAUCE ID Bytes:", sauce_bytes[:7])
            print("Finding SAUCE");
            print(sauce_bytes[:7].decode("cp1252"))
            if sauce_bytes[:7].decode("cp1252") == "SAUCE00":
                title = sauce_bytes[7:42].decode("utf-8").rstrip('\0')
                author = sauce_bytes[42:62].decode("utf-8").rstrip('\0')
                group = sauce_bytes[62:82].decode("utf-8").rstrip('\0')
                date = sauce_bytes[82:90].decode("utf-8").rstrip('\0')
                filesize = int.from_bytes(sauce_bytes[90:94], byteorder='little')
                datatype = sauce_bytes[94]
                if datatype == 5:
                    columns = sauce_bytes[95] * 2
                    rows = filesize // (columns * 2)
                else:
                    columns = int.from_bytes(sauce_bytes[96:98], byteorder='little')
                    rows = int.from_bytes(sauce_bytes[98:100], byteorder='little')
                number_of_comments = sauce_bytes[104]
                rawcomments = sauce_bytes[-(number_of_comments * 64 + 128):-128].decode("utf-8")
                comments = '\n'.join([rawcomments[i*64:(i+1)*64].rstrip('\0') for i in range(number_of_comments)])
                flags = sauce_bytes[105]
                ice_colors = (flags & 0x01) == 1
                use_9px_font = (flags >> 1 & 0x02) == 2
                font_name = sauce_bytes[106:128].decode("utf-8").replace('\0', "")
                font_name = "IBM VGA" if font_name == "" else font_name
                if filesize == 0:
                    filesize = len(bytes) - 128
                    if number_of_comments:
                        filesize -= number_of_comments * 64 + 5
                return Sauce(columns, rows, title, author, group, date, filesize, ice_colors, use_9px_font, font_name, comments)
        sauce = Sauce()
        sauce.filesize = len(bytes)
        return sauce

    def append_sauce_to_string(sauce, string):
        # Populate the SAUCE record byte array with the values from the Sauce object
        sauce_bytes = bytearray(128)
        sauce_bytes[0:7] = b'SAUCE00'


        sauce_bytes[7:42] = sauce.title.encode('cp1252').ljust(35, b'\0')
        sauce_bytes[42:62] = sauce.author.encode('cp1252').ljust(20, b'\0')
        sauce_bytes[62:82] = sauce.group.encode('cp1252').ljust(20, b'\0')
        sauce_bytes[82:90] = sauce.date.encode('cp1252').ljust(8, b'\0')
        sauce_bytes[90:94] = sauce.filesize.to_bytes(4, byteorder='little')
        # Assume datatype 5 for binary files, adjust as necessary
        if sauce.columns and sauce.rows:
            sauce_bytes[94] = 5
            sauce_bytes[95] = sauce.columns // 2
            # Compute filesize based on columns and rows if it's not provided
            sauce_bytes[90:94] = (sauce.columns * sauce.rows * 2).to_bytes(4, byteorder='little')
        else:
            # For other datatypes, you might want to set the appropriate datatype value and file type
            pass  # Replace with your logic for other datatypes

        flags = 0
        if sauce.ice_colors:
            flags |= 0x01
        if sauce.use_9px_font:
            flags |= 0x02 << 1  # Shift 1 position to the left to set the correct bit
        sauce_bytes[105] = flags

        # Handle font_name
        sauce_bytes[106:128] = sauce.font_name.encode('cp1252').ljust(22, b'\0')

        # Convert the SAUCE record byte array to a string
        sauce_string = sauce_bytes.decode('cp1252')  # cp1252 encoding will preserve the byte values
        print("SAUCE Bytes in append_sauce_to_string:", sauce_bytes)
        print("String Length Before:", len(string))
        if string[-129:-121].encode('cp1252') == b'\x1ASAUCE00':  # Updated indices and comparison string
            # Replace the existing SAUCE record
            string = string[:-129] + sauce_string  # Updated index to remove the existing SAUCE record
        else:
            # Append the SAUCE record
            string += sauce_string
        
        print("String Length After:", len(string))
        print("Last 1232 bytes after appending SAUCE:", string[-132:].encode('cp1252'))

        
        return string

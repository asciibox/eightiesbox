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
from sauce import Sauce
import bcrypt
import base64
import os
from menu import *
import asyncio
import time
from time import sleep
from threading import Timer
import uuid
import random
from bbschooser import BBSChooser
import jwt

class Utils:
    def __init__(self, sio, my_client, mylist1, mylist2, sdata, Sauce, request_id, menu_structure, secret_key):
        self.socketio = sio
        self.mongo_client = my_client
        self.sid_data = sdata.get(request_id)
        self.all_sid_data = sdata
        self.list1 = mylist1
        self.list2 = mylist2
        self.Sauce = Sauce
        self.passwordRetries = 0
        self.request_id = request_id
        self.menu_structure = menu_structure
        self.secret_key = secret_key

    def askinput(self, mylen, callback, accept_keys, default_value=''):
        if self.sid_data.startX + mylen >= self.sid_data.xWidth:
            self.sid_data.setStartY(self.sid_data.startY + 1)  # Move to the next line
            self.sid_data.setStartX(0)  # Reset the X coordinate for the new line

        self.sid_data.setMaxLength(mylen)
        self.sid_data.setMaxScrollLength(mylen)
        self.sid_data.setAcceptKeys(accept_keys)
        self.sid_data.setCallback(callback)

        # Initialize localinput with default_value
        self.sid_data.setLocalInput(default_value)

        if default_value:
            if len(default_value) >= mylen:
                # If default_value length is equal or exceeds mylen, adjust view_start to show the end of default_value
                self.sid_data.setViewStart(len(default_value) - mylen + 1)
                self.sid_data.setCurrentPos(len(default_value))
            else:
                # If default_value fits within mylen, show the entire default_value
                self.sid_data.setViewStart(0)
                self.sid_data.setCurrentPos(len(default_value))
        else:
            # When there is no default_value
            self.sid_data.setViewStart(0)
            self.sid_data.setCurrentPos(0)

        # Calculate visible string based on view_start and maxLength
            
        if self.sid_data.inputType=="text":
            visible_str = self.sid_data.localinput[self.sid_data.view_start:self.sid_data.view_start + mylen - 1]
        else:
            visible_str = '*' * len(self.sid_data.localinput[self.sid_data.view_start:self.sid_data.view_start + mylen - 1])
        # Pad the visible string with spaces to fill the background
        padded_str = visible_str.ljust(mylen )

        self.emit_current_string(padded_str, 14, 4, False, self.sid_data.startX, self.sid_data.startY)

        # Calculate cursor position
        cursor_position = self.sid_data.currentPos - self.sid_data.view_start
        # Ensure the cursor is within the bounds of the input field
        cursor_position = min(cursor_position, mylen - 1)
        self.emit_gotoXY(self.sid_data.startX + cursor_position, self.sid_data.startY)





    def wait_with_message(self, callback):
        self.output_wrap("Press any key to continue", 6 ,0)
        self.sid_data.setCurrentAction("wait_for_any_button")
        self.sid_data.setCallback(callback)

    def ask(self, mylen, callback, accept_keys = [], default_value = ''):

        current_timestamp = time.time()  # Current time in seconds since the epoch
        
        if self.sid_data.last_activity_timestamp is not None:
            # Calculate elapsed time in minutes
            elapsed_time = (current_timestamp - self.sid_data.last_activity_timestamp)
            
            # Reduce the remaining time by the elapsed minutes
            self.sid_data.remaining_time -= int(elapsed_time)
            # Check if the remaining time is up
            if self.sid_data.remaining_time <= 0:
                self.output_wrap("Your time limit has been reached", 1, 0)                
                return  # Exit the function early since the user is logged out
        
        # Update the last activity timestamp
        self.sid_data.last_activity_timestamp = current_timestamp

        self.sid_data.setInputType("text")
        self.sid_data.setCurrentAction("wait_for_input")
        self.askinput(mylen, callback, accept_keys, default_value)
        

    def askPassword(self, mylen, callback, accept_keys = []):
        self.sid_data.setInputType("password")
        self.sid_data.setCurrentAction("wait_for_input")
        self.askinput(mylen, callback, accept_keys)

    def askYesNo(self, question, callback):
        self.sid_data.setCurrentAction("wait_for_yes_no")
        self.output_wrap(question+" (Y/N)", 6, 0)
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
        self.update_status_bar()

    def get_remaining_time(self):
        current_timestamp = time.time()  # Current time in seconds since the epoch
        

        if self.sid_data.last_activity_timestamp is not None:
            elapsed_time = (current_timestamp - self.sid_data.last_activity_timestamp)
                
            # Reduce the remaining time by the elapsed minutes
            self.sid_data.remaining_time -= int(elapsed_time)
            # Update the last activity timestamp
            self.sid_data.last_activity_timestamp = current_timestamp
            if self.sid_data.remaining_time > 0:
                return self.sid_data.remaining_time
            else:
                return 0
        else:
            self.sid_data.last_activity_timestamp = current_timestamp
            return 180*60       

    def format_seconds_to_hh_mm_ss(self, seconds):
        hours = seconds // 3600  # 3600 seconds in an hour
        remaining_seconds = seconds % 3600
        minutes = remaining_seconds // 60  # 60 seconds in a minute
        remaining_seconds %= 60
        return f"{hours}:{minutes:02d}:{remaining_seconds:02d}"
        
    def get_status_content(self):
        # Generate the status bar content based on pending_requests

        if (self.sid_data.user_name==''):
            status_bar = "Tap here to toggle the keyboard"
        else:            
            status_bar = "Incoming Requests: "+str(len(self.sid_data.incoming_requests))
            # random_number = random.randint(1, 100)  # This will add a random number between 1 and 100
            # status_bar = str(random_number) + " - " + status_bar
            if self.sid_data.xWidth > 50:
                status_bar += " - Press F10 for more"
            else:
                status_bar += " F10"

            status_bar+="   Remaining time: "+self.format_seconds_to_hh_mm_ss(self.get_remaining_time())+" F12 keyboard F1 help"            

        status_content = status_bar+" "*(self.sid_data.xWidth-len(status_bar))
        return status_content

    def update_status_bar(self):
      
        status_content = self.get_status_content()

        # Output the status bar content
        self.emit_status_bar(status_content, 6, 4)

    
    def output_wrap(self, currentString, currentColor, backgroundColor):
        words = currentString.split(' ')  # Split the string by space to get individual words
        line = ""

        for word in words:
            temp_line = line + word + " "  # Add the new word and a space to the current line
            # Calculate the new length if this word is added
            temp_len = self.sid_data.startX + len(temp_line)

            if temp_len <= self.sid_data.xWidth:  # Check if adding this word exceeds the xWidth
                line += word + " "
            else:
                # Emit the current line and reset for the new line
                self.emit_current_string(line.strip(), currentColor, backgroundColor, False, self.sid_data.startX, self.sid_data.startY)
                self.sid_data.setStartY(self.sid_data.startY + 1)  # Move to the next line
                self.sid_data.setStartX(0)  # Reset the X coordinate for the new line
                line = word + " "  # Start the new line with the word that couldn't fit

        # Emit any remaining text
        if line:
            self.emit_current_string(line.strip(), currentColor, backgroundColor, False, self.sid_data.startX, self.sid_data.startY)
            self.sid_data.startX = self.sid_data.startX + len(line.strip())+1

        # Update the cursor position
        self.sid_data.setCursorX(self.sid_data.startX)
        self.sid_data.setCursorY(self.sid_data.startY)

    def update_status_bar_periodically(self):
        if self.sid_data.status_bar_paused == False:
            currentString = self.get_status_content()
            currentColor = 6
            backgroundColor = 4

            sid = self.request_id  # Get the Session ID
            if currentString:
                ascii_codes = [ord(char) for char in currentString]

                if self.sid_data.map_character_set == True:
                    mapped_ascii_codes = [self.map_value(code, self.list2, self.list1) for code in ascii_codes]
                
                    self.socketio.emit('draw_to_status_bar', {
                        'ascii_codes': mapped_ascii_codes,
                        'currentColor': currentColor,
                        'backgroundColor': backgroundColor
                    }, room=sid)
                else:
                    self.socketio.emit('draw_to_status_bar', {
                        'ascii_codes': ascii_codes,
                        'currentColor': currentColor,
                        'backgroundColor': backgroundColor
                    }, room=sid)
        Timer(1, self.update_status_bar_periodically).start()

    def passwordCallback(self, input):
        db = self.mongo_client['bbs']
        users_collection = db['users']
       
        
        # Retrieve the user document based on the username saved in self.sid_data

        user_document = users_collection.find_one({"username": self.sid_data.user_name, 'chosen_bbs': self.sid_data.chosen_bbs})
        self.sid_data.user_document = user_document

        if user_document:

            # Check if the password matches
            hashed_password_from_db = user_document.get('password').encode('utf-8')
            try:
                if bcrypt.checkpw(input.encode('utf-8'), hashed_password_from_db):
                    self.goto_next_line()

                    # Repopulate incoming_requests for the newly logged-in user
                    username = self.sid_data.user_document["username"]
                    for other_sid, other_sid_data in self.all_sid_data.items():
                        for out_req in other_sid_data.outgoing_requests:
                            if out_req['to'] == username and out_req['status'] == 'sent':
                                self.sid_data.incoming_requests.append({
                                    'from': other_sid_data.user_document["username"],
                                    'status': 'received',
                                    'sid_data': other_sid_data  # Store the sid_data of the request sender
                                })
                    

                    self.create_defaults(user_document['_id'], db)
                    self.handle_authentication()
                    # Now proceed to initialize OnelinerBBS
                    bbs = OnelinerBBS(self)
                    bbs.show_oneliners()
                else:
                    self.goto_next_line()
                    self.passwordRetries += 1
                    if self.passwordRetries < 3:
                        self.output_wrap("Incorrect password. Try again: ", 3, 0)
                        self.askPassword(35, self.passwordRetryCallback)  # Prompt again for the password
                        
                    else:
                        self.output_wrap("Too many tries!", 1, 0)
                        self.sid_data.setCurrentAction("exited")
                        return
            except ValueError as e:
                    # Catch the "Invalid salt" error
                    self.goto_next_line()
                    self.output_wrap("An error occurred while verifying your password. Please contact the Sysop.", 6, 0)
                    self.goto_next_line()
                    self.output(str(e), 1, 0)
                    self.goto_next_line()
                    self.output_wrap("Please re-enter username: ", 3, 0)
                    self.ask(35, self.usernameCallback)
        else:
            # This should not happen, but just in case
            self.goto_next_line()
            self.output_wrap("User "+ self.sid_data.user_name + " not found. Please re-enter username: ", 3, 0)
            self.ask(35, self.usernameCallback)

    def passwordRetryCallback(self, input):
        if len(input)==0:
            self.usernameCallback(input)
        else:
            self.passwordCallback(input)

    def bbsCallback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter the name of the new BBS: ", 3, 0)
            self.ask(35, self.bbsCallback)
            return
        
        db = self.mongo_client['bbs']
        mailboxes_collection = db['mailboxes']

        # Insert the new BBS and capture the returned ID
        insert_result = mailboxes_collection.insert_one({"name": input})
        new_bbs_id = insert_result.inserted_id

        # Store the ID of the newly created BBS
        self.sid_data.chosen_bbs = new_bbs_id
        
        self.socketio.emit('set_chosen_bbs', {'chosen_bbs': str(self.sid_data.chosen_bbs)})

        self.usernameCallback("")

    def create_defaults(self, user_id, db):

        my_upload_token = str(uuid.uuid4())
        self.sid_data.setUploadToken(my_upload_token)

        upload_token_collection = db['upload_token']

        # Assume 'user_document' is a document you've retrieved from the 'users' collection
        # user_id = user_document['_id']

        # Now, create the document to insert
        token_document = {
            "token": my_upload_token,
            "user_id": user_id,
            "timestamp" : int(time.time())
        }

        # Insert the document into the collection
        result = upload_token_collection.insert_one(token_document)

        # 'result' will contain information about the insertion
        if result.acknowledged:
            print("Upload token inserted successfully. Document ID:", result.inserted_id)
        else:
            print("Failed to insert upload token.")

        groups_collection = db['groups']
        if groups_collection.count_documents({'chosen_bbs': str(self.sid_data.chosen_bbs)}) == 0:
            default_groups = ["Guest", "New user", "Full user", "File admin", "Message admin", "Sysop"]
            for group_name in default_groups:
                groups_collection.insert_one({"name": group_name, 'chosen_bbs': self.sid_data.chosen_bbs})

        self.store_html_file('admin_medium.html', db)
        self.store_html_file('filebase_medium.html', db)
        self.store_html_file('mbase_medium.html', db)
        self.store_html_file('multi_medium.html', db)
        self.store_html_file('test_menu_medium.html', db)

    def store_html_file(self, filename, db):
        html_dir = 'html/'  # Replace with the actual path
        file_path = os.path.join(html_dir, filename)

        try:
            # Read the file contents
            with open(file_path, 'rb') as file:
                file_contents = file.read()
            print(file_contents)
            # Encode the contents to base64
            encoded_contents = base64.b64encode(file_contents).decode('utf-8')

            # Prepare the document
            document = {
                'filename': filename,
                'chosen_bbs': self.sid_data.chosen_bbs,
                'file_data': encoded_contents,
                'uploaded_file_type': 'HTML'  # As it's always HTML
            }

            # Check if the file already exists in the database
            uploads_html_collection = db['uploads_html']
            existing_file = uploads_html_collection.find_one({'filename': filename, 'chosen_bbs': self.sid_data.chosen_bbs})

            if existing_file is None:
                # Insert the document into the uploads_html collection
                result = uploads_html_collection.insert_one(document)

                # Check the result
                if result.acknowledged:
                    print("File data inserted successfully. Document ID:", result.inserted_id)
                else:
                    print("Failed to insert file data.")
            else:
                print("File already exists in the database.")
        except IOError:
            print("Error: File not found or unable to read html file.")


    def usernameCallback(self, input):
        input = input.strip().lower()

        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your name: ", 3, 0)
            self.ask(35, self.usernameCallback)
            return

        db = self.mongo_client['bbs']
        users_collection = db['users']
        self.sid_data.setUserName(input)
        user_document = users_collection.find_one({"username": input, "chosen_bbs" : self.sid_data.chosen_bbs})

        self.goto_next_line()

        if input == 'sysop':
            if user_document:
                # Sysop user exists
                self.goto_next_line()
                self.sid_data.setInputType("password")
                self.passwordRetries = 0
                self.output_wrap("Please enter your password: ", 3, 0)
                self.askPassword(35, self.passwordCallback)
            else:
                # Sysop user doesn't exist; create a new Sysop user
                self.goto_next_line()
                self.sid_data.setInputType("password")
                self.output_wrap("You are registering as SYSOP. Please enter a new password: ", 3, 0)
                self.askPassword(35, self.sysopPasswordCreationCallback)
            return

        if user_document:
            # User exists in the database
            self.goto_next_line()
            self.sid_data.setInputType("password")
            self.output_wrap("Please enter your password: ", 3, 0)
            self.askPassword(35, self.passwordCallback)
        else:
            # User doesn't exist in the database
            self.goto_next_line()
            registration = UserRegistration(self, self.launchMenuCallback)

    # Callback for Sysop password creation
    def sysopPasswordCreationCallback(self, first_password):
        self.goto_next_line()
        self.sid_data.setInputType("password")
        self.output_wrap("Please confirm your new password: ", 3, 0)
        self.askPassword(35, lambda second_password: self.sysopPasswordConfirmationCallback(first_password, second_password))

    # Callback for Sysop password confirmation
    def sysopPasswordConfirmationCallback(self, first_password, second_password):
        if first_password == second_password:
            # Passwords match; create Sysop user
            db = self.mongo_client['bbs']
            users_collection = db['users']
            hashed_password = bcrypt.hashpw(first_password.encode('utf-8'), bcrypt.gensalt())
            new_sysop_user = {"username": "sysop", "user_level" : 32000, "groups": "Sysop", "password": hashed_password.decode('utf-8'), 'chosen_bbs': self.sid_data.chosen_bbs}
            # Insert the document and capture the result
            insert_result = users_collection.insert_one(new_sysop_user)

            # Retrieve the _id from the result
            new_sysop_user_id = insert_result.inserted_id

            # Add the _id to the sid_data.user_document
            self.sid_data.user_document = {**new_sysop_user, "_id": new_sysop_user_id}
            self.goto_next_line()
            self.output_wrap("SYSOP account created successfully. Logging in...", 3, 0)
            self.launchMenuCallback()
        else:
            self.goto_next_line()
            self.output_wrap("Passwords did not match. Please try again.", 3, 0)
            self.askPassword(35, self.sysopPasswordCreationCallback)

    def map_value(self, value, list1, list2):
        try:
            index = list1.index(value)
            return list2[index]
        except ValueError:
            return value  # returns the original value if not found in list1
        except IndexError:
            return value  # returns the original value if index out of range in list2

    def launchMenuCallback(self):
        self.create_main_menu("MAIN")
        self.create_main_menu("ADMIN")
        self.create_main_menu("MBASE")
        self.create_main_menu("FILEBASE")
        self.create_main_menu("MULTI")
        
        self.check_for_new_messsages()


    def load_json_data(self, menu_name):
        filename = menu_name.lower() + ".json"
        print(f"Loading file: {filename}")

        if not os.path.exists(filename):
            print(f"File not found: {filename}")
            return {}

        try:
            with open(filename, "r") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON in file {filename}: {e}")
            return {}
        except Exception as e:
            print(f"Unexpected error while reading file {filename}: {e}")
            return {}
        
    def create_main_menu(self, menu_name):
        num_rows = 42
        fields = ['Type', 'Data', 'Key', 'Sec', 'Groups', 'HideOnSec']
        values = [["" for _ in fields] for _ in range(num_rows)]

        json_data = self.load_json_data(menu_name)

        # Directly access the 'table' key from json_data
        menu_json_data = json_data.get("table", [])
    
        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection

        # Check if file already exists
        existing_file = collection.find_one({"filename": f'{menu_name}.MNU', "chosen_bbs" : self.sid_data.chosen_bbs})
        if existing_file:
            return

        non_empty_values = [
            {"y": index, "row_data": {str(fields.index(key)): row[key] for key in fields if key in row}}
            for index, row in enumerate(menu_json_data)
        ]

        # Save the new file
        menu_box_data = {
            "fields": fields,
            "values": non_empty_values,
        }

        new_file_data = {
            "filename": f'{menu_name}.MNU',
            "menu_box_data": menu_box_data,
            "ansi_code_base64": json_data.get("ansi_data", ""),
            "chosen_bbs" : self.sid_data.chosen_bbs
            # Add other file details here
        }

        collection.insert_one(new_file_data)


    def check_for_new_messsages(self):
        if self.get_all_unread_messages_addressed_to_user_count() > 0:
                self.sid_data.setMessageReader(MessageReader(self, self.message_reader_new_messages_callback_on_exit))
                self.sid_data.message_reader.display_unread_messages_addressed_to_user()
        else:
            self.message_reader_new_messages_callback_on_exit()

    def message_reader_new_messages_callback_on_exit(self):
        if self.sid_data.user_name=='sysop':
            self.goto_next_line()
            self.askYesNo('Do you want to edit the menu?', self.menuCallback)    
        else:
            self.load_menu()
    

    def get_all_unread_messages_addressed_to_user_count(self):
        user_id = self.sid_data.user_document['_id']
        user_name = self.sid_data.user_name  # Assuming the username is stored in user_name field

        # Connect to MongoDB
        mongo_client = self.mongo_client
        db = mongo_client['bbs']

        # Query read_messages for the current user across all areas
        read_messages_cursor = db['read_messages'].find({
            "user_id": user_id,
            "chosen_bbs" : self.sid_data.chosen_bbs
        })

        # Convert the cursor to a list of message IDs that have been read
        read_message_ids = [msg['message_id'] for msg in read_messages_cursor]

        # Count all unread messages addressed to the current user
        unread_message_count = db['messages'].count_documents({
            "_id": {'$nin': read_message_ids},
            "to": user_name  # Filtering by the 'to' field
        })

        return unread_message_count

    def load_menu(self):
        db = self.mongo_client["bbs"]  # You can replace "mydatabase" with the name of your database
        collection = db["menufiles"]
        file_data = collection.find_one({"filename": 'MAIN.MNU', "chosen_bbs" : self.sid_data.chosen_bbs})
            
        if file_data:
            self.sid_data.setMenu(Menu(self, [["" for _ in ['Type', 'Data', 'Key', 'Sec', 'Groups', 'HideOnSec']] for _ in range(50)], 50, None))
            print("LOADING MAIN.MNU")
            self.sid_data.menu.load_menu('MAIN.MNU')
        else:
            self.goto_next_line()
            self.menuCallback("y")

    def menuCallback(self, input):
        if input=='Y' or input=='y':
            self.sid_data.setMenu(Menu(self, [["" for _ in ['Type', 'Data', 'Key', 'Sec', 'Groups', 'HideOnSec']] for _ in range(50)], 50, None)) 
            self.sid_data.setMenuBox(MenuBox(self))
        else:
            self.goto_next_line()
            self.askYesNo('Do you want to edit users?', self.userEditorCallback)   


    def userEditorCallback(self, input):
        if input=='Y' or input=='y':
            self.sid_data.setUserEditor(UserEditor(self, self.doNothing))
        else:
            self.sid_data.setANSIEditor(ANSIEditor(self))
            self.sid_data.ansi_editor.start()
            self.sid_data.setCurrentAction("wait_for_ansieditor")

    def doNothing(self):
        pass

    def emit_ansi_mod_editor(self):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('ansi_mod_editor', {}, room=sid)
    
    def emit_graphic_mod_editor(self):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('graphic_mod_editor', {}, room=sid)

    def emit_gotoXY(self, x, y):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('draw', {
                'ascii_codes': [],
                'x': x,
                'y': y
        }, room=sid)
        self.sid_data.setCursorX(x)
        self.sid_data.setCursorY(y)

    def clear_screen(self):
        self.sid_data.callbacks = {}
        if self.sid_data.copy_action:
            self.sid_data.copy_color_bgarray = []
            self.sid_data.copy_color_array = []
            self.sid_data.copy_input_values = []

        sid = self.request_id  # Get the Session ID

        # Emit the original clear command
        self.socketio.emit('clear', {}, room=sid)

        # Set the clear command flag
        self.sid_data.clear_command_issued = True

        # Store a clear command in screen data
        self.sid_data.store_screen_data(command='clear')


    def clear_line(self, y):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('clearline', {'y': y}, room=sid)
 
    def emit_toggle_keyboard(self):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('toggle_keyboard', {}, room=sid)

    def emit_uploadANSI(self, upload_file_type):
        sid = self.request_id  # Get the Session ID
        self.socketio.emit('uploadANSI', { 'upload_file_type': upload_file_type}, room=sid)

    def emit_uploadFile(self):
        sid = self.request_id  # Get the Session ID
         # Connect to MongoDB
        formatted_name = self.sid_data.current_file_area['name'].replace(" ", "_")
        formatted_name = formatted_name[:20].ljust(20, '_')
        self.socketio.emit('uploadFile', { 'uploadToken': self.sid_data.upload_token, 'current_file_area' : str(self.sid_data.current_file_area['_id'])+"-"+formatted_name }, room=sid)

    def emit_current_string(self, currentString, currentColor, backgroundColor, blink, x, y):
        #  input("Press Enter to continue...")

        sid = self.request_id  # Get the Session ID
        #print(currentString)
        #print(" to "+str(y))
        if currentString:
            if self.sid_data.copy_action == True:
                self.emit_current_string_2copy(currentString, currentColor, backgroundColor, blink, x, y)

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
                self.sid_data.store_screen_data(mapped_ascii_codes, currentColor, backgroundColor, blink, x, y)

            else:
                self.socketio.emit('draw', {
                    'ascii_codes': ascii_codes,
                    'currentColor': currentColor,
                    'backgroundColor': backgroundColor,
                    'blink': blink,
                    'x': x,
                    'y': y
                }, room=sid)
                self.sid_data.store_screen_data(ascii_codes, currentColor, backgroundColor, blink, x, y)

        return []

    def emit_status_bar(self, currentString, currentColor, backgroundColor):
        #  input("Press Enter to continue...")

        sid = self.request_id  # Get the Session ID
        if currentString:
            ascii_codes = [ord(char) for char in currentString]

            if self.sid_data.map_character_set == True:
                mapped_ascii_codes = [self.map_value(code, self.list2, self.list1) for code in ascii_codes]
                
                self.socketio.emit('draw_to_status_bar', {
                    'ascii_codes': mapped_ascii_codes,
                    'currentColor': currentColor,
                    'backgroundColor': backgroundColor
                }, room=sid)
            else:
                self.socketio.emit('draw_to_status_bar', {
                    'ascii_codes': ascii_codes,
                    'currentColor': currentColor,
                    'backgroundColor': backgroundColor
                }, room=sid)

        return []


    def keydown(self, key):
        # Ensure key is in the accepted keys
        if key.upper() not in self.sid_data.accept_keys and len(self.sid_data.accept_keys) > 0:
            return
        
        if self.sid_data.maxLength == 1:
            # If key is a valid character, update the input and adjust cursor position
            if key.isprintable():
                self.sid_data.localinput = key  # Replace any existing input with the new key
                self.sid_data.currentPos = 1  # Set current position to 1 as the field is now occupied
            elif key == 'Backspace':  # Assuming you have a way to handle backspaces
                self.sid_data.localinput = ''  # Clear the input
                self.sid_data.currentPos = 0  # Reset current position
            # Update display based on the current state of localinput
            visible_str = self.sid_data.localinput if self.sid_data.localinput else ' '  # Show cursor if input is empty
            self.emit_current_string(visible_str, 14, 4, False, self.sid_data.startX, self.sid_data.startY)
            self.emit_gotoXY(self.sid_data.startX+1, self.sid_data.startY)  # Cursor always returns to start position
        else:

            # Handling insert mode
            if self.sid_data.insert:
                # In insert mode, insert the character without overwriting, respecting max_scroll_length
                if len(self.sid_data.localinput) < self.sid_data.max_scroll_length:
                    # Insert the character at the current position
                    self.sid_data.localinput = (self.sid_data.localinput[:self.sid_data.currentPos] + 
                                                key + 
                                                self.sid_data.localinput[self.sid_data.currentPos:])
                    self.sid_data.currentPos += 1
            else:
                # Overwrite mode
                if self.sid_data.currentPos < self.sid_data.max_scroll_length:
                    # Replace character at current position or append at the end
                    self.sid_data.localinput = (self.sid_data.localinput[:self.sid_data.currentPos] + 
                                                key + 
                                                self.sid_data.localinput[self.sid_data.currentPos + 1:])
                    self.sid_data.currentPos += 1

            # Update view_start based on max_scroll_length and maxLength
            if self.sid_data.currentPos > self.sid_data.maxLength - 1:
                self.sid_data.view_start = self.sid_data.currentPos - self.sid_data.maxLength + 1

            # Ensure view_start does not exceed the limit
            self.sid_data.view_start = min(self.sid_data.view_start, self.sid_data.max_scroll_length - self.sid_data.maxLength)

            # Cut the visible region from the input based on view_start and maxLength
            visible_str = self.sid_data.localinput[self.sid_data.view_start:self.sid_data.view_start + self.sid_data.maxLength]
            myoutput = visible_str if self.sid_data.inputType != 'password' else '*' * len(visible_str)

            # Emit the current string and set the cursor position
            self.emit_current_string(myoutput, 14, 4, False, self.sid_data.startX, self.sid_data.startY)

            # Adjust cursorX based on viewStart and current position
            adjusted_cursor_position = self.sid_data.currentPos - self.sid_data.view_start
            adjusted_cursor_position = min(adjusted_cursor_position, self.sid_data.maxLength - 1)
            self.sid_data.setCursorX(self.sid_data.startX + adjusted_cursor_position)
            self.emit_gotoXY(self.sid_data.cursorX, self.sid_data.cursorY)











    def show_file(self, data, emit_current_string):

        
        filename = data.get('filename', '') + '.ans'
    
        filepath = os.path.join('ansi', filename)

        if os.path.exists(filepath):
            with codecs.open(filepath, 'r', 'cp437') as f:
                text_content = f.read()

            ansi_code_bytes = bytes(text_content, 'cp437')

            sauce = self.get_sauce(ansi_code_bytes)

            ansi_code_bytes = self.strip_sauce(ansi_code_bytes)
            if sauce != None:
                if sauce.columns and sauce.rows:
                    self.sid_data.setSauceWidth(sauce.columns)
                    self.sid_data.setSauceHeight(sauce.rows)
                else:
                    self.sid_data.setSauceWidth(80)
                    self.sid_data.setSauceHeight(50)    
            else:
                self.sid_data.setSauceWidth(80)
                self.sid_data.setSauceHeight(50)
            ansi_code = ansi_code_bytes.decode('cp437')
            self.show_file_content(ansi_code, emit_current_string)


    def show_file_content(self, text_content, emit_current_string):
        self.sid_data.setMapCharacterSet(True)
        currentColor = 15
        backgroundColor = 0
        terminalWidth = 80

    
        terminalWidth = self.sid_data.sauceWidth

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
                    
                    currentColor = currentColor + 8 # Adding this makes the foreground color of the ANSI image appear
                    self.sid_data.setStartX(posX)
                    self.sid_data.setStartY(posY)
                    isBold = True  # Add this line
                elif instruction.attribute == Attribute.NORMAL:  # Add this line
                    isBold = False  # Add this line
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

    def strip_sauce(self, bytes):
        if len(bytes) < 128:
            return bytes

        # Check the SAUCE ID
        sauce_id = bytes[-128:][:7].decode("cp1252", errors="ignore")
        if sauce_id == "SAUCE00":
            # If there are comments, their length would be indicated in byte 104
            number_of_comments = bytes[-128:][104]
            additional_length = number_of_comments * 64 + 5 if number_of_comments else 0

            # Remove SAUCE and comments
            return bytes[:-(129 + additional_length)]
        else:
            return bytes

    def get_sauce(self, bytes):
        if len(bytes) >= 128:
            sauce_bytes = bytes[-128:]
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
        sauce.columns = 80
        sauce.rows = 50
        return sauce

    def append_sauce_to_string(self, sauce, string):
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
        #print("SAUCE Bytes in append_sauce_to_string:", sauce_bytes)
        #print("String Length Before:", len(string))
        if string[-129:-121].encode('cp1252') == b'\x1ASAUCE00':  # Updated indices and comparison string
            # Replace the existing SAUCE record
            string = string[:-129] + sauce_string  # Updated index to remove the existing SAUCE record
        else:
            # Append the SAUCE record
            string += sauce_string
        
        #print("String Length After:", len(string))
        #print("Last 1232 bytes after appending SAUCE:", string[-132:].encode('cp1252'))

        
        return string

    def set_color_at_position(self, x, y, color, bgcolor, color_array, color_bgarray):
        #print(f"Setting color at position: X={x}, Y={y}")
        
        # Expand the outer list (for y coordinate) as required
        while len(color_array) <= y:
            color_array.append([])
            #print(f"Expanding outer list to {len(color_array)} due to Y={y}")
            
        # Now, expand the inner list (for x coordinate) as required
        while len(color_array[y]) <= x:
            color_array[y].append(None)
            #print(f"Expanding inner list at Y={y} to {len(color_array[y])} due to X={x}")

        # Print current size
        #print(f"Current size of color_array: Width={len(color_array[y])}, Height={len(color_array)}")

        # Do the same for the background color array
        while len(color_bgarray) <= y:
            color_bgarray.append([])
            #print(f"Expanding outer bg list to {len(color_bgarray)} due to Y={y}")
            
        while len(color_bgarray[y]) <= x:
            color_bgarray[y].append(None)
            #print(f"Expanding inner bg list at Y={y} to {len(color_bgarray[y])} due to X={x}")

        # Print current size of bg array
        #print(f"Current size of color_bgarray: Width={len(color_bgarray[y])}, Height={len(color_bgarray)}")

        # Set the color and background color at the given coordinates
        color_array[y][x] = color
        color_bgarray[y][x] = bgcolor

        # Print successful setting of color
        #print(f"Successfully set color {color} and bgcolor {bgcolor} at X={x}, Y={y}")


    def emit_current_string_local(self, currentString, currentColor, backgroundColor, blink, current_x, current_y):
        if (current_y > self.sid_data.yHeight-4):
            return []
        if (current_x < 0):
            current_x = 0
        if (current_y < 0):
            current_y = 0
        for key in currentString:
            while len(self.sid_data.input_values) <= current_y:
                self.sid_data.input_values.append("")

            if not self.sid_data.input_values[current_y]:
                self.sid_data.input_values[current_y] = ""
            # Get the current string at the specified line index
            current_str = self.sid_data.input_values[current_y]
            # Check if the length of current_str[:current_x] is shorter than the position of current_x
            if len(current_str) <= current_x:
                # Pad current_str with spaces until its length matches current_x
                current_str += ' ' * (current_x - len(current_str) + 1)

            # Construct a new string with the changed character
            new_str = current_str[:current_x] + key + current_str[current_x + 1:]

            # Assign the new string back to the list
            self.sid_data.input_values[current_y] = new_str

            self.set_color_at_position(current_x+1, current_y, currentColor, backgroundColor, self.sid_data.color_array, self.sid_data.color_bgarray)
            
            #if self.current_line_x+1 < self.sid_data.xWidth:
            current_x = current_x+1
        return []
    
    def emit_current_string_2copy(self, currentString, currentColor, backgroundColor, blink, current_x, current_y):
            current_y -= 1
            if (current_x < 0):
                current_x = 0
            if (current_y < 0):
                current_y = 0
            for key in currentString:
                while len(self.sid_data.copy_input_values) <= current_y:
                    self.sid_data.copy_input_values.append("")

                if not self.sid_data.copy_input_values[current_y]:
                    self.sid_data.copy_input_values[current_y] = ""
                # Get the current string at the specified line index
                current_str = self.sid_data.copy_input_values[current_y]
                # Check if the length of current_str[:current_x] is shorter than the position of current_x
                if len(current_str) <= current_x:
                    # Pad current_str with spaces until its length matches current_x
                    current_str += ' ' * (current_x - len(current_str) + 1)

                # Construct a new string with the changed character
                new_str = current_str[:current_x] + key + current_str[current_x + 1:]

                # Assign the new string back to the list
                self.sid_data.copy_input_values[current_y] = new_str

                self.set_color_at_position(current_x+1, current_y, currentColor, backgroundColor, self.sid_data.copy_color_array, self.sid_data.copy_color_bgarray)
                # print("current_y:"+str(current_y))
                #if self.current_line_x+1 < self.sid_data.xWidth:
                current_x = current_x+1
            return []
    
    def statusinfo(self, message):
        self.emit_status_bar(message, 11, 4)

    def format_filename(self, filename, extension):
        filename = filename.upper()
        if '.' in filename:
            name, ext = filename.split('.', 1)
            name = name[:8]
            ext = ext[:3]
            return f"{name}.{ext}"
        else:
            return filename[:8]+"."+extension

    def choose_bbs(self, data):
        self.sid_data.setBBSChooser(BBSChooser(self))
        return
    
    def pointerdown(self, x, y):
        print(x)
        print(y)

    def emit_link(self, length, parameter, callback, callback_name, x, y, height = 1):
        """ Emit a socket event for an href link. """
        # Validate parameters
        if not isinstance(callback_name, str):
            raise ValueError("Callback name must be a string")
        if not callable(callback):
            raise ValueError("Callback must be a callable function")
        if not isinstance(x, int) or not isinstance(y, int):
            raise ValueError("Coordinates x and y must be integers")

        # Store the callback function and parameter in the dictionary
        self.sid_data.callbacks[callback_name] = {'callback': callback, 'parameter': parameter}

        # Emit the socket event
        self.socketio.emit('a', {
            'callback_name': callback_name,
            'x': x,
            'y': y,
            'length' : length,
            'height' : height
        }, room=self.request_id)

    def get_callback(self, callback_name):
        """ Retrieve a callback function by its name. """
        return self.sid_data.callbacks.get(callback_name, None)
    

    def handle_authentication(self):
        payload = {
            "user_id": str(self.sid_data.user_document['_id']),  # or any other user-specific information
            "chosen_bbs" : self.sid_data.chosen_bbs
            # You can add more claims here
            }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        self.socketio.emit('authentication', {'jwt_token': token}, room=self.request_id)


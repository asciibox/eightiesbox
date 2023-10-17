from pymongo import MongoClient
from menubar import MenuBar
import bson.binary
import base64
from bson.binary import Binary
import datetime

class MenuBarANSIEditor(MenuBar):
    def __init__(self, sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file_content, emit_upload, map_value, list1, list2, get_sauce, append_sauce_to_string, Sauce, strip_sauce):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file_content, emit_upload, get_sauce, append_sauce_to_string)
        # Add any additional properties or methods specific to MenuBarANSI here
        self.current_line_x = 0
        self.current_line_index = 0
        self.map_value = map_value
        self.list1 = list1
        self.list2 = list2
        self.file_data = None
        self.ansi_code = ""
        self.columns_x = 0
        self.columns_y = 0
        self.Sauce = Sauce
        self.strip_sauce = strip_sauce

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Load ANSI":
                self.load_ansi()
            elif selected_option=="Save ANSI":
                self.save_ansi()
            elif selected_option=="Delete ANSI":
                self.delete_ansi()
            elif selected_option=="Upload ANSI":
                self.upload_ansi()
            elif selected_option=="Import uploaded ANSI":
                self.import_ansi()
            elif selected_option=="Delete uploaded ANSI":
                self.delete_uploaded_ansi()
            elif selected_option=="Leave menu bar":
                self.leave_menu_bar()                
            elif selected_option=="Clear ANSI":
                self.clear_ansi()                
            else:
                print("Hello world")
            # Perform the action associated with selected_option here.
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()
    def clear_ansi(self):
        self.current_line_x=0
        self.sid_data.input_values=[]
        self.current_line_index=0
        self.sid_data.color_array = []
        self.sid_data.color_bgarray = []
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor()
        self.sid_data.ansi_editor.current_line_x=0
        self.sid_data.ansi_editor.current_line_index=0
        self.sid_data.setCurrentAction("wait_for_ansieditor")

    def upload_ansi(self):
        self.emit_upload()

    def load_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to load: ", 6,0)
        self.ask(20, self.load_filename_callback)  # filename_callback is the function to be called once filename is entered   
    
    def save_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to save: ", 6,0)
        self.ask(20, self.save_filename_callback)  # filename_callback is the function to be called once filename is entered

    def show_filenames(self, filenames):
        # Display filenames
        display_filenames = [doc['filename'][:11] for doc in filenames]  # Limit filenames to 11 characters

        for y in range(0, 7):
            for x in range(0, 7):
                idx = y * 7 + x
                if idx < len(display_filenames):
                    self.sid_data.setStartX(x * 12)  # Assuming each entry takes up 12 spaces
                    self.sid_data.setStartY(y + 3)  # Start from the 3rd line
                    self.output(display_filenames[idx], 6, 0)

    def save_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection

        # Before saving, you might want to check if this filename already exists and handle accordingly
        if collection.find_one({"filename": entered_filename}):
            # Filename already exists, handle accordingly (overwrite, prompt again, etc.)
            self.goto_next_line()
            self.output("File already exists!", 6, 0)
            self.goto_next_line()
            self.output("Please enter the filename to save: ", 6,0)
            self.ask(20, self.save_filename_callback)  # filename_callback is the function to be called once a filename is entered
        else:
            # Create a list containing each row and its y-coordinate
            self.ansi_code = self.sid_data.ansi_editor.display_ansi()
            # add sauce record if it does not exist already

            current_date = datetime.datetime.now()

            # Format the current date as a string in the desired format
            date_string = current_date.strftime("%Y%m%d")

            sauce = self.Sauce(
            columns=self.sid_data.sauceWidth,
            rows=self.sid_data.sauceHeight,
            title="",
            author="",
            group="",
            date=date_string,
            filesize=0,
            ice_colors=True,
            use_9px_font=True,
            font_name="IBM VGA",
            comments="Created with eightiesbox editor"
            )

            self.ansi_code = self.append_sauce_to_string(sauce, self.ansi_code)

            # Save the new file
            
            ansi_code_bytes = self.ansi_code.encode('cp1252')

            print("Last 128 bytes after decoding:", ansi_code_bytes[-128:])

            # Base64-encode the bytes
            ansi_code_base64 = base64.b64encode(ansi_code_bytes).decode('ascii')
        
            new_file_data = {
                "filename": entered_filename,
                "ansi_code": ansi_code_base64
                # Add other file details here
            }
            
            collection.insert_one(new_file_data)
            
            self.output("File saved successfully!", 6, 0)
            self.leave_menu_bar()
            self.in_sub_menu = False

    def load_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})
        
        self.file_data = file_data
        if file_data:
            # Decode the Base64-encoded string into bytes
            ansi_code_bytes = base64.b64decode(file_data['ansi_code'])
            print("Last 128 bytes after BASE64 decoding:", ansi_code_bytes[-128:])
            # Convert the bytes to a string using cp1252 encoding
           
            # Clear the existing values in MenuBox
            self.current_line_x=0
            self.sid_data.input_values=[]
            self.current_line_index=0
            self.sid_data.color_array = []
            self.sid_data.color_bgarray = []
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

            ansi_code = ansi_code_bytes.decode('cp1252')
            self.show_file_content(ansi_code, self.emit_current_string)
            self.sid_data.ansi_editor.max_height = len(self.sid_data.input_values)
            self.sid_data.ansi_editor.clear_screen()
            self.sid_data.ansi_editor.update_first_line()
            self.sid_data.ansi_editor.display_editor()
            self.sid_data.setCurrentAction("wait_for_ansieditor")
            self.sid_data.ansi_editor.current_line_x=0
            self.sid_data.ansi_editor.current_line_index=0
            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(20, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found

    def delete_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()
        
        self.show_filenames(filenames)
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to delete: ", 6, 0)
        self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

    def delete_uploaded_ansi(self):
        collection = self.mongo_client.bbs.uploads  # Replace with the actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()
        
        self.show_filenames(filenames)
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to delete: ", 6, 0)
        self.ask(20, self.delete_uploaded_ansi_callback)  # delete_filename_callback is the function to be called once filename is entered

    def delete_uploaded_ansi_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.uploads  # Replace with the actual MongoDB database and collection

        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})

        if file_data:
            # Delete the file from the database
            collection.delete_one({"filename": entered_filename})
            self.goto_next_line()
            self.output("File "+entered_filename+" deleted successfully!", 6, 0)
            self.goto_next_line()
            self.output("Please enter another filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.output("Please enter the filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called if the filename is not found


    def delete_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection

        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})

        if file_data:
            # Delete the file from the database
            collection.delete_one({"filename": entered_filename})
            self.goto_next_line()
            self.output("File "+entered_filename+" deleted successfully!", 6, 0)
            self.goto_next_line()
            self.output("Please enter another filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.output("Please enter the filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called if the filename is not found


    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_ansieditor")
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor()

    def emit_current_string(self, currentString, currentColor, backgroundColor, blink, current_x, current_y):
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

            self.set_color_at_position(current_x+1, current_y, currentColor, backgroundColor)
            
            #if self.current_line_x+1 < self.sid_data.xWidth:
            current_x = current_x+1
        return []
    

    def hide_menu_bar(self):
        self.in_sub_menu = False
        self.leave_menu_bar()
        # Reset to previous state or hide the menu bar

    def import_ansi(self):
        collection = self.mongo_client.bbs.uploads  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to load: ", 6,0)
        self.ask(20, self.import_filename_callback)  # filename_callback is the function to be called once filename is entered   

    def import_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.uploads  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})

        file_data = base64.b64decode(file_data['file_data'])
        if file_data:
            sauce = self.get_sauce(file_data)
            if sauce != None:
                print("FOUND")
                self.sid_data.setSauceWidth(sauce.columns)
                self.sid_data.setSauceHeight(sauce.rows)
            else:
                print("NOT FOUND")
                self.sid_data.setSauceWidth(80)
                self.sid_data.setSauceHeight(50)

            file_data = self.strip_sauce(file_data)

            file_data = self.convert_current_string(file_data)

            str_text = file_data.decode('cp1252')

            # Clear the existing values in MenuBox
            self.current_line_x=0
            self.sid_data.input_values=[]
            self.current_line_index=0
            self.sid_data.color_array = []
            self.sid_data.color_bgarray = []

            
            #str_text = file_data['file_data'].decode('cp437', 'replace')
            #with open("ansi_import.ans", "w", encoding='cp437') as f:
            #    f.write(str_text)
            self.show_file_content(str_text, self.emit_current_string)
            self.sid_data.ansi_editor.max_height = len(self.sid_data.input_values)
            self.sid_data.ansi_editor.clear_screen()
            self.sid_data.ansi_editor.update_first_line()
            self.sid_data.ansi_editor.display_editor()
            self.sid_data.setCurrentAction("wait_for_ansieditor")
            self.sid_data.ansi_editor.current_line_x=0
            self.sid_data.ansi_editor.current_line_index=0
            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(20, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found


    def convert_current_string(self, currentBytes):

        if currentBytes:
            ascii_codes = [b for b in currentBytes]
            #print(ascii_codes)
            mapped_ascii_codes = [self.map_value(code, self.list2, self.list1) for code in ascii_codes]

            # Convert the mapped ASCII codes back into a byte array
            new_bytes = bytes(mapped_ascii_codes)

            return new_bytes
        return bytes([])  # Return an empty byte array if there's no data
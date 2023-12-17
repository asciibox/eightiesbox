import binascii
from pymongo import MongoClient
from menubar import MenuBar
import bson.binary
import base64
from bson.binary import Binary
import datetime

''' When editing a ansi file '''
class MenuBarANSIEditor(MenuBar):
    def __init__(self, sub_menus, util):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        util.sid_data.setCurrentAction("wait_for_menubar_ansieditor")
        # Add any additional properties or methods specific to MenuBarANSI here
        self.current_line_x = 0
        self.current_line_index = 0
        self.map_value = util.map_value
        self.list1 = util.list1
        self.list2 = util.list2
        self.file_data = None
        self.ansi_code = ""
        self.columns_x = 0
        self.columns_y = 0
        self.strip_sauce = util.strip_sauce
        self.current_filename = ""
        

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Exit editor":
                self.exit_editor()
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
    
    def exit_editor(self):
        self.sid_data.menu.return_from_gosub()
        self.sid_data.setCurrentAction("wait_for_menu")
    
    def clear_ansi(self):
        self.current_line_x=0
        self.sid_data.input_values=[]
        self.current_line_index=0
        self.sid_data.color_array = []
        self.sid_data.color_bgarray = []
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)
        self.sid_data.ansi_editor.current_line_x=0
        self.sid_data.ansi_editor.current_line_index=0
        self.sid_data.setCurrentAction("wait_for_ansieditor")

    def upload_ansi(self):
        self.emit_uploadANSI()

    def load_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({'chosen_bbs' : self.sid_data.chosen_bbs}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output_wrap("Please enter the filename to load: ", 6,0)
        self.ask(20, self.load_filename_callback)  # filename_callback is the function to be called once filename is entered   
    
    def save_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({'chosen_bbs' : self.sid_data.chosen_bbs}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output_wrap("Please enter the filename to save: ", 6,0)
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
        entered_filename = self.util.format_filename(entered_filename, "ANS")
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
        self.current_filename = entered_filename
        # Check if the filename already exists
        if collection.find_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs}):
            self.goto_next_line()
            self.output("File "+entered_filename+" already exists!", 6, 0)
            self.goto_next_line()

            # Ask user if they want to overwrite the existing file
            self.util.askYesNo("Do you want to overwrite "+entered_filename+"?", self.overwrite_callback)
        else:
            # Save the file because it doesn't exist
            self.save_file(entered_filename)

    def overwrite_callback(self, response):
        if response.lower() == 'y':
            # User wants to overwrite, proceed with saving
            self.save_file(self.current_filename)
        else:
            # User doesn't want to overwrite, ask for a new filename
            self.goto_next_line()
            self.output_wrap("Please enter the filename to save: ", 6, 0)
            self.ask(20, self.save_filename_callback)

    def save_file(self, entered_filename):
            
            new_file_data = {
                "filename": entered_filename,
                "ansi_code": self.sid_data.ansi_editor.get_ansi_code_base64() if self.sid_data.ansi_editor else "",
                'chosen_bbs' : self.sid_data.chosen_bbs
                # Add other file details here
            }
            collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
            # Delete any existing file with the same filename
            collection.delete_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})
            
            collection.insert_one(new_file_data)
            
            self.output_wrap("File saved successfully!", 6, 0)
            self.leave_menu_bar()
            self.in_sub_menu = False

    def load_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        entered_filename = entered_filename.upper()
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})
        
        self.file_data = file_data
        if file_data:
            # Decode the Base64-encoded string into bytes
            try:
                # Attempt to encode to bytes, if it's a string, then decode from base64
                if isinstance(file_data['ansi_code'], str):
                    ansi_code_bytes = base64.b64decode(file_data['ansi_code'].encode('utf-8'))
                else:
                    ansi_code_bytes = base64.b64decode(file_data['ansi_code'])
            except (TypeError, KeyError, binascii.Error, ValueError, UnicodeEncodeError) as e:
                print(f"An error occurred: {e}")
                ansi_code_bytes = b""
            print("Last 128 bytes after BASE64 decoding:", ansi_code_bytes[-128:])
            # Convert the bytes to a string using cp1252 encoding
           
            # Clear the existing values in MenuBox
            self.current_line_x=0
            self.sid_data.input_values=[]
            self.current_line_index=0
            self.sid_data.color_array = []
            self.sid_data.color_bgarray = []
            sauce = self.util.get_sauce(ansi_code_bytes)

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
            self.show_file_content(ansi_code, self.util.emit_current_string_local)
            self.display_ansi_file()
            
        else:
            self.goto_next_line()
            self.output_wrap("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(20, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found

    def display_ansi_file(self):
        self.sid_data.ansi_editor.max_height = len(self.sid_data.input_values)
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)
        self.sid_data.setCurrentAction("wait_for_ansieditor")
        self.sid_data.ansi_editor.current_line_x=0
        self.sid_data.ansi_editor.current_line_index=0

    def delete_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection
        filenames = collection.find({'chosen_bbs' : self.sid_data.chosen_bbs}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()
        
        self.show_filenames(filenames)
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output_wrap("Please enter the filename to delete: ", 6, 0)
        self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

    def delete_uploaded_ansi(self):
        collection = self.mongo_client.bbs.uploads  # Replace with the actual MongoDB database and collection
        filenames = collection.find({'chosen_bbs' : self.sid_data.chosen_bbs}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()
        
        self.show_filenames(filenames)
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output_wrap("Please enter the filename to delete: ", 6, 0)
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
            collection.delete_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})
            self.goto_next_line()
            self.output_wrap("File "+entered_filename+" deleted successfully!", 6, 0)
            self.goto_next_line()
            self.output_wrap("Please enter another filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

        else:
            self.goto_next_line()
            self.output_wrap("File not found!", 6, 0)
            self.goto_next_line()
            self.output_wrap("Please enter the filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called if the filename is not found


    def delete_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.ansifiles  # Replace with the actual MongoDB database and collection

        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})

        if file_data:
            # Delete the file from the database
            collection.delete_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})
            self.goto_next_line()
            self.output_wrap("File "+entered_filename+" deleted successfully!", 6, 0)
            self.goto_next_line()
            self.output_wrap("Please enter another filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

        else:
            self.goto_next_line()
            self.output_wrap("File not found!", 6, 0)
            self.goto_next_line()
            self.output_wrap("Please enter the filename to delete: ", 6, 0)
            self.ask(20, self.delete_filename_callback)  # delete_filename_callback is the function to be called if the filename is not found


    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_ansieditor")
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)

    def hide_menu_bar(self):
        self.in_sub_menu = False
        self.leave_menu_bar()
        # Reset to previous state or hide the menu bar

    def import_ansi(self):
        collection = self.mongo_client.bbs.uploads_ansi  # Replace with actual MongoDB database and collection
        filenames = collection.find({'chosen_bbs' : self.sid_data.chosen_bbs}, {'filename': 1})  # Query MongoDB for filenames
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output_wrap("Please enter the filename to load: ", 6,0)
        self.ask(20, self.import_filename_callback)  # filename_callback is the function to be called once filename is entered   

    def import_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.leave_menu_bar()
            self.in_sub_menu = False
            return
        entered_filename = entered_filename.upper()
        collection = self.mongo_client.bbs.uploads_ansi  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename, 'chosen_bbs' : self.sid_data.chosen_bbs})

        try:
            file_data = base64.b64decode(file_data['file_data'])
        except (TypeError, KeyError, binascii.Error) as e:
            print(f"An error occurred while decoding: {e}")
            file_data = b""  # Initialize as empty bytes
        if file_data:

            sauce = self.get_sauce(file_data)
            if sauce != None:
                self.sid_data.setSauceWidth(sauce.columns)
                self.sid_data.setSauceHeight(sauce.rows)
            else:
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
            self.show_file_content(str_text, self.util.emit_current_string_local)
            self.display_ansi_file()
            
        else:
            self.goto_next_line()
            self.output_wrap("File not found!", 6, 0)
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
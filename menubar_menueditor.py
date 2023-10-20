from pymongo import MongoClient
from menutexteditor import *
from menubar import MenuBar
from menu import Menu

''' When editing a menu '''
class MenuBarMenuEditor(MenuBar):
    def __init__(self, sub_menus, util):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_menueditor")
        self.current_filename = ""

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Leave menu bar":
                self.hide_menu_bar()
            elif selected_option=="Load menu":
                self.load_menu()
            elif selected_option=="Save menu":
                self.save_menu()
            elif selected_option=="New menu":
                self.new_menu()
            elif selected_option=="Delete menu":
                self.delete_menu()
            elif selected_option=="Edit text":
                self.edit_text()     
            elif selected_option=="Simulate text":
                self.simulate_text()
            else:
                print("Hello world")
            
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def simulate_text(self):
        self.sid_data.setMenu(Menu(self.util))
        self.util.clear_screen()
        self.sid_data.menu.display_editor()

    def new_menu(self):
        self.sid_data.menu_box.new_menu()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False

    def show_filenames(self, filenames):
        # Display filenames
        display_filenames = [doc['filename'][:12] for doc in filenames]  # Limit filenames to 11 characters

        for y in range(0, 7):
            for x in range(0, 7):
                idx = y * 7 + x
                if idx < len(display_filenames):
                    self.sid_data.setStartX(x * 12)  # Assuming each entry takes up 12 spaces
                    self.sid_data.setStartY(y + 3)  # Start from the 3rd line
                    self.output(display_filenames[idx], 6, 0)

    def load_menu(self):
        collection = self.mongo_client.bbs.menufiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to load: ", 6,0)
        self.ask(11, self.load_filename_callback)  # filename_callback is the function to be called once filename is entered   
    
    def save_menu(self):
        collection = self.mongo_client.bbs.menufiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames

        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to save: ", 6, 0)
        self.ask(11, self.save_filename_callback)  # filename_callback is the function to be called once filename is entered


    def save_filename_callback(self, entered_filename):
        
        if entered_filename == '':
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False
            return
        entered_filename = self.util.format_filename(entered_filename)
        self.current_filename = entered_filename

        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection

        # Check if this filename already exists
        if collection.find_one({"filename": entered_filename}):
            self.goto_next_line()
            self.output("File "+entered_filename+" already exists!", 6, 0)
            self.goto_next_line()

            # Ask user if they want to overwrite the existing file
            self.util.askYesNo("Do you want to overwrite "+entered_filename+" ?", self.overwrite_callback)
        else:
            self.save_file(entered_filename)


    def overwrite_callback(self, response):
        if response.lower() == 'y':
            # User wants to overwrite, proceed with saving
            self.save_file(self.current_filename)
        else:
            # User doesn't want to overwrite, ask for a new filename
            self.goto_next_line()
            self.output("Please enter the filename to save: ", 6, 0)
            self.ask(11, self.save_filename_callback)


    def save_file(self, entered_filename):
        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection

        # Delete any existing file with the same filename
        collection.delete_one({"filename": entered_filename})

        # Create a list containing each row and its y-coordinate
        non_empty_values = [{"y": y, "row_data": row} for y, row in enumerate(self.sid_data.menu_box.values) if row]

        # Save the new file
        menu_box_data = {
            "fields": self.sid_data.menu_box.fields,
            "values": non_empty_values,
        }

        new_file_data = {
            "filename": entered_filename,
            "menu_box_data": menu_box_data,
            "ansi_code_base64": self.sid_data.menutexteditor.get_ansi_code_base64() if self.sid_data.menutexteditor else ""
            # Add other file details here
        }

        collection.insert_one(new_file_data)

        self.output("File saved successfully!", 6, 0)
        self.sid_data.menu_box.draw_all_rows()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False


    def load_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})
        
        if file_data:
            # Clear the existing values in MenuBox
            self.sid_data.menu_box.values = [["" for _ in self.sid_data.menu_box.fields] for _ in range(self.sid_data.menu_box.num_rows)]
            
            # Retrieve the saved MenuBox data
            menu_box_data = file_data.get("menu_box_data", {})
            
            # Populate the fields
            self.sid_data.menu_box.fields = menu_box_data.get("fields", [])
            
            ansi_code_base64 = file_data.get("ansi_code_base64")

            ansi_code_bytes = base64.b64decode(ansi_code_base64)
            
            self.sid_data.setMenuTextEditor(MenuTextEditor(self.util))
            self.sid_data.menutexteditor.current_line_x=0
            self.sid_data.input_values=[]
            self.sid_data.menutexteditor.current_line_index=0
            
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
            self.show_file_content(ansi_code, self.util.emit_current_string_local)

            # Populate the values at their respective y-coordinates
            for row in menu_box_data.get("values", []):
                y = row.get('y', 0)
                row_data = row.get('row_data', [])
                self.sid_data.menu_box.values[y] = row_data
                
            self.output("File loaded successfully!", 6, 0)
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False
            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(11, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found

    def delete_menu(self):
        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()
        
        self.show_filenames(filenames)
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to delete: ", 6, 0)
        self.ask(11, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered


    def delete_filename_callback(self, entered_filename):
        if entered_filename=='':
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False
            return
        collection = self.mongo_client.bbs.menufiles  # Replace with the actual MongoDB database and collection

        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})

        if file_data:
            # Delete the file from the database
            collection.delete_one({"filename": entered_filename})
            self.goto_next_line()
            self.output("File "+entered_filename+" deleted successfully!", 6, 0)
            self.goto_next_line()
            self.output("Please enter another filename to delete: ", 6, 0)
            self.ask(11, self.delete_filename_callback)  # delete_filename_callback is the function to be called once filename is entered

        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.output("Please enter the filename to delete: ", 6, 0)
            self.ask(11, self.delete_filename_callback)  # delete_filename_callback is the function to be called if the filename is not found


    def hide_menu_bar(self):
        self.sid_data.menu_box.draw_all_rows()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False
        # Reset to previous state or hide the menu bar

    def edit_text(self):
        self.sid_data.setCurrentAction("wait_for_menutexteditor")
        if self.util.sid_data.menutexteditor == None:
            self.util.sid_data.setMenuTextEditor(MenuTextEditor(self.util))
        self.util.sid_data.menutexteditor.start()

    def load_ansi(self):
        collection = self.mongo_client.bbs.ansifiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to load: ", 6,0)
        self.ask(20, self.load_ansi_callback)  # filename_callback is the function to be called once filename is entered   
    
    def leave_menu_bar(self):
        self.sid_data.menu_box.draw_all_rows()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False

        

    def load_ansi_callback(self, entered_filename):
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
            self.sid_data.ansi_editor.current_line_x=0
            self.sid_data.ansi_editor.current_line_index=0
            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(20, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found

    
    
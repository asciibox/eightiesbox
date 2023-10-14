from pymongo import MongoClient
from menutexteditor import *
from menubar import MenuBar

class MenuBarMenuEditor(MenuBar):
    def __init__(self, sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file)
        # Add any additional properties or methods specific to MenuBarANSI here
        

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
            else:
                print("Hello world")
            # Perform the action associated with selected_option here.
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def new_menu(self):
        self.sid_data.menu_box.new_menu()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False

    def load_menu(self):
        collection = self.mongo_client.mydatabase.menufiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to load: ", 6,0)
        self.ask(11, self.load_filename_callback)  # filename_callback is the function to be called once filename is entered   
    
    def save_menu(self):
        collection = self.mongo_client.mydatabase.menufiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames
        
        self.clear_screen()

        self.show_filenames(filenames)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.output("Please enter the filename to save: ", 6,0)
        self.ask(11, self.save_filename_callback)  # filename_callback is the function to be called once filename is entered

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
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False
            return
        collection = self.mongo_client.mydatabase.menufiles  # Replace with the actual MongoDB database and collection

        # Before saving, you might want to check if this filename already exists and handle accordingly
        if collection.find_one({"filename": entered_filename}):
            # Filename already exists, handle accordingly (overwrite, prompt again, etc.)
            self.goto_next_line()
            self.output("File already exists!", 6, 0)
            self.goto_next_line()
            self.output("Please enter the filename to save: ", 6,0)
            self.ask(11, self.filename_callback)  # filename_callback is the function to be called once a filename is entered
        else:
            # Create a list containing each row and its y-coordinate
            non_empty_values = [{"y": y, "row_data": row} for y, row in enumerate(self.sid_data.menu_box.values)]
            
            # Save the new file
            menu_box_data = {
                "fields": self.sid_data.menu_box.fields,
                "values": non_empty_values,
            }
            
            new_file_data = {
                "filename": entered_filename,
                "menu_box_data": menu_box_data,
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
        collection = self.mongo_client.mydatabase.menufiles  # Replace with the actual MongoDB database and collection
        
        # Look for the filename in the database
        file_data = collection.find_one({"filename": entered_filename})
        
        if file_data:
            # Clear the existing values in MenuBox
            self.sid_data.menu_box.values = [["" for _ in self.sid_data.menu_box.fields] for _ in range(self.sid_data.menu_box.num_rows)]
            
            # Retrieve the saved MenuBox data
            menu_box_data = file_data.get("menu_box_data", {})
            
            # Populate the fields
            self.sid_data.menu_box.fields = menu_box_data.get("fields", [])
            
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
        collection = self.mongo_client.mydatabase.menufiles  # Replace with the actual MongoDB database and collection
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
        collection = self.mongo_client.mydatabase.menufiles  # Replace with the actual MongoDB database and collection

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

    def edit_text(self):
        self.sid_data.setCurrentAction("wait_for_menutexteditor")
        self.sid_data.setMenuTextEditor(MenuTextEditor(self.sid_data, self.output, self.ask, self.goto_next_line, self.clear_screen, self.emit_gotoXY, self.clear_line))

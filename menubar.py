from pymongo import MongoClient

class MenuBar:
    def __init__(self, sid_data, output_function, ask_function, mongo_client, goto_next_line):
        self.mongo_client = mongo_client
        self.sid_data = sid_data
        sid_data.setCurrentAction("wait_for_menubar")
        self.output = output_function
        self.ask = ask_function
        self.goto_next_line = goto_next_line

        self.current_main_menu_index = 0
        self.current_sub_menu_index = 0
        self.in_sub_menu = False  # Flag to determine if in sub-menu
        
        self.current_x = 0  # To keep track of the current x-coordinate
        
        # Define main menu and sub-menus
        self.main_menu = ['File', 'Edit']
        self.sub_menus = {
            'File': ['Load menu', 'Save menu', 'New menu'],
            'Edit': ['Edit text', 'Simulate text', 'Clear text', 'View text', 'Leave menu bar'],
        }
        self.main_menu_positions = {}

        # Clear the lines where the sub-menus would appear
        max_sub_menu_length = max([len(sub) for sub in self.sub_menus.values()])
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)  # Assuming sub-menus start at y=1
        for i in range(max_sub_menu_length):
            print("I:"+str(i))
            self.sid_data.setStartY(i)  # Move down one line
            self.sid_data.setStartX(0)  # Move to the start
            self.output(" " * sid_data.xWidth, 6, 0)
            
            
        self.draw_menu_bar()

    def draw_menu_bar(self):
        x = 0
        max_x = self.sid_data.xWidth  # Assuming xWidth contains the max width of the display
        
        # Clear the entire menu bar line first
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        self.output(" " * max_x, 6, 0)

        # Draw the visible menus
        for idx, menu in enumerate(self.main_menu):
            if x >= max_x:
                break  # Stop drawing menus if we've reached the max width
            
            self.sid_data.setStartX(x)
            self.sid_data.setStartY(0)
            
            color = 1 if idx == self.current_main_menu_index else 7  # Highlight if this menu is selected
            self.output(menu, color, 0)
            
            max_length = max([len(item) for item in self.sub_menus[menu]])
            self.main_menu_positions[menu] = x
            
            x += max_length + 2  # Update x to the end of this menu's longest sub-item + padding
            
            
    def draw_sub_menu(self):
        current_menu = self.main_menu[self.current_main_menu_index]
        sub_menu_items = self.sub_menus[current_menu]
        
        self.current_x = self.main_menu_positions[current_menu]  # Get the x starting point for this menu

        for idx, item in enumerate(sub_menu_items):
            self.sid_data.setStartX(self.current_x)
            self.sid_data.setStartY(1 + idx)

            color = 1 if idx == self.current_sub_menu_index else 7  # Highlight if this sub-menu item is selected
            self.output(item, color, 0)

    def hide_menu(self):
        # Clear the main menu line
        max_x = self.sid_data.xWidth  # Assuming xWidth contains the max width of the display
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        self.output(" " * max_x, 6, 0)
        
        # Clear the sub-menu lines
        max_sub_menu_length = max([len(sub) for sub in self.sub_menus.values()])
        for i in range(max_sub_menu_length):
            self.sid_data.setStartY(1 + i)  # Move down one line
            self.sid_data.setStartX(0)  # Move to the start
            self.output(" " * max_x, 6, 0)

    def arrow_left(self):
        self.hide_menu()
        self.current_main_menu_index = (self.current_main_menu_index - 1) % len(self.main_menu)
        self.draw_menu_bar()
        self.draw_sub_menu()

    def arrow_right(self):
        self.hide_menu()
        self.current_main_menu_index = (self.current_main_menu_index + 1) % len(self.main_menu)
        self.draw_menu_bar()
        self.draw_sub_menu()

    def arrow_up(self):
        if self.in_sub_menu:
            self.current_sub_menu_index = (self.current_sub_menu_index - 1) % len(self.sub_menus[self.main_menu[self.current_main_menu_index]])
            self.draw_sub_menu()

    def arrow_down(self):
        if self.in_sub_menu:
            self.current_sub_menu_index = (self.current_sub_menu_index + 1) % len(self.sub_menus[self.main_menu[self.current_main_menu_index]])
            self.draw_sub_menu()

    def choose_field(self):
        if self.in_sub_menu:
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_index]
            if selected_option=="Leave menu bar":
                self.hide_menu_bar()
            elif selected_option=="Save menu":
                self.save_menu()
            elif selected_option=="New menu":
                self.new_menu()
            else:
                print("Hello world")
            # Perform the action associated with selected_option here.
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def hide_menu_bar(self):
        self.sid_data.menu_box.draw_all_rows()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False
        # Reset to previous state or hide the menu bar
    
    def new_menu(self):
        self.sid_data.menu_box.new_menu()
        self.sid_data.setCurrentAction("wait_for_menu")
        self.in_sub_menu = False      
    
    def save_menu(self):
        collection = self.mongo_client.mydatabase.myfiles  # Replace with actual MongoDB database and collection
        filenames = collection.find({}, {'filename': 1})  # Query MongoDB for filenames

        # Display filenames
        display_filenames = [doc['filename'][:11] for doc in filenames]  # Limit filenames to 11 characters

        for y in range(0, 7):
            for x in range(0, 7):
                idx = y * 7 + x
                if idx < len(display_filenames):
                    self.sid_data.setStartX(x * 12)  # Assuming each entry takes up 12 spaces
                    self.sid_data.setStartY(y + 3)  # Start from the 3rd line
                    self.output(display_filenames[idx], 6, 0)

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(10)  # Assuming you are asking at the 10th line
        self.ask(40, self.filename_callback)  # filename_callback is the function to be called once filename is entered

    def filename_callback(self, entered_filename):
        # Here you can save the entered_filename to MongoDB or take other actions
        collection = self.mongo_client.mydatabase.myfiles  # Replace with actual MongoDB database and collection

        # Before saving, you might want to check if this filename already exists and handle accordingly
        if collection.find_one({"filename": entered_filename}):
            # Filename already exists, handle accordingly (overwrite, prompt again, etc.)
            self.goto_next_line()
            self.output("File already exists!", 6, 0)
            self.goto_next_line()
            self.ask(40, self.filename_callback)  # filename_callback is the function to be called once filename is entered
        else:
            # Save the new file
            new_file_data = {
                "filename": entered_filename,
                # Add other file details here
            }
            collection.insert_one(new_file_data)
            self.output("File saved successfully!", 6, 0)
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            self.in_sub_menu = False

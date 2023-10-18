from pymongo import MongoClient
from menubar import MenuBar
from menubar_ansieditor import MenuBarANSIEditor
import base64

''' When editing a menu ansi file '''

class MenuBarTextEditor(MenuBarANSIEditor):
    def __init__(self, sub_menus, util):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_menutexteditor")

        # Add ANSI-specific methods here if needed

    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_menutexteditor")
        self.sid_data.menutexteditor.clear_screen()
        self.sid_data.menutexteditor.update_first_line()
        self.sid_data.menutexteditor.display_editor()

    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Leave menu bar":
                self.hide_menu_bar()            
            if selected_option=="Load ANSI":
                self.load_ansi()          
            if selected_option=="Leave ANSI editor":
                self.leave_ansi_editor()            
            elif selected_option=="Import uploaded ANSI":
                self.import_ansi()
            else:
                print("Hello world")
            
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def hide_menu_bar(self):
        self.in_sub_menu = False
        self.leave_menu_bar()
        # Reset to previous state or hide the menu bar

    def leave_ansi_editor(self):
         self.sid_data.setCurrentAction("wait_for_menu")
         self.sid_data.menu_box.clear_screen()
         self.sid_data.menu_box.draw_all_rows()

    def display_ansi_file(self):
        self.sid_data.menutexteditor.max_height = len(self.sid_data.input_values)
        self.sid_data.menutexteditor.clear_screen()
        self.sid_data.menutexteditor.update_first_line()
        self.sid_data.menutexteditor.display_editor()
        self.sid_data.setCurrentAction("wait_for_menutexteditor")
        self.sid_data.menutexteditor.current_line_x=0
        self.sid_data.menutexteditor.current_line_index=0

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

        if file_data:
            file_data = base64.b64decode(file_data['file_data'])
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

            self.show_file_content(str_text, self.util.emit_current_string_local)
            self.sid_data.menutexteditor.start()
            self.sid_data.setCurrentAction("wait_for_menutexteditor")
            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
            self.goto_next_line()
            self.ask(20, self.load_filename_callback)  # load_filename_callback is the function to be called if the filename is not found
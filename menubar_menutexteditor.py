from pymongo import MongoClient
from menubar import MenuBar
from menubar_ansieditor import MenuBarANSIEditor

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
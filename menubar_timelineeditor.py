from pymongo import MongoClient
from menubar import MenuBar
from menubar_ansieditor import MenuBarANSIEditor
import base64

''' When editing a timeline entry '''

class MenuBarTimelineEditor(MenuBarANSIEditor):
    def __init__(self, sub_menus, util):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_timelineeditor")

        # Add ANSI-specific methods here if needed

    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_timelineeditor")
        self.util.clear_screen()
        # Optionally, redraw the editor to reflect these changes on the screen
        self.sid_data.timeline.display_editor()

    def hide_menu_bar(self):
        self.in_sub_menu = False
        self.leave_menu_bar()
        # Reset to previous state or hide the menu bar

    # 'Save timeline entry', 'Exit without saving'],
    # 'Edit': ['Clear timeline entry', 'Leave menu bar'],
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Save timeline entry":
                self.save_timeline_entry()    
                return        
            if selected_option=="Exit without saving":
                self.exit_message_editor()          
                return
            if selected_option=="Clear timeline entry":
                self.clear_text()            
                return
            if selected_option=="Leave menu bar":
                self.hide_menu_bar()            
                return
            else:
                pass
            
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def save_timeline_entry(self):
        self.util.clear_screen()
        self.sid_data.timeline.save_timeline_entry()
        #self.sid_data.setCurrentAction("wait_for_menu")
        #self.sid_data.menu.return_from_gosub()
        
    def exit_message_editor(self):
        self.util.emit_waiting_for_input(False, 8)
        self.sid_data.setCurrentAction("wait_for_menu")
        self.sid_data.menu.return_from_gosub()

    def clear_text(self):
        # Clear the input values
        self.sid_data.input_values = []
        
        # Clear the color array
        self.sid_data.color_array = []

        # Clear the background color array
        self.sid_data.color_bgarray = []

        self.sid_data.timeline.set_text_values([], [], [],[])

        self.hide_menu_bar()


from pymongo import MongoClient
from menutexteditor import *

class MenuBar:
    def __init__(self, sub_menus, util):
        util.sid_data.setCurrentAction("wait_for_menubar_menueditor")
        self.util = util
        self.mongo_client = util.mongo_client
        self.clear_screen = util.clear_screen
        self.sid_data = util.sid_data
        
        self.output_wrap = util.output_wrap
        self.output = util.output
        self.ask = util.ask
        self.goto_next_line = util.goto_next_line
        self.emit_gotoXY = util.emit_gotoXY
        self.opened_menu = False

        self.current_main_menu_index = 0
        self.in_sub_menu = False  # Flag to determine if in sub-menu
        
        self.current_x = 0  # To keep track of the current x-coordinate
        self.clear_line = util.clear_line
        
        # Define main menu and sub-menus
        self.main_menu = ['File', 'Edit']
        self.current_sub_menu_indexes = [0,0]
        self.sub_menus = sub_menus
        self.main_menu_positions = {}

        self.show_file_content = util.show_file_content
        self.emit_uploadANSI = util.emit_uploadANSI
        self.get_sauce = util.get_sauce
        self.append_sauce_to_string = util.append_sauce_to_string
        
        self.strip_sauce = util.strip_sauce
        
        # Clear the lines where the sub-menus would appear
        max_sub_menu_length = max([len(sub) for sub in self.sub_menus.values()])
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)  # Assuming sub-menus start at y=1
        for i in range(max_sub_menu_length):
            self.sid_data.setStartY(i)  # Move down one line
            self.sid_data.setStartX(0)  # Move to the start
            self.output(" " * self.sid_data.xWidth, 6, 0)
            
            
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

            color = 1 if idx == self.current_sub_menu_indexes[self.current_main_menu_index] else 7  # Highlight if this sub-menu item is selected
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
        self.in_sub_menu = True
        self.draw_sub_menu()

    def arrow_right(self):
        self.hide_menu()
        self.current_main_menu_index = (self.current_main_menu_index + 1) % len(self.main_menu)
        self.draw_menu_bar()
        self.in_sub_menu = True
        self.draw_sub_menu()

    def arrow_up(self):
            current_menu = self.current_main_menu_index
            self.current_sub_menu_indexes[current_menu] = (self.current_sub_menu_indexes[current_menu] - 1) % len(self.sub_menus[self.main_menu[self.current_main_menu_index]])
            self.draw_sub_menu()
            self.in_sub_menu = True

    def arrow_down(self):
            current_menu = self.current_main_menu_index
            self.current_sub_menu_indexes[current_menu] = (self.current_sub_menu_indexes[current_menu] + 1) % len(self.sub_menus[self.main_menu[self.current_main_menu_index]])
            self.draw_sub_menu()
            self.in_sub_menu = True

    def exit(self):
        #self.util.emit_waiting_for_input(False, 9)
        self.sid_data.menu.return_from_gosub()
        self.util.sid_data.setCurrentAction("wait_for_menu")
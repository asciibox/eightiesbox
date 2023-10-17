from pymongo import MongoClient
from menutexteditor import *

class MenuBar:
    def __init__(self, sub_menus, util):
        util.sid_data.setCurrentAction("wait_for_menubar_menueditor")
        self.util = util
        self.mongo_client = util.mongo_client
        self.clear_screen = util.clear_screen
        self.sid_data = util.sid_data
        
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
        self.sub_menus = sub_menus;
        self.main_menu_positions = {}

        self.show_file_content = util.show_file_content
        self.emit_upload = util.emit_upload
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
        print("ANSI")
        print(self.sid_data.ansi_editor_values)
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

    def set_color_at_position(self, x, y, color, bgcolor):
        #print(f"Setting color at position: X={x}, Y={y}")
        
        # Expand the outer list (for y coordinate) as required
        while len(self.sid_data.color_array) <= y:
            self.sid_data.color_array.append([])
            #print(f"Expanding outer list to {len(self.sid_data.color_array)} due to Y={y}")
            
        # Now, expand the inner list (for x coordinate) as required
        while len(self.sid_data.color_array[y]) <= x:
            self.sid_data.color_array[y].append(None)
            #print(f"Expanding inner list at Y={y} to {len(self.sid_data.color_array[y])} due to X={x}")

        # Print current size
        #print(f"Current size of color_array: Width={len(self.sid_data.color_array[y])}, Height={len(self.sid_data.color_array)}")

        # Do the same for the background color array
        while len(self.sid_data.color_bgarray) <= y:
            self.sid_data.color_bgarray.append([])
            #print(f"Expanding outer bg list to {len(self.sid_data.color_bgarray)} due to Y={y}")
            
        while len(self.sid_data.color_bgarray[y]) <= x:
            self.sid_data.color_bgarray[y].append(None)
            #print(f"Expanding inner bg list at Y={y} to {len(self.sid_data.color_bgarray[y])} due to X={x}")

        # Print current size of bg array
        #print(f"Current size of color_bgarray: Width={len(self.sid_data.color_bgarray[y])}, Height={len(self.sid_data.color_bgarray)}")

        # Set the color and background color at the given coordinates
        self.sid_data.color_array[y][x] = color
        self.sid_data.color_bgarray[y][x] = bgcolor

        # Print successful setting of color
        #print(f"Successfully set color {color} and bgcolor {bgcolor} at X={x}, Y={y}")



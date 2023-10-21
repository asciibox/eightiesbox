from basicansi import BasicANSI
import base64
import copy
from messageareamenu import *
from fileareamenu import *
from usereditor import *
from messageeditor import MessageEditor
from ansieditor import ANSIEditor
from menubox import MenuBox
from messageareachange import MessageAreaChange
from messagereader import MessageReader

class Menu(BasicANSI):
    def __init__(self, util, values, num_rows, callback_on_exit):
        super().__init__(util)
        util.sid_data.setCurrentAction("wait_for_menu")
        self.values = values
        self.num_rows = num_rows
        self.callback_on_exit = callback_on_exit
        self.menu_stack = []  # Initialize the menu stack

    def message_menu_callback_on_exit(self):
        self.util.sid_data.setCurrentAction("wait_for_menu")
        self.util.clear_screen()
        self.display_editor()

    def user_editor_callback_on_exit(self):
        self.util.sid_data.setCurrentAction("wait_for_menu")
        self.util.clear_screen()
        self.display_editor()

    def message_editor_callback_on_exit(self):
        self.util.sid_data.setCurrentAction("wait_for_menu")
        self.util.clear_screen()
        self.display_editor()

    def handle_key(self, key):
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return
        
        if (key == 'Escape'):
            self.callback_on_exit()
            return
            
        key = key.lower()
        if len(key) == 1:  # Check if it's a single character input
            print(key)
            for row_idx in range(self.num_rows):
                if  self.values[row_idx][2].lower()==key:
                    # Mimic switch statement for values "00" and "01"
                    action_code = self.values[row_idx][0]
                    if action_code == "01":
                        filename = self.values[row_idx][1]
                        self.load_menu(filename)
                        return
                    elif action_code == "11":
                        self.append_gosub()
                        if self.sid_data.current_message_area is None:
                            self.sid_data.setMessageAreaChange(MessageAreaChange(self.util, self.on_message_area_selected_11))
                            self.sid_data.message_area_change.show_message_areas()
                            return
                        else:
                            self.execute_action_11()
                    elif action_code == "12":
                        self.append_gosub()
                        if self.sid_data.current_message_area is None:
                            self.sid_data.setMessageAreaChange(MessageAreaChange(self.util, self.on_message_area_selected_12))
                            self.sid_data.message_area_change.show_message_areas()
                            return
                        else:
                            self.execute_action_12()
                    elif action_code == "13":
                        self.sid_data.setMessageAreaChange(MessageAreaChange(self.util))
                        self.sid_data.message_area_change.show_message_areas()
                        return
                    elif action_code == "81":
                        
                        self.sid_data.setMessageAreaMenu(MessageAreaMenu(self.util, self.message_menu_callback_on_exit))
                        return
                    elif action_code == "82":
                        
                        self.sid_data.setFileAreaMenu(FileAreaMenu(self.util, self.message_menu_callback_on_exit))
                        return
                    elif action_code == "83":                        
                        # Example usage:
                        # Replace 'util' with your actual utility object
                        self.sid_data.setUserEditor(UserEditor(self.util, self.user_editor_callback_on_exit))
                        return
                    elif action_code == "84":         
                        # Example usage:
                        # Replace 'util' with your actual utility object
                        self.append_gosub()
                        self.sid_data.setANSIEditor(ANSIEditor(self.util))

                        self.sid_data.setCurrentAction("wait_for_ansieditor")
                        # Clear the editor
                        self.sid_data.input_values = []
                        self.sid_data.color_array = []
                        self.sid_data.color_bgarray = []
                        self.sid_data.ansi_editor.start()
                        return
                    elif action_code == "85":        
                        # Example usage:
                        # Replace 'util' with your actual utility object
                        self.sid_data.setMenuBox(MenuBox(self.util))
                        self.sid_data.setCurrentAction("wait_for_menubox")
                        self.sid_data.menu_box.clear_screen()
                        self.sid_data.menu_box.draw_all_rows()
                        return

                    # Gosub menu
                    elif action_code == "02":
                        # Gosub menu
                        # Save current state to stack
                        self.append_gosub()
                        filename = self.values[row_idx][1]
                        self.load_menu(filename)
                        return

                    elif action_code == "03":
                        # Return from Gosub
                        if self.menu_stack:
                            # Restore state from stack
                            self.return_from_gosub()
                            return
                        else:
                            print("No menu to return to.")
                    else:
                        print(f"Unhandled action code: {action_code}")

    def on_message_area_selected_12(self):
            self.execute_action_12()

    def on_message_area_selected_11(self):
        if self.sid_data.current_message_area is not None:
            # Proceed with reading messages
            self.execute_action_11()
        else:
            # Return to the menu if no message area is selected
            self.sid_data.menu.return_from_gosub()
            self.sid_data.setCurrentAction("wait_for_menu")
            
    def execute_action_12(self):
        self.sid_data.sauceWidth = self.sid_data.xWidth
        self.sid_data.sauceHeight = self.sid_data.yHeight
        self.sid_data.setMessageEditor(MessageEditor(self.util, self.message_editor_callback_on_exit))

    def execute_action_11(self):
        self.sid_data.sauceWidth = self.sid_data.xWidth
        self.sid_data.sauceHeight = self.sid_data.yHeight
        self.sid_data.setMessageReader(MessageReader(self.util, self.message_editor_callback_on_exit))
        self.sid_data.message_reader.display_menu()

    def append_gosub(self):
        current_state = {
            'values': copy.deepcopy(self.values),
            'sauce_width': self.sid_data.sauceWidth,
            'sauce_height': self.sid_data.sauceHeight,
            'color_array': copy.deepcopy(self.sid_data.color_array),
            'color_bgarray': copy.deepcopy(self.sid_data.color_bgarray),
            'input_values': copy.deepcopy(self.sid_data.input_values)
        }
        self.menu_stack.append(current_state)

    def return_from_gosub(self):
        last_state = self.menu_stack.pop()
        self.values = last_state['values']
        self.sid_data.setSauceWidth(last_state['sauce_width'])
        self.sid_data.setSauceHeight(last_state['sauce_height'])
        self.sid_data.color_array = last_state['color_array']
        self.sid_data.color_bgarray = last_state['color_bgarray']
        self.sid_data.input_values = last_state['input_values']
        self.util.clear_screen()
        self.display_editor()

    def load_menu(self, filename):
# Look for the filename in the database
        db = self.util.mongo_client["bbs"]  # You can replace "mydatabase" with the name of your database
        collection = db["menufiles"]

        file_data = collection.find_one({"filename": filename})
        
        if file_data:
            # Clear the existing values in MenuBox
            # self.sid_data.menu_box.values = [["" for _ in self.sid_data.menu_box.fields] for _ in range(self.sid_data.menu_box.num_rows)]
            
            # Retrieve the saved MenuBox data
            menu_box_data = file_data.get("menu_box_data", {})
            
            # Populate the fields
            #self.sid_data.menu_box.fields = menu_box_data.get("fields", [])
            
            ansi_code_base64 = file_data.get("ansi_code_base64")

            ansi_code_bytes = base64.b64decode(ansi_code_base64)
            
            sauce = self.util.get_sauce(ansi_code_bytes)

            ansi_code_bytes = self.util.strip_sauce(ansi_code_bytes)
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
            self.sid_data.input_values = []
            self.util.show_file_content(ansi_code, self.util.emit_current_string_local)

            # Populate the values at their respective y-coordinates
            for row in menu_box_data.get("values", []):
                y = row.get('y', 0)
                row_data = row.get('row_data', [])
                self.values[y] = row_data
                
            self.util.clear_screen()
            self.display_editor()

            
        else:
            self.util.goto_next_line()
            self.util.output("File "+filename+" not found!", 6, 0)
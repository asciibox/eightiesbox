from basicansi import BasicANSI
import base64

class Menu(BasicANSI):
    def __init__(self, util, values, num_rows, callback_on_exit):
        super().__init__(util)
        util.sid_data.setCurrentAction("wait_for_menu")
        self.values = values
        self.num_rows = num_rows
        self.callback_on_exit = callback_on_exit

    def handle_key(self, key):
        print("KEY")
        print(key)
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
                    if action_code == "00":
                        filename = self.values[row_idx][1]
                        self.load_menu(filename)
                        # Insert your code for action "00" here
                    elif action_code == "01":
                        filename = self.values[row_idx][1]
                        self.load_menu(filename)
                    else:
                        print(f"Unhandled action code: {action_code}")


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
from basicansi import BasicANSI

class Menu(BasicANSI):
    def __init__(self, util):
        super().__init__(util)
        
        self.values = None
        
    def handle_key(self, key):
        print("KEY")
        print(key)
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return
            
        if len(key) == 1:  # Check if it's a single character input
            print(key)


    def load_menu(self, filename):
# Look for the filename in the database
        file_data = collection.find_one({"filename": filename})
        
        if file_data:
            # Clear the existing values in MenuBox
            # self.sid_data.menu_box.values = [["" for _ in self.sid_data.menu_box.fields] for _ in range(self.sid_data.menu_box.num_rows)]
            
            # Retrieve the saved MenuBox data
            menu_box_data = file_data.get("menu_box_data", {})
            
            # Populate the fields
            self.sid_data.menu_box.fields = menu_box_data.get("fields", [])
            
            ansi_code_base64 = file_data.get("ansi_code_base64")

            ansi_code_bytes = base64.b64decode(ansi_code_base64)
            
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
                self.values[y] = row_data
                
            self.util.clear_scren()
            self.display_editor()

            
        else:
            self.goto_next_line()
            self.output("File not found!", 6, 0)
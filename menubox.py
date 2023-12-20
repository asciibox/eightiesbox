from menubar_menueditor import MenuBarMenuEditor
from menutexteditor import MenuTextEditor
import json
import base64

class MenuBox:
    def __init__(self, util):
        self.util = util
        self.sid_data = util.sid_data
        self.sid_data.setCurrentAction("wait_for_menubox")
        self.output = util.output
        # navigation on the menu on top of the list
        self.ask = util.ask
        self.current_main_index = 0
        self.current_sub_index = 0
        # navigation on the list
        self.in_sub_menu = False  # Flag to determine if in sub-menu
        self.current_row_index = 0  # To keep track of the current row
        self.current_field_index = 0  # To keep track of the field within a row
        self.fields = ['Type', 'Data', 'Key', 'Sec', 'Flags']
        self.fields_length = [3, 20, 4, 6, 36]

        self.mongo_client = util.mongo_client
        self.goto_next_line = util.goto_next_line
        self.clear_screen = util.clear_screen
        self.emit_gotoXY = util.emit_gotoXY
        self.clear_line = util.clear_line

        self.num_rows = 42

        # Initialize a 2D array to hold values for each field and each row.
        self.values = [["" for _ in self.fields] for _ in range(self.num_rows)]
        self.clear_screen()
        self.draw_all_rows()

        self.sid_data.input_values = []
        self.sid_data.color_array = []
        self.sid_data.color_bgarray = []

    
    def update_item(self, field, value):
        """Update a field's value and redraw the row."""
        
        # Check if we need to apply the special formatting logic
        type_field_value = self.get_value_for_field_and_row("Type", self.current_row_index)
        if field == "Data" and (type_field_value == "00" or type_field_value == "01"):
            value = self.util.format_filename(value, 'MNU')
        #prnt("FILENAME:"+value)

        key_to_insert = self.fields.index(field)

        # Convert to dictionary if it's not
        if not isinstance(self.values[self.current_row_index], dict):
            existing_list = self.values[self.current_row_index]
            new_dict = {i: val for i, val in enumerate(existing_list)}
            self.values[self.current_row_index] = new_dict

        # Update the value
        self.values[self.current_row_index][key_to_insert] = value

        # Draw the row
        self.draw_row(self.current_row_index)


        
    def get_field_widths(self):
        separator_total_width = 3 * (len(self.fields) - 1)  # " | " is 3 chars wide
        total_field_length = sum(self.fields_length)
        field_widths = [(length / total_field_length) * (self.sid_data.xWidth - separator_total_width) for length in self.fields_length]
        return field_widths

    # draws all menu box menu points, like key, content, security, flags
    def draw_all_rows(self):
        """Draw all rows at once. Useful for the initial rendering."""
              

        # Store startX for each field for use in edit_field
        self.field_startX = []
        startX = 0

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        # Create header using a loop
        for idx, (field, width) in enumerate(zip(self.fields, self.get_field_widths())):
            self.field_startX.append(startX)  # Store this coordinate for use in edit_field

            formatted_field = f"{field: <{int(width)}}"
            self.sid_data.setStartX(startX)  # Set the X-coordinate
            self.output(formatted_field, 7, 0)

            startX += int(width)  # Update X-coordinate
            
            if idx < len(self.fields) - 1:
                self.output(" | ", 7, 0)
                startX += 3  # " | " is 3 characters wide
                
        for row_idx in range(self.num_rows):
            self.draw_row(row_idx)

    def delete_current_row(self):
        self.values[self.current_row_index] = [''] * len(self.fields)
        self.draw_row(self.current_row_index)


    def get_value_for_field_and_row(self, field, row_idx):
        field_idx = self.fields.index(field)
        return self.values[row_idx][field_idx]


    def draw_row(self, row_idx):
        """Draw a single row given its index."""
        
        # Calculate total width consumed by separators
        field_widths = self.get_field_widths()

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(row_idx + 1)  # Assuming 1 line per row for example

        for field_idx, (field, width) in enumerate(zip(self.fields, field_widths)):
            value = self.get_value_for_field_and_row(field, row_idx)
            formatted_field = f"{value: <{int(width)}}"

            # Cut formatted_field to width characters
            formatted_field = formatted_field[:int(width)]

            if row_idx == self.current_row_index and field_idx == self.current_field_index:
                self.output(formatted_field, 0, 14)  # Assuming 0 is black and 14 is yellow
            else:
                self.output(formatted_field, 6, 0)  # Default colors

            # Add separator and padding between fields
            if field_idx < len(self.fields) - 1:
                self.output(" | ", 7, 0)

    
    def arrow_left(self):
        prev_field_idx = self.current_field_index
        self.current_field_index = (self.current_field_index - 1) % len(self.fields)
        self.draw_row(self.current_row_index)
        self.draw_row(self.current_row_index)  # Redraw same line as it has moved horizontally

    def arrow_right(self):
        prev_field_idx = self.current_field_index
        self.current_field_index = (self.current_field_index + 1) % len(self.fields)
        self.draw_row(self.current_row_index)  # Redraw same line as it has moved horizontally

    def arrow_up(self):
        if self.current_row_index >= 1:
            prev_row_idx = self.current_row_index
            self.current_row_index = (self.current_row_index - 1) % self.num_rows
            self.draw_row(prev_row_idx)  # Redraw the previous line
            self.draw_row(self.current_row_index)  # Redraw the new line
        else:
            sub_menus = {
            'File': ['Load menu', 'Save menu', 'New menu', 'Delete menu'],
            'Edit': ['Edit text', 'Simulate text', 'Clear text', 'View text', 'Leave menu bar'],
            }
            self.util.sid_data.setMenuBar(MenuBarMenuEditor(sub_menus, self.util))
            
    def arrow_down(self):
        prev_row_idx = self.current_row_index
        self.current_row_index = (self.current_row_index + 1) % self.num_rows
        self.draw_row(prev_row_idx)  # Redraw the previous line
        self.draw_row(self.current_row_index)  # Redraw the new line

    def create_update_callback(self, field_name):
        def callback(value):
            self.sid_data.setCurrentAction("wait_for_menubox")
            self.update_item(field_name, value)
        return callback

    def edit_field(self):
        field_idx = self.current_field_index
        row_idx = self.current_row_index
        start_field_idx = self.field_startX[field_idx]  # Retrieve startX from stored list
        start_row_idx = row_idx + 1

        self.sid_data.setStartX(start_field_idx)
        self.sid_data.setStartY(start_row_idx)

        input_length = self.fields_length[field_idx]
        field_name = self.fields[field_idx]
        callback = self.create_update_callback(field_name)

        field_widths = self.get_field_widths()
        
        if (field_idx == 0):            

            value = self.values[self.current_row_index][field_idx]
    
            # Assuming value is a string of two characters, each being a digit
            if len(value) == 2 and value.isnumeric():
                self.current_main_index = int(value[0])
                self.current_sub_index = int(value[1])-1                
                self.current_sub_menu = self.util.menu_structure[list(self.util.menu_structure.keys())[self.current_main_index]]
                self.in_sub_menu = True
                self.draw_main_menu()
                self.draw_sub_menu()
            else:
                self.draw_main_menu()

            self.sid_data.setCurrentAction("wait_for_layered_menu")
        elif field_idx == 1:
            width = min(int(field_widths[field_idx]), 100)  # max_input_length is a predefined maximum
            self.ask(width, callback)
            self.sid_data.setMaxScrollLength(100)
        else:
            width = min(int(field_widths[field_idx]), 100)
            self.ask(width, callback)

    # Menu on top
    def main_arrow_up(self):
        if self.current_main_index > 0:
            self.current_main_index -= 1
        self.draw_main_menu()

    def main_arrow_down(self):
        if self.current_main_index < len(self.util.menu_structure) - 1:
            self.current_main_index += 1
        self.draw_main_menu()

    def main_arrow_left(self):
        # Logic for left arrow in main menu if needed
        pass

    def main_arrow_right(self):
        # Logic for right arrow in main menu if needed
        pass

    def show_sub_menu(self):
        self.in_sub_menu = True
        selected_main_menu = list(self.util.menu_structure.keys())[self.current_main_index]
        self.current_sub_menu = self.util.menu_structure[selected_main_menu]
        self.current_sub_index = 0  # Resetting sub menu index
        self.draw_sub_menu()

    def sub_menu_arrow_up(self):
        if self.current_sub_index > 0:
            self.current_sub_index -= 1
        self.draw_sub_menu()

    def sub_menu_arrow_down(self):
        if self.current_sub_index < len(self.current_sub_menu) - 1:
            self.current_sub_index += 1
        self.draw_sub_menu()

    def select_sub_menu_item(self):
        field_idx = self.current_field_index
        first_field = ""
        first_field = str(self.current_main_index)
        value = first_field+str(self.current_sub_index+1)
        self.values[self.current_row_index][field_idx] = value
        
        self.draw_row(self.current_row_index)  # Only redraw the updated row
        # Handle the action associated with the selected item
        return
        
        
    def hide_sub_menu(self):
        self.in_sub_menu = False
        num_categories = len(self.util.menu_structure)  # Dynamic number of categories
        for row_idx in range(min(num_categories, len(self.values))):
            self.draw_row(row_idx)
        self.draw_main_menu()

    def hide_menu(self):
        # Assuming that hiding the menu means clearing out the area where it was displayed
        # You can implement this by setting spaces (' ') where the text was. 
        # (Or you can implement it your way)
        self.sid_data.setCurrentAction("wait_for_menubox")
        num_categories = len(self.util.menu_structure)  # Dynamic number of categories
        for row_idx in range(min(num_categories, len(self.values))):
            self.draw_row(row_idx)
        pass

    def draw_main_menu(self):
        # Set starting coordinates
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(1)

        # Iterate over main menu items and display them
        for idx, item in enumerate(self.util.menu_structure.keys()):
            color = 14 if idx == self.current_main_index else 0  # Highlight current row with color 14
            self.output(item.ljust(20), 7, color)  # Using 20 spaces for each menu item
            self.sid_data.setStartX(0) 
            self.sid_data.setStartY(self.sid_data.startY + 1)  # Move down one row for the next menu item

    def draw_sub_menu(self):
        # Set starting coordinates
        self.sid_data.setStartX(20)  # Assuming main menu takes 20 columns
        self.sid_data.setStartY(1)   # Align with main menu

        # Iterate over sub-menu items and display them
        for idx, item in enumerate(self.current_sub_menu):
            color = 14 if idx == self.current_sub_index else 0  # Highlight current row with color 14
            self.output(item.ljust(20), 7, color)  # Using 20 spaces for each menu item
            self.sid_data.setStartX(20)
            self.sid_data.setStartY(self.sid_data.startY + 1)  # Move down one row for the next menu item

    def get_selected_main_menu(self):
        # Convert dictionary keys to a list and then return the item at the current index
        return list(self.util.menu_structure.keys())[self.current_main_index]

    def new_menu(self):
        for row in self.values:
            for i, field in enumerate(self.fields):
                row[i] = ''  # Reset value

        self.sid_data.input_values = []
        self.sid_data.color_array = []
        self.sid_data.color_bgarray = []
        self.draw_row(self.current_row_index)  # Redraw the updated row
        self.draw_all_rows()

    
    def draw_all_rows_and_output_json(self):
        """Draw all rows and output relevant JSON."""
      
        # List to store the table data
        table_data = []

        # Iterate over the rows
        for row_idx in range(len(self.values)):
            
            # Dictionary to store the row data
            row_data = {}

            # Calculate total width consumed by separators
            separator_total_width = 3 * (len(self.fields) - 1)  # " | " is 3 chars wide

            # Calculate the sum of the field lengths
            total_field_length = sum(self.fields_length)

            # Calculate individual field widths as a percentage of total width
            field_widths = [(length / total_field_length) * (self.sid_data.xWidth - separator_total_width) for length in self.fields_length]

            for field_idx, (field, width) in enumerate(zip(self.fields, field_widths)):
                value = self.get_value_for_field_and_row(field, row_idx)
                formatted_field = f"{value: <{int(width)}}".strip()  # Stripping whitespace for better JSON format

                # Storing the formatted value in the row_data dictionary
                row_data[field] = formatted_field

            # Append the row data to the table data only if not all fields are empty
            if not all(val == "" for val in row_data.values()):
                table_data.append(row_data)

        self.sid_data.setMenuTextEditor(MenuTextEditor(self.util))
        ansi_code = self.sid_data.menutexteditor.display_ansi()
        ansi_code_bytes = ansi_code.encode('utf-8')
        ansi_code_base64 = base64.b64encode(ansi_code_bytes).decode('ascii')

        # Overall JSON structure including the table data and ansi_data
        result_data = {
            "table": table_data,
            "ansi_data": ansi_code_base64  # Replace with the actual ANSI string or data if needed
        }
   

        print (json.dumps(result_data, indent=4))

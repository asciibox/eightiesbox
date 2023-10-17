from menubar_menueditor import *

class MenuBox:
    def __init__(self, util):
        self.util = util
        self.sid_data = util.sid_data
        self.sid_data.setCurrentAction("wait_for_menu")
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

        self.num_rows = 50

        # Initialize a 2D array to hold values for each field and each row.
        self.values = [["" for _ in self.fields] for _ in range(self.num_rows)]
        self.clear_screen()
        self.draw_all_rows()

        self.menu_structure = {
            'Goto & Gosub': ['Goto new menu', 'Gosub new menu', 'Return from gosub'],
            'Message base': ['Read message', 'Write message', 'Area change'],
            'File base': ['Download files', 'Upload files', 'List files', 'Select file area'],
            'User options': ['Change password', 'Change email', 'Change interests/hobbies'],
            'Login/Logout': ['Logout', 'Show oneliners'],
            'Multiline options': ['Users online', 'Chat between nodes', 'Add conference', 'Join conference', 'Delete conference'],
            'Display text': ['Display ANS / ASC', 'Display ANS / ASC and wait'],
            'BBS List': ['Long list display', 'Short list display', 'Add BBS']
        }

    def get_value_for_field_and_row(self, field, row_idx):
        field_idx = self.fields.index(field)
        return self.values[row_idx][field_idx]

    def draw_all_rows(self):
        """Draw all rows at once. Useful for the initial rendering."""
        
        separator_total_width = 3 * (len(self.fields) - 1)  # " | " is 3 chars wide
        total_field_length = sum(self.fields_length)
        field_widths = [(length / total_field_length) * (self.sid_data.xWidth - separator_total_width) for length in self.fields_length]

        # Store startX for each field for use in edit_field
        self.field_startX = []
        startX = 0

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        # Create header using a loop
        for idx, (field, width) in enumerate(zip(self.fields, field_widths)):
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

    def update_item(self, field, value):
        """Update a field's value and redraw the row."""
        self.values[self.current_row_index][self.fields.index(field)] = value
        
        self.draw_row(self.current_row_index)  # Only redraw the updated row

    def draw_row(self, row_idx):
        """Draw a single row given its index."""
        
        # Calculate total width consumed by separators
        separator_total_width = 3 * (len(self.fields) - 1)  # " | " is 3 chars wide

        # Calculate the sum of the field lengths
        total_field_length = sum(self.fields_length)

        # Calculate individual field widths as a percentage of total width
        field_widths = [(length / total_field_length) * (self.sid_data.xWidth - separator_total_width) for length in self.fields_length]

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(row_idx + 1)  # Assuming 1 line per row for example

        for field_idx, (field, width) in enumerate(zip(self.fields, field_widths)):
            value = self.get_value_for_field_and_row(field, row_idx)
            formatted_field = f"{value: <{int(width)}}"

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
            self.sid_data.setCurrentAction("wait_for_menu")
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
        
        if (field_idx == 0):
            self.draw_main_menu()
            self.sid_data.setCurrentAction("wait_for_layered_menu")
        else:
            self.ask(input_length, callback)

    # Menu on top
    def main_arrow_up(self):
        if self.current_main_index > 0:
            self.current_main_index -= 1
        self.draw_main_menu()

    def main_arrow_down(self):
        if self.current_main_index < len(self.menu_structure) - 1:
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
        selected_main_menu = list(self.menu_structure.keys())[self.current_main_index]
        self.current_sub_menu = self.menu_structure[selected_main_menu]
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
        if self.current_main_index!=0:
            first_field = str(self.current_main_index)
        value = first_field+str(self.current_sub_index+1)
        self.values[self.current_row_index][field_idx] = value
        
        self.draw_row(self.current_row_index)  # Only redraw the updated row
        # Handle the action associated with the selected item
        return
        
    def hide_sub_menu(self):
        self.in_sub_menu = False
        for row_idx in range(min(8, len(self.values))):
            self.draw_row(row_idx)
        self.draw_main_menu()

    def hide_menu(self):
        # Assuming that hiding the menu means clearing out the area where it was displayed
        # You can implement this by setting spaces (' ') where the text was. 
        # (Or you can implement it your way)
        self.sid_data.setCurrentAction("wait_for_menu")
        for row_idx in range(min(8, len(self.values))):
            self.draw_row(row_idx)
        pass

    def draw_main_menu(self):
        # Set starting coordinates
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(1)

        # Iterate over main menu items and display them
        for idx, item in enumerate(self.menu_structure.keys()):
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
        return list(self.menu_structure.keys())[self.current_main_index]

    def new_menu(self):
        for row in self.values:
            for i, field in enumerate(self.fields):
                row[i] = ''  # Reset value

        self.draw_row(self.current_row_index)  # Redraw the updated row
        self.draw_all_rows()

            
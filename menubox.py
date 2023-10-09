class MenuBox:
    def __init__(self, sid_data, output_function, ask_function):
        self.sid_data = sid_data
        self.output = output_function
        self.ask = ask_function
        self.current_row_index = 0  # To keep track of the current row
        self.current_field_index = 0  # To keep track of the field within a row
        self.fields = ['Text', 'Optional data', 'Menu type', 'Security', 'Key', 'Foreground', 'Background']
        
        self.num_rows = 50

        # Initialize a 2D array to hold values for each field and each row.
        self.values = [["" for _ in self.fields] for _ in range(self.num_rows)]
        self.draw_all_rows()


    def get_value_for_field_and_row(self, field, row_idx):
        field_idx = self.fields.index(field)
        return self.values[row_idx][field_idx]

    def draw_all_rows(self):
        """Draw all rows at once. Useful for the initial rendering."""
        
        # Calculate total width consumed by separators
        separator_total_width = 3 * (len(self.fields) - 1)  # " | " is 3 chars wide
        
        # Calculate remaining width available for fields
        available_width = self.sid_data.xWidth - separator_total_width
        
        # Calculate individual field width
        field_width = int(available_width / len(self.fields))
        
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        
        # Create header using a loop
        header = ""
        for idx, field in enumerate(self.fields):
            my_field = field
            while len(my_field)<field_width+1:
                my_field = my_field + " "
            header = header + my_field
            if idx < len(self.fields) - 1:  # Add separator except after last field
                header += " | "
        
        self.output(header, 7, 0)
        
        # Draw the rows
        for row_idx in range(self.num_rows):
            self.draw_row(row_idx)

    def update_item(self, field, value):
        """Update a field's value and redraw the row."""
        self.values[self.current_row_index][self.fields.index(field)] = value
        
        self.draw_row(self.current_row_index)  # Only redraw the updated row

    def draw_row(self, row_idx):
        """Draw a single row given its index."""
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(row_idx+1)  # Assuming 1 line per row for example
        field_width = int(self.sid_data.xWidth / len(self.fields))

        for field_idx, field in enumerate(self.fields):
            value = self.get_value_for_field_and_row(field, row_idx)
            formatted_field = f"{value: <{field_width - 2}}"
            
            if row_idx == self.current_row_index and field_idx == self.current_field_index:
                self.output(formatted_field, 0, 14)  # Assuming 0 is black and 14 is yellow
            else:
                self.output(formatted_field, 6, 0)  # Default colors
            
            # Add separator and padding between fields
            if field_idx < len(self.fields) - 1:
                self.output(" | ", 7, 0)
                # self.sid_data.setStartX(self.sid_data.startX + 1)

            #self.sid_data.setStartX(self.sid_data.startX + len(formatted_field) + 1)

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
        prev_row_idx = self.current_row_index
        self.current_row_index = (self.current_row_index - 1) % self.num_rows
        self.draw_row(prev_row_idx)  # Redraw the previous line
        self.draw_row(self.current_row_index)  # Redraw the new line

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
        start_field_idx = sum(18 for _ in range(field_idx))
        start_row_idx = row_idx + 1

        self.sid_data.setStartX(start_field_idx)
        self.sid_data.setStartY(start_row_idx)
        
        self.output(" " * 16, 0, 0)
        self.sid_data.setStartX(self.sid_data.startX + 16)
        
        field_name = self.fields[field_idx]
        callback = self.create_update_callback(field_name)
        self.ask(16, callback)

from ansieditor import ANSIEditor

class Timeline(ANSIEditor):
    def __init__(self, util, callback_on_exit):
        super().__init__(util)
        # Initialize common rendering properties
        self.util = util

        self.output = self.util.output
        self.callback_on_exit = callback_on_exit
        self.current_page = 0
        self.sid_data = util.sid_data
        self.max_height = self.sid_data.yHeight

        self.input_values_page = [[]]
        self.color_array_page = [[]]
        self.color_bgarray_page = [[]]
        self.current_line_index_page = []


    def show_timeline(self):
        db = self.util.mongo_client['bbs']
        timeline_entries_collection = db['timeline_entries']

        # Fetch timeline entries, assuming they are sorted by time
        entries = timeline_entries_collection.find().sort("time")

        # Calculate screen dimensions and layout
        max_width = 128
        max_height = 60
        separator_pos = max_width // 2  # Position of the vertical separator

        # Current positions for rendering
        current_x_left = 0
        current_x_right = separator_pos + 1
        current_y = 0

        # Keep track of the previous date for headline display
        previous_date = None

        for entry in entries:
            # Check if the date has changed
            if previous_date != entry['time'].strftime("%Y-%m-%d"):
                previous_date = entry['time'].strftime("%Y-%m-%d")
                self.util.setStartX(0)
                self.util.setStartY(current_y)
                self.util.output(previous_date.center(max_width), fg_color, bg_color)
                current_y += 1  # Move to the next line after the headline

            # Determine which side to render the message
            if current_x_left < separator_pos:
                self.util.setStartX(current_x_left)
                self.util.setStartY(current_y)
                self.util.output(entry['message'], fg_color, bg_color)
                current_x_left += len(entry['message']) + 1
            else:
                self.util.setStartX(current_x_right)
                self.util.setStartY(current_y)
                self.util.output(entry['message'], fg_color, bg_color)
                current_x_right += len(entry['message']) + 1

            # Move to next line if right side is filled or display separator
            if current_x_right >= max_width:
                current_y += 1
                current_x_left = 0
                current_x_right = separator_pos + 1

                # Draw separator if not at a headline
                self.util.setStartX(separator_pos)
                self.util.setStartY(current_y)
                self.util.output('|', fg_color, bg_color)

            # Check if we reached the bottom of the screen
            if current_y >= max_height:
                break  # Implement pagination or scrolling if needed

    def display_editor(self, write_header=True):
        # Displaying "From:"

        if write_header:
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(0)
            from_user = self.sid_data.user_name
            self.output("From: ", 6, 0)
            self.output(from_user, 11, 0)

            # Moving to next line and displaying "To:"
            self.goto_next_line()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(1)  # Assuming Y index is 0-based
            to_user = self.sid_data.message_data.get("To", "data")
            self.output("To: ", 6, 0)
            self.output(to_user, 14, 4)

            # Moving to next line and displaying "Subject:"
            self.goto_next_line()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(2)  # Assuming Y index is 0-based
            subject = self.sid_data.message_data.get("Subject", "data")
            self.output("Subject: ", 6, 0)
            self.output(subject, 14, 4)

            self.current_line_index = 3  # For navigating vertically among characters
            self.current_line_x = 0

            for idx in range(3, self.max_height):
                self.draw_line(idx)
            self.emit_gotoXY(0, 4)
        else:
            for idx in range(0, self.max_height):
                self.draw_line(idx)
            self.emit_gotoXY(0, 0)

    def setup_interface(self):
        # Setting cursor position for "From:"
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        # Output "From:" in different colors, let's say fg=2 and bg=0
        
        self.output("Press ESC to stop typing in a timeline entry", 6, 0)

        self.util.sid_data.setCurrentAction("wait_for_timelineeditor")
        self.util.emit_gotoXY(0, 1)
        self.current_line_index = 1
        self.sid_data.sauceWidth = 60
        

    def enter_pressed(self):
        self.enter_pressed2()
        self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
        self.current_line_index_page[self.current_page] = self.current_line_index
        
        if self.current_line_index >= self.max_height - 1:
            self.save_current_page_data()
            self.current_page += 1
            self.current_line_index = 0
            self.update_page_data()

   

    def arrow_up_pressed(self):
        super().arrow_up_pressed()
        
        self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
        self.current_line_index_page[self.current_page] = self.current_line_index
        print(self.current_line_index)
        print("CURRENT LINE INDEX:"+str(self.current_line_index))
        if self.current_line_index < 0 and self.current_page > 0:
            self.save_current_page_data()
            self.current_page -= 1
            self.update_page_data()
            self.current_line_index = self.current_line_index_page[self.current_page]
            print("self.current_line_index restored: "+str(self.current_line_index))
            self.util.emit_gotoXY(0, self.util.sid_data.yHeight - 2)

    def ensure_page_index_exists(self, index, default_value=0):
        while len(self.current_line_index_page) <= index:
            self.current_line_index_page.append(default_value)

    def arrow_down_pressed(self):
        if self.current_line_index < self.max_height -2:
            self.current_line_index += 1
            self.set_cursor_y(self.current_line_index)
            
            self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
            self.current_line_index_page[self.current_page] = self.current_line_index
        
    def update_page_data(self):
         # Ensure the current page exists in the arrays
        while len(self.input_values_page) <= self.current_page:
            self.input_values_page.append([])  # Append an empty list for the new page
        while len(self.color_array_page) <= self.current_page:
            self.color_array_page.append([])
        while len(self.color_bgarray_page) <= self.current_page:
            self.color_bgarray_page.append([])

        self.sid_data.input_values = self.input_values_page[self.current_page]
        self.sid_data.color_array = self.color_array_page[self.current_page]
        self.sid_data.color_bgarray = self.color_bgarray_page[self.current_page]
        self.util.clear_screen()
        self.input_values = self.sid_data.input_values
        self.color_array = self.sid_data.color_array
        self.color_bgarray = self.sid_data.color_bgarray
        self.sid_data.message_editor.display_editor(self.current_page == 0)

    def save_current_page_data(self):
        self.input_values_page[self.current_page] = self.sid_data.input_values
        self.color_array_page[self.current_page] = self.sid_data.color_array
        self.color_bgarray_page[self.current_page] = self.sid_data.color_bgarray

    def draw_line(self, line_index):
        # self.sid_data.setMapCharacterSet(True)
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(line_index+self.yOffsetOnDraw)
        if line_index < len(self.input_values):
            self.output_with_color(0, line_index, self.input_values[line_index], None, 0)

    def process_key_input(self, current_line_index, current_line_x, key, foregroundColor, backgroundColor):
        print("PROCESS OK")
        if self.sid_data.insert:
            self.draw_line(current_line_index)
            self.emit_gotoXY(current_line_x, current_line_index )
        else:
            self.sid_data.setStartX(current_line_x)
            self.sid_data.setStartY(current_line_index)
            self.output(key, foregroundColor, backgroundColor)

    def set_cursor_x(self, current_line_x):
        self.emit_gotoXY(current_line_x, self.current_line_index)

    def set_cursor_y(self, current_line_y):
        self.emit_gotoXY(self.current_line_x, current_line_y)

    def enter_pressed2(self):
        if self.current_line_index < self.max_height - 2:
            self.current_line_x = 0  # Reset x coordinate to 0
            self.current_line_index += 1  # Increment line index

            self.set_cursor_y(self.current_line_index)  # Go to next line

    
    def clear_current_line(self, cur_y):
        print("CLEAR LINE "+str(cur_y-1))
        self.clear_line(cur_y)
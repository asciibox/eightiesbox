from ansieditor import ANSIEditor
from datetime import datetime
import pymongo
import time

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

        self.sleeper = 0.25

    def show_timeline(self, page=1):
        db = self.util.mongo_client['bbs']
        timeline_entries_collection = db['timeline_entries']

        # Fetch timeline entries, sorted by timestamp
        entries = list(timeline_entries_collection.find().sort("timestamp", -1))

        # Screen dimensions and layout
        max_width = self.util.sid_data.xWidth
        max_height = self.util.sid_data.yHeight-1
        lines_per_page = max_height
        separator_pos = max_width // 2 if max_width >= 50 else None

        # Initialize counters and flags
        current_page = 1
        line_count = 0
        page_entries = []

        # Split entries into pages
        for entry in entries:
            entry_lines = 2 + entry['text'].count('\n')  # Add 2 for timestamp and blank line
            if line_count + entry_lines > lines_per_page:
                current_page += 1
                line_count = 0

            if current_page == page:
                page_entries.append(entry)

            line_count += entry_lines
            if current_page > page:
                break

        if max_width < 50:
            self.render_narrow_screen(page_entries, lines_per_page)
        else:
            self.render_wide_screen(page_entries, lines_per_page, separator_pos)

        

        self.util.sid_data.setCurrentAction("wait_for_timeline_entry")
        self.util.sid_data.startX = 0
        self.util.sid_data.startY += 1
        self.output("Press C to create a new timeline entry", 11, 0)

    def render_narrow_screen(self, page_entries, lines_per_page):
        lines_on_page = 0

        for entry in page_entries:
            if lines_on_page >= lines_per_page:
                break

            timestamp_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            entry_lines = entry['text'].split('\n')

            self.util.sid_data.startX = 0

            # Display timestamp
            self.util.sid_data.startY = lines_on_page
            self.util.output(timestamp_str, 4, 0)
            lines_on_page += 1

            # Display each line of the entry
            for line in entry_lines:
                if lines_on_page >= lines_per_page:
                    break
                self.util.sid_data.startY = lines_on_page
                self.util.output(line, 6, 0)
                lines_on_page += 1

            lines_on_page += 1  # Add a blank line after each entry

    def render_wide_screen(self, page_entries, lines_per_page, separator_pos):
        lines_on_left = 0
        lines_on_right = 0
        left_side = True

        # Draw the separator for the entire column first
        for line in range(lines_per_page):
            self.util.sid_data.startX = separator_pos
            self.util.sid_data.startY = line
            self.util.output('|', 1, 0)

        # Now render the entries on either side
        for entry in page_entries:
            if max(lines_on_left, lines_on_right) >= lines_per_page:
                break

            timestamp_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            entry_lines = entry['text'].split('\n')

            # Decide which side to put the timestamp and entry on
            if lines_on_left <= lines_on_right:
                # Place timestamp and entry on the left side
                self.render_entry_on_side(timestamp_str, entry_lines, lines_on_left, 0)
                lines_on_left += len(entry_lines) + 2  # Including space for timestamp and a blank line
                left_side = False
            else:
                # Place timestamp and entry on the right side
                self.render_entry_on_side(timestamp_str, entry_lines, lines_on_right, separator_pos + 1)
                lines_on_right += len(entry_lines) + 2
                left_side = True

    def render_entry_on_side(self, timestamp_str, entry_lines, start_line, start_x):
        # Output the timestamp
        self.util.sid_data.startX = start_x
        self.util.sid_data.startY = start_line
        self.util.output(timestamp_str, 1, 0)

        # Output each line of the entry text below the timestamp
        for line in entry_lines:
            start_line += 1
            self.util.sid_data.startX = start_x
            self.util.sid_data.startY = start_line
            self.util.output(line, 6, 0)

                


    def handle_timeline_view_key(self, key, key_status_array):
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return


        if key == 'Escape':
            self.util.sid_data.menu.return_from_gosub()
            self.util.sid_data.setCurrentAction("wait_for_menu")
            return
        # keyStatusArray = [shiftPressed, ctrlKeyPressed, altgrPressed]
        if key == 'c':
            
            self.add_timeline_entry() 
            return


    def display_editor(self, write_header=True):
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = 0
        self.output("Press ESC to stop typing in a timeline entry", 6, 0)
        for idx in range(0, self.max_height):
            self.draw_line(idx)
        self.emit_gotoXY(0, 1)
        
    def add_timeline_entry(self):
        # Setting cursor position for "From:"
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        # Output "From:" in different colors, let's say fg=2 and bg=0
        
        self.output("Press ESC to stop typing in a timeline entry", 6, 0)

        self.sid_data.input_values = []
        
        # Clear the color array
        self.sid_data.color_array = []

        # Clear the background color array
        self.sid_data.color_bgarray = []

        self.sid_data.timeline.set_text_values([], [], [],[])

        self.util.sid_data.setCurrentAction("wait_for_timelineeditor")
        self.util.emit_gotoXY(0, 1)
        self.current_line_index = 1
        self.sid_data.sauceWidth = 55
        

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
        if self.current_line_index < 0 and self.current_page > 0:
            self.save_current_page_data()
            self.current_page -= 1
            self.update_page_data()
            self.current_line_index = self.current_line_index_page[self.current_page]
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
        self.clear_line(cur_y)
        
    def save_timeline_entry(self):
         # Convert 2D array into a string
        text = self.convert_2d_array_to_text(self.sid_data.input_values)

        # Get current date and time
        current_datetime = datetime.now()

        # Create a document
        document = {
            "text": text,
            "timestamp": current_datetime,
            "user_id" : self.sid_data.user_document['_id']
        }

        # Insert into MongoDB
        db = self.mongo_client['bbs']
        timeline_entries_collection = db['timeline_entries']
        timeline_entries_collection.insert_one(document)

        self.show_timeline()

    def convert_2d_array_to_text(self, input_values):
        # Convert each row in the 2D array to a string and join them with newlines
        return '\n'.join([''.join(row) for row in input_values])
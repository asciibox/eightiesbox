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
        self.current_page = 1
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
        max_height = self.util.sid_data.yHeight - 5
        lines_per_page = max_height

        # Pre-render entries and calculate page breaks
        rendered_entries, page_breaks = self.pre_render_and_calculate_pages(entries, lines_per_page)

        if page <= len(page_breaks):
            start_index, end_index = page_breaks[page - 1]
            page_entries = rendered_entries[start_index:end_index]
            self.display_content(page_entries, max_width)  # Display the content for the requested page
        else:
            print("Page out of range error")

        self.util.sid_data.setCurrentAction("wait_for_timeline_entry")
        self.util.sid_data.startX = 0
        self.util.sid_data.startY += 1
        self.output("Press C to create a new timeline entry and the arrow keys to navigate through the timeline", 11, 0)

    def display_content(self, page_entries, max_width):
        # Determine the layout based on max_width
        is_wide_screen = max_width >= 50
        separator_pos = max_width // 2 if is_wide_screen else None

        # Initialize counters for line positions
        left_line_pos = 0
        right_line_pos = 0

        for entry in page_entries:
            # 'entry' here is assumed to be a pre-rendered string
            entry_lines = entry.split('\n')

            # Check if the entry should be on the left or right (for wide screen)
            if is_wide_screen:
                if left_line_pos <= right_line_pos:
                    # Render timestamp and text on the left side
                    self.render_entry_on_screen(entry_lines, left_line_pos, 0)
                    left_line_pos += len(entry_lines)
                else:
                    # Render timestamp and text on the right side
                    self.render_entry_on_screen(entry_lines, right_line_pos, separator_pos + 1)
                    right_line_pos += len(entry_lines)
            else:
                # For narrow screens, just render the entry
                self.render_entry_on_screen(entry_lines, left_line_pos, 0)
                left_line_pos += len(entry_lines)

        # Handle screen refresh or update here if necessary

    def render_entry_on_screen(self, entry_lines, start_line, start_col):
        # Render the entry (timestamp and text)
        for i, line in enumerate(entry_lines):
            self.util.sid_data.startX = start_col
            self.util.sid_data.startY = start_line + i
            self.output(line, 7, 0)  # Example color codes, adjust as needed

    def render_entry(self, entry):
        # Prepare the rendered content as a string
        rendered_content = ""

        # Render the timestamp
        timestamp_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        rendered_content += timestamp_str + "\n"

        # Render the entry text
        entry_lines = entry['text'].split('\n')
        for line in entry_lines:
            rendered_content += line + "\n"

        return rendered_content

    def count_lines(self, rendered_entry):
        # Count the number of newline characters in the rendered entry
        # Add one additional line for the break after the entry
        return rendered_entry.count('\n') + 1

    def pre_render_and_calculate_pages(self, entries, lines_per_page):
        rendered_entries = []
        page_breaks = []
        current_page_start = 0
        left_line_count = 0
        right_line_count = 0

        # Pre-render entries
        for entry in entries:
            rendered_entry = self.render_entry(entry)  # Render the entry into a display-ready format
            rendered_entries.append(rendered_entry)
            entry_lines = self.count_lines(rendered_entry)  # Count the lines in the rendered entry

            # Decide whether to place the entry on the left or right column
            if left_line_count <= right_line_count:
                # If the entry does not fit in the left column, move to the next page
                if left_line_count + entry_lines > lines_per_page:
                    page_breaks.append((current_page_start, len(rendered_entries) - 1))
                    current_page_start = len(rendered_entries) - 1
                    left_line_count = 0
                    right_line_count = 0
                left_line_count += entry_lines
            else:
                # If the entry does not fit in the right column, move to the next page
                if right_line_count + entry_lines > lines_per_page:
                    page_breaks.append((current_page_start, len(rendered_entries) - 1))
                    current_page_start = len(rendered_entries) - 1
                    left_line_count = 0
                    right_line_count = 0
                right_line_count += entry_lines

        # Add the last page
        page_breaks.append((current_page_start, len(rendered_entries)))

        return rendered_entries, page_breaks


    def show_page(self, page_number, rendered_entries, page_breaks):
        if page_number <= len(page_breaks):
            start_index, end_index = page_breaks[page_number - 1]
            page_content = rendered_entries[start_index:end_index+1]
            self.display_content(page_content)  # Implement this method to display the content on the screen
        else:
            pass

    def handle_timeline_view_key(self, key, key_status_array):
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return


        if key == 'Escape':
            self.util.sid_data.menu.return_from_gosub()
            self.util.sid_data.setCurrentAction("wait_for_menu")
            return
        # keyStatusArray = [shiftPressed, ctrlKeyPressed, altgrPressed]
        elif key == 'ArrowDown' or key == 'ArrowRight':
            self.current_page += 1
            self.util.clear_screen()
            self.show_timeline(self.current_page)
            return
        elif key == 'ArrowUp' or key == 'ArrowLeft':
            if self.current_page > 0:
                self.current_page -= 1
                self.util.clear_screen()
                self.show_timeline(self.current_page)
            return
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
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

        self.sleeper = 1

        self.page_breaks = []

    def show_timeline(self, page=1):
        db = self.util.mongo_client['bbs']
        timeline_entries_collection = db['timeline_entries']

        # Get the current user's ID from the session data
        current_user_id = self.util.sid_data.user_document['_id']

        # Fetch timeline entries for the current user, sorted by timestamp
        entries = list(timeline_entries_collection.find({"user_id": current_user_id}).sort("timestamp", -1))

        # Screen dimensions and layout
        
        max_width = self.util.sid_data.xWidth
        print("MAX WIDTH :"+str(max_width))
        if max_width>=50:
            max_height = self.util.sid_data.yHeight
            lines_per_page = max_height
            processed_entries = entries
        else:
            max_height = self.util.sid_data.yHeight - 9
            lines_per_page = max_height
            processed_entries = self.process_and_split_entries(entries, max_width, lines_per_page)
        

        # Pre-render entries and calculate page breaks
        
        rendered_entries = self.pre_render_and_calculate_pages(processed_entries, lines_per_page, max_width)

        print("Page Breaks:", self.page_breaks)
        if page <= len(self.page_breaks):
            start_index, end_index = self.page_breaks[page - 1]
            page_entries = rendered_entries[start_index:end_index + 1]
            self.display_content(page_entries, max_width)  # Display the content for the requested page
            time.sleep(self.sleeper)
        else:
            print("Page out of range error")

        self.util.sid_data.setCurrentAction("wait_for_timeline_entry")
        self.util.sid_data.startX = 0
        
        if max_width>=50:
            self.util.sid_data.startY = self.util.sid_data.yHeight -3
            self.util.output("Press C to create a new timeline entry and the arrow keys to navigate", 11, 0)
            self.util.goto_next_line()
            self.util.output("Press I to upload an image to the timeline", 11, 0)
        else:
            self.util.sid_data.startY = self.util.sid_data.yHeight - 3
            self.util.output("[C] - create entry [I] - upload img", 11, 0)
            self.util.goto_next_line()
            self.util.output("use cursorkeys for pagenav", 6, 0)

    def display_content(self, page_entries, max_width):
        # Constants for layout
        is_wide_screen = max_width >= 50
        separator_pos = max_width // 2 if is_wide_screen else 0
        image_height = 7  # Fixed image height

        # Initialize counters for line positions, starting at 1 to accommodate the first timestamp
        left_line_pos = 1
        right_line_pos = 1

        for rendered_entry, original_entry in page_entries:
            # Split the entry into lines
            entry_lines = rendered_entry.split('\n')
            
            # Extract the timestamp line and adjust the remaining entry lines
            timestamp_line = entry_lines[0]
            entry_text = [line for line in entry_lines[1:] if line.strip() != '']  # Remove empty lines

            # Decide whether to place the entry in the left or right column
            in_right_column = is_wide_screen and (right_line_pos <= left_line_pos)
            text_left = separator_pos if in_right_column else 0

            # Calculate the correct line position for the timestamp
            current_line_pos = right_line_pos if in_right_column else left_line_pos

            # Render the timestamp line first
            self.render_entry_on_screen([timestamp_line], current_line_pos - 1, text_left)
           
            # If there's an image, render it below the timestamp and add image_height to the line counter
            if 'image_url' in original_entry:
                img_top = current_line_pos
                img_left = separator_pos if in_right_column else 0
                self.util.emit_background_image("https://storage.googleapis.com/eightiesbox_uploaded/" + original_entry['image_url'], img_left, img_top, 0, 7, True)
                current_line_pos += image_height

            # Render the rest of the text below the image or timestamp
            if entry_text:
                self.render_entry_on_screen(entry_text, current_line_pos, text_left)
                current_line_pos += len(entry_text)

            # Add a one-line gap after every entry (image or text)
            current_line_pos += 2

            # Update the line positions for the next entry
            if in_right_column:
                right_line_pos = current_line_pos
            else:
                left_line_pos = current_line_pos

    def render_entry_on_screen(self, entry_lines, start_line, start_col):
        # Render the entry (timestamp and text)
        for i, line in enumerate(entry_lines):
            self.util.sid_data.startX = start_col
            self.util.sid_data.startY = start_line + i
            self.output(line, 7, 0)  # Example color codes, adjust as needed

    def render_entry(self, entry):
        # Always start with rendering the timestamp
        timestamp_str = entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
        rendered_content = timestamp_str + "\n"

        # Check if the entry contains an image
        if 'image_url' in entry:
            # Return the timestamp followed by 7 line breaks for entries with an image
            return rendered_content + '\n' * 3

        # Render the entry text for entries without an image
        entry_lines = entry['text'].split('\n')
        for line in entry_lines:
            rendered_content += line + "\n"

        return rendered_content

    def count_lines(self, rendered_entry):
        # Count the number of newline characters in the rendered entry
        # Add one additional line for the break after the entry
        return rendered_entry.count('\n') + 1

    def process_and_split_entries(self, entries, max_width, max_height):
        modified_entries = []
        current_y_pos = 0  # Current Y position on the page

        def split_entry_text(text, available_lines, max_width):
            lines = text.split('\n')
            processed_lines = []
            remaining_text = ''

            for line in lines:
                current_line = ''
                words = line.split()

                for word in words:
                    # Check if adding the next word exceeds the max width
                    if len(current_line) + len(word) + 1 > max_width:
                        if len(processed_lines) < available_lines:
                            processed_lines.append(current_line)
                            current_line = word
                        else:
                            # Add the rest to remaining_text
                            remaining_text += ' ' + word
                    else:
                        current_line += (' ' if current_line else '') + word

                # Add the last processed line if there's space
                if len(processed_lines) < available_lines:
                    processed_lines.append(current_line)
                else:
                    remaining_text += '\n' + current_line

                # Check if max lines for the page are reached
                if len(processed_lines) >= available_lines:
                    remaining_text += '\n'.join(lines[lines.index(line) + 1:])
                    break

            return '\n'.join(processed_lines).strip(), remaining_text.strip()

        for entry in entries:
            if 'image_url' in entry and entry['image_url']:
                text = ' \n' * 7
            else:
                text = entry['text']
            while text:
                # Calculate available lines based on the current Y position
                available_lines = max_height - current_y_pos

                partial_text, text = split_entry_text(text, available_lines, max_width)
                if text:
                    # Prepare text for the next entry if there's more to display
                    text = "(continued) " + text

                new_entry = entry.copy()
                new_entry['text'] = partial_text
                modified_entries.append(new_entry)

                # Update current Y position
                current_y_pos += len(partial_text.split('\n'))
                if current_y_pos >= max_height:
                    # Reset Y position for the new page
                    current_y_pos = 0

        return modified_entries




    def pre_render_and_calculate_pages(self, entries, lines_per_page, max_width):
        is_wide_screen = max_width >= 50
        rendered_entries = []
        self.page_breaks = []
        current_page_start = 0
        left_line_count = 0
        right_line_count = 0
        image_height = 7  # Height for images

        # Pre-render entries
        for index, entry in enumerate(entries):
            rendered_entry = self.render_entry(entry)
            rendered_entries.append((rendered_entry, entry))
            
            # Determine the number of lines this entry will take
            entry_lines = self.count_lines(rendered_entry)
            if 'image_url' in entry:
                entry_lines += image_height  # Add image height if the entry has an image and it's a narrow screen

            if is_wide_screen:
                # Alternate between left and right columns
                if left_line_count <= right_line_count:
                    left_line_count += entry_lines
                else:
                    right_line_count += entry_lines
                max_line_count = max(left_line_count, right_line_count)
            else:
                # Only one column, so add to the left line count
                left_line_count += entry_lines
                max_line_count = left_line_count

            # Check if we need to create a page break
            if max_line_count > lines_per_page:
                if index-1 >= current_page_start:
                    self.page_breaks.append((current_page_start, index - 1))
                current_page_start = index
                left_line_count = entry_lines if is_wide_screen else 0
                right_line_count = 0

        # Add the final page break
        if not self.page_breaks or current_page_start < len(rendered_entries):
            last_index = len(rendered_entries) - 1
            if last_index >= current_page_start:
                self.page_breaks.append((current_page_start, last_index))

        return rendered_entries


    def handle_timeline_view_key(self, key, key_status_array):
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return


        if key == 'Escape' or key == 'Enter':
            #self.util.sid_data.menu.return_from_gosub()
            #self.util.sid_data.setCurrentAction("wait_for_menu")
            self.callback_on_exit()
            return
        # keyStatusArray = [shiftPressed, ctrlKeyPressed, altgrPressed]
        elif key == 'ArrowDown' or key == 'ArrowRight':
            print("PAGE BREAKS:")
            print(self.page_breaks)
            print(str(self.current_page)+"<"+str(len(self.page_breaks)))
            if self.current_page < len(self.page_breaks): 
                self.current_page += 1
                #print("Navigating to Page:", self.current_page)
                self.util.clear_screen()
                self.show_timeline(self.current_page)
            return
        elif key == 'ArrowUp' or key == 'ArrowLeft':
            if self.current_page > 1:
                self.current_page -= 1
                self.util.clear_screen()
                self.show_timeline(self.current_page)
            return
        elif key == 'c':
            
            self.add_timeline_entry() 
            return
        elif key == 'i':
            self.util.emit_uploadANSI('Timeline')


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
        #self.util.emit_waiting_for_input(True, 12)
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
        #if line_index < len(self.input_values):
        print("PRINTING")

        print(line_index)
        print(self.sid_data.input_values[line_index])
        self.output_with_color(0, line_index, self.sid_data.input_values[line_index], None, 0)

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
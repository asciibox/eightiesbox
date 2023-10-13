class MenuTextEditor:
    def __init__(self, sid_data, output_function, ask_function, goto_next_line, clear_screen, emit_gotoXY, clear_line):
        self.keys = {
            0: [49, 50, 51, 52, 53, 54, 55, 56, 57, 48],
            1: [218, 191, 192, 217, 196, 179, 195, 180, 193, 194],
            2: [201, 187, 200, 188, 205, 186, 204, 185, 202, 203],
            3: [251, 184, 212, 190, 205, 179, 198, 181, 207, 209],
            4: [161, 183, 211, 135, 179, 186, 199, 182, 208, 144],
            5: [197, 206, 139, 140, 232, 163, 155, 156, 153, 239],
            6: [176, 177, 178, 219, 223, 220, 124, 141, 254, 250],
            7: [1, 2, 3, 4, 5, 6, 196, 127, 14, 207],
            8: [24, 25, 24, 25, 16, 17, 23, 23, 20, 21],
            9: [174, 175, 61, 243, 169, 170, 253, 246, 171, 172],
            10: [149, 241, 20, 21, 235, 157, 227, 167, 251, 252],
            11: [162, 225, 147, 228, 230, 232, 235, 236, 237, 237],
            12: [128, 135, 165, 164, 152, 159, 44, 249, 173, 168],
            13: [131, 132, 133, 160, 248, 134, 142, 143, 145, 146],
            14: [136, 137, 138, 130, 144, 140, 139, 141, 161, 158],
            15: [147, 148, 149, 224, 167, 150, 129, 151, 163, 154]
        }

        self.characterSet = 0
        self.foregroundColor = 7
        self.clear_screen = clear_screen
        self.sid_data = sid_data
        self.output = output_function
        self.ask = ask_function
        self.goto_next_line = goto_next_line
        self.emit_gotoXY = emit_gotoXY

        self.current_line_index = 0  # For navigating vertically among characters
        self.current_line_x = 1
        self.clear_line = clear_line

        self.clear_screen()
        self.update_first_line()
        self.display_editor()
        

    def draw_line(self, line_index):
        # Display the key on the left with color 6
        char_value = self.sid_data.menu_box.values[line_index][2]  # Assuming 'Key' field is the character.
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(line_index + 1)
        self.output_with_color(0, line_index + 1, char_value, 6)
        
        # Display the input value with color 6
        self.sid_data.setStartX(1)
        if line_index < len(self.sid_data.input_values):
            self.output_with_color(1, line_index + 1, self.sid_data.input_values[line_index], None)


    def output_with_color(self, x, y, text, color):
        print("TEXT:"+text)
        if text == None or text == "":
            return
        # Initialize variables to keep track of current color and text batch
        current_color = color  # Initialize to the input color
        current_text = ""

        for idx, char in enumerate(text):
            cur_x = x + idx
            cur_y = y -1

            # Safely get stored color for the current position
            if cur_y < len(self.sid_data.color_array) and cur_x < len(self.sid_data.color_array[cur_y]):
                stored_color = self.sid_data.color_array[cur_y][cur_x]
            else:
                stored_color = None

            # Check if color at the current position matches the new color
            if stored_color is not None and stored_color != color:
                # If the color changes, output the current text batch
                if current_text:
                    self.output(current_text, current_color, 0)

                # Reset current_text and update the current_color
                current_text = char
                current_color = stored_color
            else:
                # If the color is the same, append the character to the current text batch
                current_text += char

        # Output any remaining text
        if current_text:
            print("OUTPUT:"+text)
            self.output(current_text, current_color, 0)
       

    def display_editor(self):
        for idx, _ in enumerate(self.sid_data.menu_box.values):
            self.draw_line(idx)
        self.emit_gotoXY(1, 1)


    def handle_key(self, key):
        print("handle key claled")
        print(key)
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock', 'Tab']:
            return

        if key == 'ArrowDown':
            if self.current_line_index < len(self.sid_data.menu_box.values) - 1:
                self.current_line_index += 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'ArrowUp':
            if self.current_line_index > 0:
                self.current_line_index -= 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        if key == 'ArrowRight':
            if self.current_line_x < self.sid_data.xWidth - 1:
                self.current_line_x += 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'ArrowLeft':
            if self.current_line_x > 1:
                self.current_line_x -= 1

                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'Enter':
            self.current_line_x = 1
            self.current_line_index = self.current_line_index + 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'Alt':
            print(self.sid_data.input_values[self.current_line_index])
            self.characterSet = self.characterSet + 1
            if self.characterSet > 14:
                self.characterSet = 0
            self.update_first_line()
            return

        elif key == 'Backspace':
            if self.current_line_x > 1:

                current_x = self.current_line_x-2

                current_str = self.sid_data.input_values[self.current_line_index]

                # Construct a new string with the changed character
                new_str = current_str[:current_x] + current_str[current_x + 1:]

                # Assign the new string back to the list
                self.sid_data.input_values[self.current_line_index] = new_str
                self.clear_line(self.current_line_index+1)
                self.draw_line(self.current_line_index)
                self.emit_gotoXY(self.current_line_x-1, self.current_line_index + 1)

        elif key == 'Control':
            self.foregroundColor = self.foregroundColor + 1
            if self.foregroundColor > 14:
                self.foregroundColor = 0
            self.update_first_line()
            return

        elif key == 'Delete':
            current_str = self.sid_data.input_values[self.current_line_index]
            
            if self.current_line_x <= len(current_str):  # Ensure the cursor is within the line length
                current_x = self.current_line_x - 1
                new_str = current_str[:current_x] + current_str[current_x + 1:]

                # Assign the new string back to the list
                self.sid_data.input_values[self.current_line_index] = new_str

                # Shift color codes to the left in self.sid_data.color_array
                cur_y = self.current_line_index
                for idx in range(current_x, len(self.sid_data.color_array[cur_y]) - 1):
                    self.sid_data.color_array[cur_y][idx] = self.sid_data.color_array[cur_y][idx + 1]
                self.sid_data.color_array[cur_y][-1] = None  # Clear the last position

                # Use draw_line to redraw the entire line
                self.clear_line(cur_y+1)
                self.draw_line(cur_y)

                # Move the cursor back to its original position
                self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)


        elif key == 'Escape':
            self.sid_data.menu_box.draw_all_rows()
            self.sid_data.setCurrentAction("wait_for_menu")
            return

        # Handling special characters
        special_chars = {
            "ä": chr(132),
            "ö": chr(148),
            "ü": chr(129),
            "ß": chr(223),
            "Ä": chr(142),
            "Ö": chr(153),
            "Ü": chr(154)
        }

        if key in special_chars:
            key = special_chars[key]

        if key.isdigit() and len(key) == 1:
            if key!="0":
                key_index = int(key)
                ascii_value = self.keys[self.characterSet][key_index-1]
                key = chr(ascii_value)
            else:
                key_index = int("9")
                ascii_value = self.keys[self.characterSet][key_index]
                key = chr(ascii_value)

        # Handle character input
        if len(key) == 1:  # Check if it's a single character input
            current_x = self.current_line_x -1
            while len(self.sid_data.input_values) <= self.current_line_index:
                self.sid_data.input_values.append("")

            if not self.sid_data.input_values[self.current_line_index]:
                self.sid_data.input_values[self.current_line_index] = ""
            # Get the current string at the specified line index
            current_str = self.sid_data.input_values[self.current_line_index]

            # Check if the length of current_str[:current_x] is shorter than the position of current_x
            if len(current_str) <= current_x:
                # Pad current_str with spaces until its length matches current_x
                current_str += ' ' * (current_x - len(current_str) + 1)

            # Construct a new string with the changed character
            new_str = current_str[:current_x] + key + current_str[current_x + 1:]

            # Assign the new string back to the list
            self.sid_data.input_values[self.current_line_index] = new_str
            
            self.sid_data.setStartX(self.current_line_x)
            self.sid_data.setStartY(self.current_line_index+1)

            self.output(key, self.foregroundColor, 0 )
            self.set_color_at_position(current_x+1, self.current_line_index, self.foregroundColor)
            self.current_line_x = self.current_line_x+1

    def update_first_line(self):
        # Navigate to the first line
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)

        # Output a 5-character block with the current foreground color as background color
        for _ in range(5):
            self.output(' ', self.foregroundColor, self.foregroundColor)

        # Output an empty space 15 times with bg colors ranging from 0 to 15
        for bg_color in range(16):
            self.output(' '*2, 7, bg_color)

        # Output the formatted number sequences with their respective ASCII character values
        for idx, num in enumerate("1234567890"):
            self.output(f'{num}=', 7, 0)
            self.output(chr(self.keys[self.characterSet][idx])+" ", 7, 0)

        padded_characterSet = str(self.characterSet+1).zfill(2)
        self.output(padded_characterSet, 6, 0)

        # You may want to reset the cursor to its original position after updating the line
        # Assuming self.sid_data.cursorX and self.sid_data.cursorY store the original cursor position
        self.sid_data.setStartX(self.sid_data.cursorX)
        self.sid_data.setStartY(self.sid_data.cursorY)

    def set_color_at_position(self, x, y, color):
        # Expand the array to fit the given coordinates, if necessary
        while len(self.sid_data.color_array) <= y:
            self.sid_data.color_array.append([])

        while len(self.sid_data.color_array[y]) <= x:
            self.sid_data.color_array[y].append(None)

        # Set the color at the given coordinates
        self.sid_data.color_array[y][x] = color
        print(self.sid_data.color_array)
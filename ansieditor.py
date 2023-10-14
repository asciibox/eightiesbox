from menu2ansi import *
from menubar_ansieditor import *

class ANSIEditor:
    def __init__(self, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line, show_file_content):
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
        self.color_mapping = [
            'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'
        ]

        self.max_height = sid_data.yHeight # len(self.editor_values)


        self.show_file_content = show_file_content
        self.startX = 0
        self.ansi_string = ""
        self.characterSet = 0
        self.foregroundColor = 7
        self.backgroundColor = 0
        self.clear_screen = clear_screen
        self.sid_data = sid_data
        self.output = output_function
        self.ask = ask_function
        self.goto_next_line = goto_next_line
        self.emit_gotoXY = emit_gotoXY

        self.current_line_index = 0  # For navigating vertically among characters
        self.current_line_x = 0
        self.clear_line = clear_line
        self.mongo_client = mongo_client

        self.clear_screen()
        self.update_first_line()
        self.display_editor()

        sid_data.setCurrentAction("wait_for_ansieditor")
    
    
    def display_editor(self):
        for idx in range(0, self.max_height):
            self.draw_line(idx)
        self.emit_gotoXY(0, 1)


    def draw_line(self, line_index):
        # Display the key on the left with color 6
        # Display the input value with color 6
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(line_index+1)
        if line_index < len(self.sid_data.input_values):
            self.output_with_color(0, line_index, self.sid_data.input_values[line_index], None, 0)


    def output_with_color(self, x, y, text, color, bgcolor):
        if text == None or text == "":
            return
        # Initialize variables to keep track of current color and text batch
        current_color = color  # Initialize to the input color
        current_bgcolor = bgcolor  # Initialize to the input color
        current_text = ""

        for idx, char in enumerate(text):
            cur_x = x + idx +1
            cur_y = y

            # Safely get stored color for the current position
            if cur_y < len(self.sid_data.color_array) and cur_x < len(self.sid_data.color_array[cur_y]):
                stored_color = self.sid_data.color_array[cur_y][cur_x]
            else:
                stored_color = None

            # Safely get stored color for the current position
            if cur_y < len(self.sid_data.color_bgarray) and cur_x < len(self.sid_data.color_bgarray[cur_y]):
                stored_bgcolor = self.sid_data.color_bgarray[cur_y][cur_x]
            else:
                stored_bgcolor = None

            # Check if color at the current position matches the new color
            if (stored_color is not None and stored_color != color) or (stored_bgcolor is not None and stored_bgcolor != bgcolor):
                # If the color changes, output the current text batch
                if current_text:
                    self.output(current_text, current_color, current_bgcolor)

                # Reset current_text and update the current_color
                current_text = char
                current_color = stored_color
                current_bgcolor = stored_bgcolor
            else:
                # If the color is the same, append the character to the current text batch
                current_text += char

        # Output any remaining text
        if current_text:
            self.output(current_text, current_color, current_bgcolor)
       

  

    def handle_key(self, key):
        print("handle key claled")
        print(key)
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return

        if key == 'ArrowDown':
            if self.current_line_index < self.max_height - 1:
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
            if self.current_line_x > self.startX:
                self.current_line_x -= 1

                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'Enter':
            self.current_line_x = 1
            self.current_line_index = self.current_line_index + 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return
        
        elif key == 'Escape':
            if self.sid_data.current_action == "wait_for_menubar":
                self.sid_data.setCurrentAction("wait_for_ansieditor")
                self.sid_data.ansi_editor.clear_screen()
                self.sid_data.ansi_editor.update_first_line()
                self.sid_data.ansi_editor.display_editor()
            else:
                sub_menus = {
                        'File': ['Load ANSI', 'Save ANSI', 'Delete ANSI'],
                        'Edit': ['Clear ANSI', 'Leave menu bar'],
                    }
                self.sid_data.setMenuBar(MenuBarANSIEditor(sub_menus, self.sid_data, self.output, self.ask, self.mongo_client, self.goto_next_line, self.clear_screen, self.emit_gotoXY, self.clear_line, self.show_file_content))
                return

        elif key == 'Alt':
            self.display_ansi()
            self.characterSet = self.characterSet + 1
            if self.characterSet > 14:
                self.characterSet = 0
            self.update_first_line()
            return

        elif key == 'Backspace':
            if self.current_line_x > self.startX:

                current_x = self.current_line_x-2

                current_str = self.sid_data.input_values[self.current_line_index]

                # Construct a new string with the changed character
                new_str = current_str[:current_x] + current_str[current_x + 1:]

                # Assign the new string back to the list
                self.sid_data.input_values[self.current_line_index] = new_str

                cur_y = self.current_line_index
                for idx in range(current_x+1, len(self.sid_data.color_array[cur_y]) - 1):
                    self.sid_data.color_array[cur_y][idx] = self.sid_data.color_array[cur_y][idx + 1]
                    self.sid_data.color_bgarray[cur_y][idx] = self.sid_data.color_bgarray[cur_y][idx + 1]
                self.sid_data.color_array[cur_y][-1] = None  # Clear the last position
                self.sid_data.color_bgarray[cur_y][-1] = None  # Clear the last position

                self.clear_line(self.current_line_index+1)
                self.draw_line(self.current_line_index)
                self.emit_gotoXY(self.current_line_x-1, self.current_line_index + 1)
                self.current_line_x = self.current_line_x - 1

        elif key == 'Control':
            self.foregroundColor = self.foregroundColor + 1
            if self.foregroundColor > 15:
                self.foregroundColor = 0
            self.update_first_line()
            return

        elif key == 'Tab':
            self.backgroundColor = self.backgroundColor + 1
            if self.backgroundColor > 15:
                self.backgroundColor = 0
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
                    self.sid_data.color_bgarray[cur_y][idx] = self.sid_data.color_bgarray[cur_y][idx + 1]
                    
                self.sid_data.color_array[cur_y][-1] = None  # Clear the last position
                self.sid_data.color_bgarray[cur_y][-1] = None  # Clear the last position

                # Use draw_line to redraw the entire line
                self.clear_line(cur_y+1)
                self.draw_line(cur_y)

                # Move the cursor back to its original position
                self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
       
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
            current_x = self.current_line_x
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

            self.output(key, self.foregroundColor, self.backgroundColor )
            self.set_color_at_position(current_x+1, self.current_line_index, self.foregroundColor, self.backgroundColor)
            
            if self.current_line_x+1 < self.sid_data.xWidth:
                self.current_line_x = self.current_line_x+1
            else:
                self.emit_gotoXY(self.sid_data.xWidth-1, self.current_line_index+1)

    def update_first_line(self):
        # Navigate to the first line
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)

        # Output a 5-character block with the current foreground color as background color
        for _ in range(5):
            self.output(' ', self.foregroundColor, self.foregroundColor)
        for _ in range(5):
            self.output(' ', 6, self.backgroundColor)

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

    def set_color_at_position(self, x, y, color, bgcolor):
        # Expand the array to fit the given coordinates, if necessary
        while len(self.sid_data.color_array) <= y:
            self.sid_data.color_array.append([])

        while len(self.sid_data.color_array[y]) <= x:
            self.sid_data.color_array[y].append(None)

        while len(self.sid_data.color_bgarray) <= y:
            self.sid_data.color_bgarray.append([])

        while len(self.sid_data.color_bgarray[y]) <= x:
            self.sid_data.color_bgarray[y].append(None)

        # Set the color at the given coordinates
        self.sid_data.color_array[y][x] = color
        self.sid_data.color_bgarray[y][x] = bgcolor

    def display_ansi(self):
        print("dispaly_ansi")
        self.ansi_string = ""
        self.current_color = 7
        self.current_bgcolor = 0
        for idx in range(0, self.max_height):
            self.draw_ansi_line(idx)
        return self.ansi_string

    def draw_ansi_line(self, line_index):
        print("draw_ansi_line")
        print(str(line_index)+"<"+str(len(self.sid_data.input_values)))
        if line_index < len(self.sid_data.input_values):
            self.output_ansi_with_color(1, line_index, self.sid_data.input_values[line_index])

    def output_ansi_with_color(self, x, y, text):
        if not text:
            return

        self.current_color = -1  # Starting with no color set
        self.current_bgcolor = 0  # Starting with no color set
        current_text = ""

        self.ansi_string += cursor_to(x, y)

        for idx, char in enumerate(text):
            cur_x = x + idx
            cur_y = y
            
            if cur_y < len(self.sid_data.color_array) and cur_x < len(self.sid_data.color_array[cur_y]):
                stored_color = self.sid_data.color_array[cur_y][cur_x]
            else:
                stored_color = None

            if cur_y < len(self.sid_data.color_bgarray) and cur_x < len(self.sid_data.color_bgarray[cur_y]):
                stored_bgcolor = self.sid_data.color_bgarray[cur_y][cur_x]
            else:
                stored_bgcolor = None

            if stored_color != self.current_color:
                if current_text:
                    self.ansi_string += self._get_ansi_sequence(self.current_color, self.current_bgcolor) + current_text
                    current_text = ""
                self.current_color = stored_color
                self.current_bgcolor = stored_bgcolor

            current_text += char

        if current_text:
            self.ansi_string += self._get_ansi_sequence(self.current_color, self.current_bgcolor) + current_text

    def _get_ansi_sequence(self, color, bgcolor):
        ansi_sequence = ""
        
        # Foreground color
        if color is not None:
            if 0 <= color <= 7:
                ansi_sequence += "\033[22;{}m".format(30 + color)  # Reset bold and set standard colors
            elif 8 <= color <= 15:
                ansi_sequence += "\033[1;{}m".format(30 + (color - 8))  # Bold for bright colors
        
        # Background color
        if bgcolor is not None:
            if 0 <= bgcolor <= 7:
                ansi_sequence += "\033[{}m".format(40 + bgcolor)  # Standard background colors
            elif 8 <= bgcolor <= 15:
                ansi_sequence += "\033[{};5;{}m".format(48, bgcolor)  # 256-color mode for bright background colors

        return ansi_sequence



            
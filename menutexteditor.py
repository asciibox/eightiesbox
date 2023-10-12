class MenuTextEditor:
    def __init__(self, sid_data, output_function, ask_function, goto_next_line, clear_screen, emit_gotoXY):
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
        self.clear_screen()
        self.display_editor()

        self.keys = {
            0: [49, 50, 51, 52, 53, 54, 55, 56, 57, 48],
            1: [218, 191, 192, 217, 196, 179, 195, 180, 193, 194],
            2: [201, 203, 200, 188, 205, 186, 204, 185, 202, 203],
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

    def code(self):
        codestring = ""
        for i in range(1, 256):
            codestring += f"{i}:{chr(i)} "
        
        startX = 0  # Assuming startX starts at 0, change as needed
        startY = 0  # Assuming startY starts at 0, change as needed
        
        slice_length = 10  # Number of codes per slice
        for i in range(0, len(codestring), slice_length * 4):  # 4 characters per code (e.g., "128:A ")
            slice_str = codestring[i:i + slice_length * 4]
            self.sid_data.setStartX(startX);
            self.sid_data.setStartY(startY+1);
            self.output(slice_str, 14, 4)
            startY += 1  # Increment startY by 1


    def display_editor(self):
        for idx, char_list in enumerate(self.sid_data.menu_box.values):
            char_value = char_list[2]  # Assuming the 'Key' field is the character.
            self.sid_data.setStartX(0)
            print("setStartY:"+str(idx))
            self.sid_data.setStartY(idx+1)
            self.output(char_value, 6, 0)  # Display the key on the left
            self.sid_data.setStartX(2)
            print("len(self.input_values):"+str(len(self.sid_data.input_values)))
            if idx < len(self.sid_data.input_values):
                self.output(self.sid_data.input_values[idx], 6, 0)  # Display the key on the left
        print("display editor called")
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
            if self.current_line_x > 0:
                self.current_line_x -= 1

                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'Enter':
            self.current_line_x = 1
            self.current_line_index = self.current_line_index + 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return

        elif key == 'Alt':
            self.code()
            self.characterSet = self.characterSet + 1
            if self.characterSet > 14:
                self.characterSet = 0
            self.update_first_line()
            return

        elif key == 'Backspace':
            if self.current_line_x > 0:

                current_str = self.sid_data.input_values[self.current_line_index]

                # Construct a new string with the changed character
                new_str = current_str[:self.current_line_x] + current_str[self.current_line_x + 1:]

                # Assign the new string back to the list
                self.sid_data.input_values[self.current_line_index] = new_str
                self.sid_data.setStartX(self.current_line_x-1)
                self.output(' ', 7,0 )
                self.current_line_x -= 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)

        elif key == 'Control':
            self.foregroundColor = self.foregroundColor + 1
            if self.foregroundColor > 14:
                self.foregroundColor = 0
            self.update_first_line()
            return


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

            while len(self.sid_data.input_values) <= self.current_line_index:
                self.sid_data.input_values.append("")

            if not self.sid_data.input_values[self.current_line_index]:
                self.sid_data.input_values[self.current_line_index] = ""
            # Get the current string at the specified line index
            current_str = self.sid_data.input_values[self.current_line_index]

            # Check if the length of current_str[:self.current_line_x] is shorter than the position of self.current_line_x
            if len(current_str) <= self.current_line_x:
                # Pad current_str with spaces until its length matches self.current_line_x
                current_str += ' ' * (self.current_line_x - len(current_str) + 1)

            # Construct a new string with the changed character
            new_str = current_str[:self.current_line_x] + key + current_str[self.current_line_x + 1:]

            # Assign the new string back to the list
            self.sid_data.input_values[self.current_line_index] = new_str
            
            self.sid_data.setStartX(self.current_line_x)
            self.sid_data.setStartY(self.current_line_index+1)

            self.output(key, 7,0 )
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

        # You may want to reset the cursor to its original position after updating the line
        # Assuming self.sid_data.cursorX and self.sid_data.cursorY store the original cursor position
        self.sid_data.setStartX(self.sid_data.cursorX)
        self.sid_data.setStartY(self.sid_data.cursorY)
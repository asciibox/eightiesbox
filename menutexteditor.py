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




    def display_editor(self):
        for idx, char_list in enumerate(self.sid_data.menu_box.values):
            char_value = char_list[2]  # Assuming the 'Key' field is the character.
            self.sid_data.setStartX(0)
            print("setStartY:"+str(idx))
            self.sid_data.setStartY(idx)
            self.output(char_value, 6, 0)  # Display the key on the left
            self.sid_data.setStartX(1)
            print("len(self.input_values):"+str(len(self.sid_data.input_values)))
            if idx < len(self.sid_data.input_values):
                self.output(self.sid_data.input_values[idx], 6, 0)  # Display the key on the left
        print("display editor called")
        self.emit_gotoXY(2, 0)

    def handle_key(self, key):
        print("handle key claled")
        print(key)
        if key in ['AltGraph', 'Shift', 'Control', 'Dead', 'CapsLock', 'Tab']:
            return

        if key == 'ArrowDown':
            if self.current_line_index < len(self.sid_data.menu_box.values) - 1:
                self.current_line_index += 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index)
            return

        elif key == 'ArrowUp':
            if self.current_line_index > 0:
                self.current_line_index -= 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index)
            return

        if key == 'ArrowRight':
            if self.current_line_x < self.sid_data.xWidth - 1:
                self.current_line_x += 1
                self.emit_gotoXY(self.current_line_x, self.current_line_index)
            return

        elif key == 'ArrowLeft':
            if self.current_line_x > 0:
                self.current_line_x -= 1

                self.emit_gotoXY(self.current_line_x, self.current_line_index)
            return

        elif key == 'Enter':
            self.current_line_x = 1
            self.current_line_index = self.current_line_index + 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index)
            return

        elif key == 'Alt':
            self.characterSet = self.characterSet + 1
            if self.characterSet > 14:
                self.characterSet = 0
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
                self.emit_gotoXY(self.current_line_x, self.current_line_index)

        elif key == 'Shift':
            self.foregroundColor = self.foregroundColor + 1
            if self.foregroundColor > 14:
                self.foregroundColor = 0
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
            self.sid_data.setStartY(self.current_line_index)

            self.output(key, 7,0 )
            self.current_line_x = self.current_line_x+1

            
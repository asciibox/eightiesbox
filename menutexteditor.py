class MenuTextEditor:
    def __init__(self, sid_data, output_function, ask_function, goto_next_line, clear_screen, emit_gotoXY):
        self.clear_screen = clear_screen
        self.sid_data = sid_data
        self.output = output_function
        self.ask = ask_function
        self.goto_next_line = goto_next_line
        self.emit_gotoXY = emit_gotoXY

        self.current_line_index = 0  # For navigating vertically among characters
        self.current_line_x = 0
        self.clear_screen()
        self.display_editor()

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

    def handle_key(self, key):
        print("handle key claled")
        if key in ['Alt', 'AltGraph', 'Shift', 'Control', 'Dead', 'CapsLock', 'Tab']:
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

            
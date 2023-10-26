from menu2ansi import *
from menubar_ansieditor import *
from menubar_menutexteditor import *
import datetime

class BasicANSI:
    def __init__(self, util):
        # Add your BasicANSI initialization code here
        self.ansi_string = ""
        self.foregroundColor = 7
        self.backgroundColor = 0
        
        self.max_height = util.sid_data.sauceHeight # len(self.editor_values)
        self.sid_data = util.sid_data
        self.emit_gotoXY = util.emit_gotoXY
        self.util = util
            
        self.color_array = util.sid_data.color_array
        self.color_bgarray = util.sid_data.color_bgarray
        self.input_values = util.sid_data.input_values

        pass

    def display_editor(self, color_array, color_bgarray, input_values, menu_values):
        self.color_array = color_array
        self.color_bgarray = color_bgarray
        self.input_values = input_values
        
        if self.sid_data.xWidth < 50 and menu_values != None:
            self.util.clear_screen()
            self.util.sid_data.startX  = 0
            self.util.sid_data.startY  = 0
            for line_index in range(0, self.max_height):
                action_value = menu_values[line_index][0]  # Assuming 'Key' field is the character.
                if len(str(action_value))==2:
                    char_value = menu_values[line_index][2]  # Assuming 'Key' field is the character.
                    self.util.output(char_value, 6, 0)
                    self.util.output(" ", 6,0)
                    self.display_menu_name(int(action_value[0]), int(action_value[1]), self.util.menu_structure)
                    self.util.goto_next_line()

        else:
            for idx in range(0, self.max_height):
                self.draw_line(idx)
            self.emit_gotoXY(0, 1)

    def display_menu_name(self, first_field, second_field, menu_structure):
        # Validate first_field and second_field
        menu_keys = list(menu_structure.keys())
        if first_field < 0 or first_field >= len(menu_keys):
            self.util.output("text: Invalid first_field "+str(first_field), 6, 0)
            return

        menu_name = menu_keys[first_field]
        submenu = menu_structure[menu_name]

        second_field = second_field - 1

        if second_field < 0 or second_field >= len(submenu):
            self.util.output("text: Invalid second_field"+str(second_field), 6, 0)
            return

        submenu_name = submenu[second_field]

        # Output the menu name and submenu name
        self.util.output(f"{submenu_name}", 6, 0)


    def draw_line(self, line_index):
        # Display the key on the left with color 6
        self.sid_data.setMapCharacterSet(True)
        # Display the input value with color 6
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(line_index+1)
        if line_index < len(self.input_values):
            self.output_with_color(0, line_index, self.input_values[line_index], None, 0)
        self.sid_data.setMapCharacterSet(False)


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
            if cur_y < len(self.color_array) and cur_x < len(self.color_array[cur_y]):
                stored_color = self.color_array[cur_y][cur_x]
            else:
                stored_color = None

            # Safely get stored color for the current position
            if cur_y < len(self.color_bgarray) and cur_x < len(self.color_bgarray[cur_y]):
                stored_bgcolor = self.color_bgarray[cur_y][cur_x]
            else:
                stored_bgcolor = None

            # Check if color at the current position matches the new color
            if (stored_color is not None and stored_color != color) or (stored_bgcolor is not None and stored_bgcolor != bgcolor):
                # If the color changes, output the current text batch
                if current_text:
                    self.util.output(current_text, current_color, current_bgcolor)

                # Reset current_text and update the current_color
                current_text = char
                current_color = stored_color
                current_bgcolor = stored_bgcolor
            else:
                # If the color is the same, append the character to the current text batch
                current_text += char

        # Output any remaining text
        if current_text:
            self.util.output(current_text, current_color, current_bgcolor)
    
    
    def display_ansi(self):
        self.ansi_string = ""
        self.current_color = 7
        self.current_bgcolor = 0
        for idx in range(0, self.max_height):
            self.draw_ansi_line(idx)
        return self.ansi_string

    def draw_ansi_line(self, line_index):
        print(str(line_index)+"<"+str(len(self.input_values)))
        if line_index < len(self.input_values):
            self.output_ansi_with_color(1, line_index, self.input_values[line_index])

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
            
            if cur_y < len(self.color_array) and cur_x < len(self.color_array[cur_y]):
                stored_color = self.color_array[cur_y][cur_x]
            else:
                stored_color = None

            if cur_y < len(self.color_bgarray) and cur_x < len(self.color_bgarray[cur_y]):
                stored_bgcolor = self.color_bgarray[cur_y][cur_x]
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
    
    def code(self):
            codestring = ""
            for i in range(128, 256):
                codestring += f"{i}:{chr(i)} "
            
            startX = 0  # Assuming startX starts at 0, change as needed
            startY = 0  # Assuming startY starts at 0, change as needed
            
            slice_length = 10  # Number of codes per slice
            for i in range(0, len(codestring), slice_length * 4):  # 4 characters per code (e.g., "128:A ")
                slice_str = codestring[i:i + slice_length * 4]
                self.emit_current_string(slice_str, 14, 4, False, startX, startY+1)
                startY += 1  # Increment startY by 1

            startX = 50  # Assuming startX starts at 0, change as needed
            self.sid_data.setMapCharacterSet(True)
            for i in range(0, len(codestring), slice_length * 4):  # 4 characters per code (e.g., "128:A ")
                slice_str = codestring[i:i + slice_length * 4]
                self.emit_current_string(slice_str, 14, 4, False, startX, startY+1)
                startY += 1  # Increment startY by 1
    
    def get_ansi_code_base64(self):

        ansi_code = self.display_ansi()
        # add sauce record if it does not exist already

        current_date = datetime.datetime.now()

        # Format the current date as a string in the desired format
        date_string = current_date.strftime("%Y%m%d")

        sauce = self.util.Sauce(
        columns=self.sid_data.sauceWidth,
        rows=self.sid_data.sauceHeight,
        title="",
        author="",
        group="",
        date=date_string,
        filesize=0,
        ice_colors=True,
        use_9px_font=True,
        font_name="IBM VGA",
        comments="Created with eightiesbox editor"
        )

        ansi_code = self.append_sauce_to_string(sauce, ansi_code)

        # Save the new file
        
        ansi_code_bytes = ansi_code.encode('cp1252')

        print("Last 128 bytes after decoding:", ansi_code_bytes[-128:])

        # Base64-encode the bytes
        ansi_code_base64 = base64.b64encode(ansi_code_bytes).decode('ascii')

        return ansi_code_base64
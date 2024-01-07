from menu2ansi import *
from menubar_ansieditor import *
from menubar_menutexteditor import *
from pycode.renderer import Renderer
import datetime

class BasicANSI:
    def __init__(self, util):
        # Add your BasicANSI initialization code here
        self.ansi_string = ""
        self.foregroundColor = 7
        self.backgroundColor = 0
        
        self.sid_data = util.sid_data
        self.emit_gotoXY = util.emit_gotoXY
        self.util = util
            
        self.color_array = util.sid_data.color_array
        self.color_bgarray = util.sid_data.color_bgarray
        self.input_values = util.sid_data.input_values

        self.yOffsetOnDraw = 0

        pass

    def set_text_values(self, color_array, color_bgarray, input_values, menu_values):
        self.color_array = color_array
        self.color_bgarray = color_bgarray
        self.input_values = input_values

   
       
    def count_menu_length(self, menu_values):
        if menu_values is None or not isinstance(menu_values, dict):
            return 0
        return max(menu_values.keys())+1 if menu_values else 0
    
    def is_user_in_required_groups(self, user_groups, required_groups):
        """
        Check if the user is a member of at least one of the required groups.

        :param user_groups: List of groups the user belongs to.
        :param required_groups: List of required groups for a specific action.
        :return: True if the user is in any of the required groups, False otherwise.
        """
        if not required_groups:
            return True

        for required_group in required_groups:
            if required_group in user_groups:
                return True

        return False
    
    def display_editor_for_editor(self, color_array, color_bgarray, input_values, menu_values):
        
        self.color_array = color_array
        self.color_bgarray = color_bgarray
        self.input_values = input_values
        self.max_height = self.util.sid_data.sauceHeight # len(self.editor_values)
       
        for idx in range(self.max_height):
                # Only process the idx if it exists in the dictionary
                self.draw_line(idx)



    def display_editor(self, color_array, color_bgarray, input_values, menu_values):
        
        self.color_array = color_array
        self.color_bgarray = color_bgarray
        self.input_values = input_values
        self.max_height = self.util.sid_data.sauceHeight # len(self.editor_values)
        print(self.max_height)
        
        for idx in range(self.max_height):
            if idx in menu_values:  # Check if idx is a valid key in menu_values
                command_value = int(menu_values[idx][0]) if menu_values[idx][0] != '' else 0
                
                if command_value == 4:
                    filename = menu_values[idx][1]
                    print("FILENAME:" + filename)
                    filename_without_extension, _ = os.path.splitext(filename)  # Split the filename from its extension

                    self.sid_data.setRenderer(Renderer(self.util, None))

                    # Determine modified filenames based on screen width
                    possible_filenames = []
                    if self.sid_data.xWidth > 80:
                        possible_filenames.append(filename_without_extension + '.html')
                    if self.sid_data.xWidth > 50:
                        possible_filenames.append(filename_without_extension + "_medium.html")
                    possible_filenames.append(filename_without_extension + "_small.html")

                    collection = self.util.mongo_client.bbs.uploads_html

                    for modified_filename in possible_filenames:
                        print("Checking file:", modified_filename)

                        # Convert the filename to a regex pattern for case-insensitive matching
                        filename_pattern = re.compile("^" + re.escape(modified_filename) + "$", re.IGNORECASE)

                        # Look for the filename in the database using a case-insensitive search
                        file_data = collection.find_one({"filename": filename_pattern, 'chosen_bbs': self.sid_data.chosen_bbs})

                        if file_data is not None:
                            print("File found:", modified_filename)
                            print("xWidth:", self.util.sid_data.xWidth)

                            # Check if xWidth is less than 50 or if the filename ends with '_small.html'
                            if self.util.sid_data.xWidth < 50 and "_small.html" in modified_filename:
                                print("Rendering _small.html")
                                self.sid_data.renderer.render_page(None, modified_filename)
                                print("Rendered page and returning")
                                return
                            elif self.util.sid_data.xWidth >= 50:
                                print("Rendering other format")
                                self.sid_data.renderer.render_page(None, modified_filename)
                                print("Rendered page and returning")
                                return

                    print("No suitable file found or render conditions not met")

        if self.sid_data.xWidth < 50 and menu_values is not None:
            self.process_small_menu_values(menu_values)
            return

        # No matching file found, handle accordingly
        if isinstance(menu_values, list):
            self.process_values(menu_values, self.max_height, None)

        elif isinstance(menu_values, dict):
            counter = 0
            for idx in range(self.max_height):
                if idx in menu_values:
                    # Only process the idx if it exists in the dictionary
                    self.process_values([menu_values[idx]], 1, counter)
                else:
                    self.draw_line(idx)
                counter += 1

        else:
            pass  # Handle the case when menu_values is neither a list nor a dictionary.


    def process_values(self, values, num_rows, idx2):
    
        for idx in range(num_rows):
            # Initialize variables
            security_value = 0
            required_groups = []
            value_y_condition = False  # Condition for values[idx][5] being "y"

            # Check if idx is within the range of values
            if values is not None and idx < len(values):
                security_value = int(values[idx][3]) if values[idx][3] != '' else 0

                # Check if element has enough items for index 4 and 5
                if len(values[idx]) > 4 and values[idx][4] != '':
                    required_groups = values[idx][4].split(',')
                if len(values[idx]) > 5:
                    value_y_condition = values[idx][5] == "y"

            user_groups = self.sid_data.user_document['groups'].split(',')

            # Condition to check group membership if value_y_condition is "y"
            is_user_in_groups = self.is_user_in_required_groups(user_groups, required_groups) if value_y_condition else True

            if not hasattr(self, 'draw_hotkeys'):
                # Check for user's security level and combined condition
                if (values is None or security_value <= self.sid_data.user_document['user_level']) and is_user_in_groups:
                    if idx2 is None:
                        print("Drawing line1 "+str(idx))
                        self.draw_line(idx)
                    else:
                        print("Drawing line2 "+str(idx2))
                        self.draw_line(idx2)
            else:
                if is_user_in_groups:
                    if idx2 is None:
                        print("Drawing line3 "+str(idx))
                        self.draw_line(idx)
                    else:
                        print("Drawing line4 "+str(idx2))
                        self.draw_line(idx2)
        self.emit_gotoXY(0, 1)



    def process_small_menu_values(self, menu_values):
        self.util.clear_screen()
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = 0

        #if isinstance(menu_values, list):
        #    for line_index in range(0, self.count_menu_length(menu_values)):
        #        self.process_line(menu_values, line_index)
        #elif isinstance(menu_values, dict):
        counter = 0
        for line_index in range(0, self.count_menu_length(menu_values)):
            
            if line_index not in menu_values:  # Check if row_idx exists in the dictionary
                    print(f"Row {line_index} not found in menu_values")
                    continue
            self.process_line(menu_values, line_index, counter)
            counter += 1

    def process_line(self, menu_values, line_index, counter):
        self.util.sid_data.startX = 0
        self.util.sid_data.startY = counter
        action_value = menu_values[line_index][0]  # Assuming 'Key' field is the character.
        key_value = menu_values[line_index][2]
        comment_value = menu_values[line_index][1]
        security_value = int(menu_values[line_index][3]) if menu_values[line_index][3] != '' else 0

        required_groups = menu_values[line_index][4].split(',') if len(menu_values[line_index]) > 4 and menu_values[line_index][4] != '' else []
        user_groups = self.sid_data.user_document['groups'].split(',')

        # Check if menu_values has the sixth element and set value_y_condition
        value_y_condition = False
        if len(menu_values[line_index]) > 5:
            value_y_condition = menu_values[line_index][5] == "y"

        # Check group membership if value_y_condition is "y"
        is_user_in_groups = self.is_user_in_required_groups(user_groups, required_groups) if value_y_condition else True

        if not hasattr(self, 'draw_hotkeys'):
            # Draw line based on security level and combined condition
            if security_value <= self.sid_data.user_document['user_level'] and is_user_in_groups:

                # Check for text in brackets in the comment
                start_idx = comment_value.find("(")
                end_idx = comment_value.find(")")
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    display_text = key_value + " " + comment_value[start_idx+1:end_idx]  # Include key_value before the extracted text
                else:
                    display_text = key_value

                if display_text:
                    self.util.output(display_text, 6, 0)
                    self.util.output(" ", 6, 0)
                    # Call display_menu_name only when the condition for not showing the menu name is not met
                    if not (start_idx != -1 and end_idx != -1 and end_idx > start_idx):
                        self.display_menu_name(int(action_value[0]), int(action_value[1]), self.util.menu_structure)
                    self.util.goto_next_line()

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
        # self.sid_data.setMapCharacterSet(True)
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(line_index+1+self.yOffsetOnDraw)
        if line_index < len(self.input_values):
            self.output_with_color(0, line_index, self.input_values[line_index], None, 0)
        # self.sid_data.setMapCharacterSet(False)


    def output_with_color(self, x, y, text, color, bgcolor):

        if text == None or text == "":
            return
        # Initialize variables to keep track of current color and text batch
        current_color = color  # Initialize to the input color
        current_bgcolor = bgcolor  # Initialize to the input color
        current_text = ""
        color_changed = False

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
                color_changed = True
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
            if current_color == None and current_bgcolor == 0 and color_changed == False:
                self.util.output(current_text, 7, 0)
            else:
                self.util.output(current_text, current_color, current_bgcolor)
    
    
    def display_ansi(self):
        print("self.input_values")
        print(self.input_values)
        self.max_height = self.util.sid_data.sauceHeight # len(self.editor_values)
        self.ansi_string = ""
        self.current_color = 7
        self.current_bgcolor = 0
        for idx in range(0, self.max_height):
            self.draw_ansi_line(idx)
        return self.ansi_string

    def draw_ansi_line(self, line_index):

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

    def setYOffsetOnDraw(self, value):
        self.yOffsetOnDraw = value
from menu2ansi import *
from menubar_ansieditor import *
from menubar_menutexteditor import *
from menubar_messageeditor import *
import datetime
from basicansi import *
import random
from menubar_uploadeditor import *

class ANSIEditor(BasicANSI):
    def __init__(self, util):
        super().__init__(util)
        self.util = util
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
            9: [174, 175, 61, 243, 169, 170 , 253, 246, 171, 172],
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

        self.emit_current_string=util.emit_current_string

        self.map_value = util.map_value
        self.list1 = util.list1
        self.list2 = util.list2


        self.show_file_content = util.show_file_content
        self.emit_uploadFile = util.emit_uploadFile
        self.startX = 0
        self.characterSet = 0
        self.pressedF9 = False
        self.clear_screen = util.clear_screen
        self.sid_data = util.sid_data
        self.output = util.output
        self.ask = util.ask
        self.goto_next_line = util.goto_next_line
        self.emit_gotoXY = util.emit_gotoXY

        self.current_line_index = 0  # For navigating vertically among characters
        self.current_line_x = 0
        self.clear_line = util.clear_line
        self.mongo_client = util.mongo_client

        self.append_sauce_to_string = util.append_sauce_to_string
        self.get_sauce = util.get_sauce
        self.strip_sauce = util.strip_sauce

        self.input_x = ""
        self.default_foregroundColor = 6
        self.default_backgroundColor = 0
       
    def start(self):
        self.clear_screen()
        self.update_first_line()
        self.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None )

    def check_key_by_subclass(self, key):
        return
    
    
       

  

    def handle_key(self, key):
        random_number = random.randint(1, 100)  # Generates a random integer between 1 and 100
        # print("KEY" + str(random_number))
        if key in ['AltGraph', 'Shift', 'Dead', 'CapsLock']:
            return

        if self.check_key_by_subclass and self.check_key_by_subclass(key) == True:
            return
            
        if key == 'AltGraph':
            return
        elif key == 'ArrowDown':
            self.arrow_down_pressed()

        elif key == 'ArrowUp':
            self.arrow_up_pressed()

        elif key == 'ArrowRight':
            self.arrow_right_pressed()

        elif key == 'ArrowLeft':
            self.arrow_left_pressed()
        
        elif key == 'Insert':
            self.sid_data.setInsert(not self.sid_data.insert)
            return

        elif key == 'Enter':
            self.enter_pressed()
        
        elif key == 'Escape':
            if self.sid_data.current_action == "wait_for_menubar_messageeditor":
                self.sid_data.setCurrentAction("wait_for_messageeditor")
                self.sid_data.message_editor.clear_screen()
                self.sid_data.message_editor.update_first_line()
                self.sid_data.message_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)
            elif self.sid_data.current_action == "wait_for_menubar_ansieditor":
                self.sid_data.setCurrentAction("wait_for_ansieditor")
                self.sid_data.ansi_editor.clear_screen()
                self.sid_data.ansi_editor.update_first_line()
                self.sid_data.ansi_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)
            elif self.sid_data.current_action == "wait_for_menubar_menueditor":
                print("RETURNING FROM MENUEDITOR")
            elif self.sid_data.current_action == "wait_for_messageeditor":
                sub_menus = {
                    'File': ['Send message', 'Exit message editor without saving'],
                    'Edit': ['Clear message', 'Hide menu bar'],
                }
                self.sid_data.setMenuBar(MenuBarMessageEditor(sub_menus, self.util))

                return
            elif self.sid_data.current_action == "wait_for_menutexteditor":
                sub_menus = {
                    'File': ['Leave ANSI editor', 'Load ANSI', 'Import uploaded ANSI'],
                    'Edit': ['Clear ANSI', 'Leave menu bar'],
                }
                self.sid_data.setMenuBar(MenuBarTextEditor(sub_menus, self.util))
                self.sid_data.setCurrentAction("wait_for_menubar_messageeditor")
                return
                
            elif self.sid_data.current_action == "wait_for_ansieditor":
                sub_menus = {
                        'File': ['Exit editor', 'Load ANSI', 'Save ANSI', 'Delete ANSI', 'Upload ANSI','Import uploaded ANSI','Delete uploaded ANSI'],
                        'Edit': ['Clear ANSI', 'Leave menu bar'],
                }
                self.sid_data.setMenuBar(MenuBarANSIEditor(sub_menus, self.util))

                self.sid_data.setCurrentAction("wait_for_menubar_ansieditor")
                return
            elif self.sid_data.current_action == "wait_for_uploadeditor":
                self.escape2MenuUploadEditor()
                return
            elif self.sid_data.current_action == "wait_for_editfile":
                self.escape2FileEditEditor()
                return

        elif key == 'Alt':
            #self.code()
            #current_str = self.sid_data.input_values[self.current_line_index][self.current_line_x]
            #print(ord(current_str[0]))
            if self.sid_data.current_action != "wait_for_ansieditor" and self.sid_data.current_action != "wait_for_menutexteditor":
                return

            self.display_ansi()
            self.characterSet = self.characterSet + 1
            if self.characterSet > 14:
                self.characterSet = 0
            self.update_first_line()
            return

        elif key == 'Backspace':
            if self.current_line_x > self.startX:
                
                if self.current_line_index >= len(self.sid_data.input_values):
                    # If the current_line_index is out of range, simply return
                    return

                current_x = self.current_line_x-1
                current_str = self.sid_data.input_values[self.current_line_index]

                # Additional check to see if the string is too short
                if current_x >= len(current_str):
                    self.emit_gotoXY(self.current_line_x-1, self.current_line_index + 1)
                    self.current_line_x = self.current_line_x - 1
                    return

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
                return

        elif key == 'Tab':
            if self.sid_data.current_action != "wait_for_ansieditor" and self.sid_data.current_action != "wait_for_menutexteditor":
                return
            self.foregroundColor = self.foregroundColor + 1
            if self.foregroundColor > 15:
                self.foregroundColor = 0
            self.update_first_line()
            return


        elif key == 'Delete':
            current_str = self.sid_data.input_values[self.current_line_index]
            
            if self.current_line_x <= len(current_str):  # Ensure the cursor is within the line length
                current_x = self.current_line_x
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
            return
       
        elif key == 'Home':
             self.current_line_x = 0
             self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
             return

        elif key == 'End':
             self.current_line_x = self.sid_data.sauceWidth
             self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
             return

        elif key == 'F12':
            if self.sid_data.current_action != "wait_for_ansieditor":
                return
            self.util.clear_screen()
            self.sid_data.startX = 0
            self.sid_data.startY = 0
            self.output("How many character horizontally (columns, x)? ", 6,0)
            self.util.ask(3, self.horizontal_callback)
            return            

        elif key == 'F9':
            self.pressedF9 = not self.pressedF9 # Toggle the state of pressedF9
            return

        elif key == 'F11':
            if self.foregroundColor < 8:
                self.foregroundColor += 8
            else:
                self.foregroundColor -= 8
            self.update_first_line()
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
        if len(key) == 1:
            self.keypress_event()
            current_x = self.current_line_x
            #print("current_x:"+str(current_x))
            #print("self.current_line_index"+str(self.current_line_index))
            #print("self.current_line_x"+str(self.current_line_x))

            while len(self.sid_data.input_values) <= self.current_line_index:
                self.sid_data.input_values.append("")
                
            current_str = self.sid_data.input_values[self.current_line_index]
            
            if len(current_str) < current_x:
                current_str += ' ' * (current_x - len(current_str))
                
            # Update the array with the padded string
            self.sid_data.input_values[self.current_line_index] = current_str
            #print("current_str:"+current_str)
            if self.sid_data.insert:
                print("insert_into_string")
                new_str = self.insert_into_string(current_str, current_x, key)
            else:
                # Overwrite mode doesn't change the length of the string
                print("overwrite mode")
                new_str = current_str[:current_x] + key + current_str[current_x + 1:]

            self.sid_data.input_values[self.current_line_index] = new_str
            #print("new_str:"+new_str)
            self.set_color_at_position(current_x+1, self.current_line_index, self.foregroundColor, self.backgroundColor)
            
            if self.sid_data.insert:
                self.draw_line(self.current_line_index)
                self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
            else:
                self.sid_data.setStartX(self.current_line_x)
                self.sid_data.setStartY(self.current_line_index + 1)
                self.output(key, self.foregroundColor, self.backgroundColor)
                
    # Additional logic for cursor movement could go here...

            self.go_to_the_right_horizontally()





        # Extract the function key number (e.g., 'F1' -> 1)
        try:
            fkey_num = int(key[1:])
        except ValueError:
            return

        if 1 <= fkey_num <= 8:
            if self.pressedF9:
                self.backgroundColor = fkey_num - 1  # Set background to one of the colors 0-7
                self.pressedF9 = False  # Reset the state of pressedF9
            else:
                self.foregroundColor = fkey_num - 1  # Set foreground to one of the colors 0-7
            self.update_first_line()
            self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)

    def shift_color_attributes_right_from(self, start_x, line_index):
        # Check if the line exists in color_array and color_bgarray
        while len(self.sid_data.color_array) <= line_index:
            self.sid_data.color_array.append([])
        while len(self.sid_data.color_bgarray) <= line_index:
            self.sid_data.color_bgarray.append([])

        # Append default colors to the end of the line to maintain the line length
        self.sid_data.color_array[line_index].append(self.default_foregroundColor)
        self.sid_data.color_bgarray[line_index].append(self.default_backgroundColor)
        
        # Start shifting colors from right to left, starting from the end.
        # Note that we start shifting from the next position (start_x + 1),
        # to preserve the original color at start_x.
        for i in range(len(self.sid_data.color_array[line_index]) - 1, start_x + 1, -1):
            self.sid_data.color_array[line_index][i] = self.sid_data.color_array[line_index][i-1]
            self.sid_data.color_bgarray[line_index][i] = self.sid_data.color_bgarray[line_index][i-1]

        while len(self.sid_data.color_array[line_index]) <= start_x + 1:
            self.sid_data.color_array[line_index].append(self.default_foregroundColor)
        while len(self.sid_data.color_bgarray[line_index]) <= start_x + 1:
            self.sid_data.color_bgarray[line_index].append(self.default_backgroundColor)

        # Now you can safely set the color without running into an IndexError
        self.sid_data.color_array[line_index][start_x + 1] = self.foregroundColor
        self.sid_data.color_bgarray[line_index][start_x + 1] = self.backgroundColor


    def keypress_event(self):
        pass

    def set_wait_for(self):
        self.sid_data.setCurrentAction("wait_for_ansieditor")

    def horizontal_callback(self, input):
        if (input!=''):
            self.input_x = input
            self.goto_next_line()
            self.output("How many character vertically (rows, y)? ", 6,0)
            self.util.ask(3, self.vertical_callback)
        else:
            self.start()
            self.set_wait_for()

    def vertical_callback(self, input):
        if (input!=''):
            if self.input_x.isnumeric() and input.isnumeric():
                myx = int(self.input_x)
                myy = int(input)
                if myx > 120:
                    myx = 120
                if myy > 80:
                    myy = 80
                if myx < 0:
                    myx = 0
                if myy < 0:
                    myy = 0
                self.sid_data.setSauceWidth(myx)
                self.sid_data.setSauceHeight(myy)
                self.start()
                self.set_wait_for()
        else:
            self.start()
            self.set_wait_for()


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

        self.output(" x="+str(self.sid_data.sauceWidth)+" y="+str(self.sid_data.sauceHeight)+" (F12)", 4, 0)
        
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

    def enter_pressed(self):
        self.current_line_x = 0  # Reset x coordinate to 0

        if self.max_height < self.sid_data.yHeight - 3:
            self.current_line_index += 1
            if self.current_line_index >= self.max_height:
                self.max_height = self.current_line_index + 1
                self.sid_data.sauceHeight = self.max_height
                self.update_first_line()
                self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
                return

            self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
            return
        else:
            if self.current_line_index < self.sid_data.yHeight - 3:
                self.current_line_index += 1  # Increment line index

            self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)  # Go to next line
            
    def arrow_down_pressed(self):
        if self.current_line_index < self.max_height:
            self.current_line_index += 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        
    def arrow_up_pressed(self):

        if self.sid_data.current_action == "wait_for_messageeditor":
                if self.current_line_index < 4:
                    return

        if self.current_line_index > 0:
            self.current_line_index -= 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        
    def arrow_right_pressed(self):
        if self.current_line_x < self.sid_data.sauceWidth - 1:
            self.current_line_x += 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        return
    
    def arrow_left_pressed(self):
        if self.current_line_x > self.startX:
            self.current_line_x -= 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        return
    
    def go_to_the_right_horizontally(self):
        if self.current_line_x + 1 < self.sid_data.sauceWidth:
            if not self.sid_data.insert:
                self.current_line_x += 1
        else:
            self.emit_gotoXY(self.sid_data.sauceWidth-1, self.current_line_index+1)
    
    def insert_into_string(self, current_str, current_x, key):
        # Make sure adding a character doesn't exceed the xWidth limit
        if len(current_str) < self.sid_data.sauceWidth:
            new_str = current_str[:current_x] + key + current_str[current_x:]
            self.shift_color_attributes_right_from(current_x, self.current_line_index)
            self.current_line_x += 1  # Move the cursor to the right
            return new_str
        # If it exceeds, you might want to handle this case, e.g., by not allowing the insert or beeping
        return current_str

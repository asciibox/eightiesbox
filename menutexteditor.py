from ansieditor import *

class MenuTextEditor(ANSIEditor):
    def __init__(self, util):
        super().__init__(util)

    def check_key_by_subclass(self, key):
        if key == 'ArrowRight':
            if self.current_line_x < self.sid_data.sauceWidth - 1:
                self.current_line_x += 1
            if (self.current_line_x > 1):
                self.draw_hotkeys()
            else:
                self.draw_first_two_characters()
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            return True

        elif key == 'ArrowLeft':
            if self.current_line_x > 0: 
                self.current_line_x -= 1

            if (self.current_line_x > 1):
                self.draw_hotkeys()
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            else:
                self.draw_first_two_characters()
                self.cursorX = self.current_line_x
                self.cursorY = self.current_line_index
                self.startX = self.current_line_x
                self.startY = self.current_line_index
                print(self.current_line_x)
                print("y:"+str(self.current_line_index))
                self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
            
            return True

    def set_wait_for(self):
        self.sid_data.setCurrentAction("wait_for_menutexteditor")

    # Display the key on the left
    def draw_hotkeys(self):
        for line_index in range(0, len(self.sid_data.menu_box.values)):
           
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(line_index + 1)
            if line_index < len(self.sid_data.menu_box.values) and line_index < len(self.sid_data.input_values):
                char_value = self.sid_data.menu_box.values[line_index][2]  # Assuming 'Key' field is the character.
                if char_value == "":
                    char_value = " "    
                self.output(char_value+"|", 6, 4)
            else:
                self.output(" |", 6, 4)

    def draw_first_two_characters(self):
      
            for idx in range(0, self.max_height):
                self.draw_line(idx)
                if idx < len(self.sid_data.input_values):
                    if len(self.sid_data.input_values[idx]) == 0:
                        self.clear_line(idx+1)
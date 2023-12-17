from ansieditor import *

class UploadEditor(ANSIEditor):
    def __init__(self, util):
        super().__init__(util)
        
        self.first_document = None

    def start(self):
        self.clear_screen()
        self.util.sid_data.color_array=[]
        self.util.sid_data.color_bgarray=[]
        self.util.sid_data.input_values=[]
        
        self.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None )

        db = self.util.mongo_client['bbs']
        # Output a 5-character block with the current foreground color as background color
        to_be_edited_collection = db['to_be_edited']

       # Retrieve the first document uploaded by the user
        user_id = self.sid_data.user_document['_id']
        self.first_document = to_be_edited_collection.find_one({'uploaded_by_user_id': str(user_id), 'chosen_bbs' : self.sid_data.chosen_bbs})

        self.update_first_line()

    def update_first_line(self):
        # Navigate to the first line
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)

        # Check if a document was found
        if self.first_document:
            print(self.first_document)
            self.util.output("File description: "+self.first_document['filename']+" ("+str(self.first_document['file_size'])+")", 6, 0)
            print("First document in 'to_be_edited' collection:", self.first_document)
        else:
            user_id = self.sid_data.user_document['_id']
            print("No documents found in 'to_be_edited' collection. User ID:"+str(user_id))
            self.util.output("No documents found which need a description", 1, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return


    def exit(self):
        print("EXITING")
        self.sid_data.menu.return_from_gosub()
        self.util.sid_data.setCurrentAction("wait_for_menu")

    def enter_pressed(self):
        self.current_line_x = 0  # Reset x coordinate to 0

        if self.current_line_index < 20:
            self.current_line_index += 1  # Increment line index

        self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)  # Go to next line
            
    def arrow_down_pressed(self):
        if self.current_line_index < 20:
            self.current_line_index += 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        
    def arrow_right_pressed(self):
        if self.current_line_x < 40:
            self.current_line_x += 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index+1)
        return


    def go_to_the_right_horizontally(self):
        if self.current_line_x + 1 < 40:
            if not self.sid_data.insert:
                self.current_line_x += 1
        else:
            self.emit_gotoXY(self.sid_data.sauceWidth-1, self.current_line_index+1)

    def insert_into_string(self, current_str, current_x, key):
        # Make sure adding a character doesn't exceed the xWidth limit
        print("LEN")
        print(str(len(current_str)))
        if len(current_str) < 40:
            new_str = current_str[:current_x] + key + current_str[current_x:]
            self.shift_color_attributes_right_from(current_x, self.current_line_index)
            self.current_line_x += 1  # Move the cursor to the right
            return new_str
        # If it exceeds, you might want to handle this case, e.g., by not allowing the insert or beeping
        return current_str

    def escape2MenuUploadEditor(self):
        sub_menus = {
            'File': ['Save and proceed', 'Save and exit', 'Exit without saving'],
            'Edit': ['Clear description', 'Leave menu bar'],
        }
        print(self.first_document)
        self.sid_data.setMenuBar(MenuBarUploadEditor(sub_menus, self.util, self.first_document['file_id']))

        self.sid_data.setCurrentAction("wait_for_menubar_ansieditor")
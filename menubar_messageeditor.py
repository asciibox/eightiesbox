from datetime import datetime
from pymongo import MongoClient
from menubar import MenuBar
from menubar_ansieditor import MenuBarANSIEditor
import base64

''' When editing a message in the message area '''

class MenuBarMessageEditor(MenuBarANSIEditor):
    def __init__(self, sub_menus, util):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_messageeditor")

        # Add ANSI-specific methods here if needed
    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_messageeditor")
        self.util.clear_screen()

        # Optionally, redraw the editor to reflect these changes on the screen
        self.sid_data.message_editor.display_editor()


    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Send message":
                self.send_message()            
            if selected_option=="Exit message editor without saving":
                self.exit_message_editor()          
            if selected_option=="Clear message":
                self.clear_text()            
            if selected_option=="Hide menu bar":
                self.hide_menu_bar()            
            else:
                print("Hello world")
            
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def hide_menu_bar(self):
        self.in_sub_menu = False
        self.leave_menu_bar()
        # Reset to previous state or hide the menu bar

    def clear_text(self):
        # Clear the input values
        self.sid_data.input_values = []
        
        # Clear the color array
        self.sid_data.color_array = []

        # Clear the background color array
        self.sid_data.color_bgarray = []
        
        self.util.clear_screen()

        self.sid_data.message_editor.set_text_values([], [], [],[])

        # Optionally, redraw the editor to reflect these changes on the screen
        self.sid_data.message_editor.display_editor()

        self.leave_menu_bar()

    def send_message(self):

        all_page_contents = []

        self.sid_data.message_editor.save_current_page_data()
        # Loop through each page's list of input values
        for page in self.sid_data.message_editor.input_values_page:
            # Join the strings in the current page and append to all_page_contents
            page_content = "\n".join(page)
            all_page_contents.append(page_content)
        
        # Finally, join all pages' contents
        message_content = "\n".join(all_page_contents)
        
        # Fetch the current message area
        current_area = self.sid_data.current_message_area

        # Prepare the message data
        message_data = {
            "from": self.sid_data.user_name,  # Existing sender's user ID or name
            "to": self.sid_data.message_data['To'],  # Existing recipient's user ID or name
            "subject": self.sid_data.message_data['Subject'],  # Existing subject
            "area": current_area['name'],  # Existing message area
            "area_id": current_area['_id'],  # Existing area ID
            "content": message_content,  # Existing message content
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Current date and time
        }

        # Insert the message into the MongoDB database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        db['messages'].insert_one(message_data)

        # Optionally, notify the user that the message was sent
        self.util.output("Message sent successfully.", 7, 0)
        self.util.wait_with_message(self.exit_message_editor)
    

    def exit_message_editor(self):
        self.util.emit_waiting_for_input(False, 7)
        self.sid_data.setCurrentAction("wait_for_menu")
        self.sid_data.menu.return_from_gosub()

        

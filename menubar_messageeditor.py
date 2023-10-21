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
        self.clear_text()

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

        # Optionally, redraw the editor to reflect these changes on the screen
        self.sid_data.message_editor.display_editor()

    def send_message(self):
        # Collect the message content from self.sid_data.input_values
        message_content = "\n".join(self.sid_data.input_values)
        
        # Fetch the current message area
        current_area = self.sid_data.current_message_area

        # Prepare the message data
        message_data = {
            "from": self.sid_data.user_name,  # Replace with the actual sender's user ID or name
            "to": self.sid_data.message_data['To'],  # Replace with the actual recipient's user ID or name
            "subject": self.sid_data.message_data['Subject'],  # Replace with the actual recipient's user ID or name
            "area": current_area['name'],  # Message area
            "content": message_content,
            "is_read": False  # Add this line
        }

        # Insert the message into the MongoDB database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        db['messages'].insert_one(message_data)

        # Optionally, notify the user that the message was sent
        self.util.output("Message sent successfully.", 7, 0)
        self.util.wait_with_message(self.exit_message_editor)
    

    def exit_message_editor(self):
        self.sid_data.setCurrentAction("wait_for_menu")
        self.sid_data.menu.return_from_gosub()

        

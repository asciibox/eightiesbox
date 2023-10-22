from utils import *

class WhoIsOnline:
    def __init__(self, util, launchMenuCallback):
        self.util = util
        self.launchMenuCallback = launchMenuCallback

    def display_online_users(self):
        current_sid_data = self.util.sid_data  # get current user's sid_data
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)

        self.util.output("Who is Online:", 6, 0)
        self.util.goto_next_line()
        for index, (sid, sid_data) in enumerate(self.util.all_sid_data.items()):
            user_doc = sid_data.user_document
            
            # Make sure user_doc is not empty
            if not user_doc:
                continue

            if not user_doc['age']:
                user_doc['age']='?'
            if not user_doc['sex']:
                user_doc['sex']='?'
            if not user_doc['hobbies']:
                user_doc['hobbies']='?'
            
                
            display_str = f"{index + 1}. Username: {user_doc['username']}, Age: {user_doc['age']}, Sex: {user_doc['sex']}, Hobbies: {user_doc['hobbies']}"

            self.util.output(display_str, 6, 0)
            self.util.goto_next_line()

        self.util.wait_with_message(self.launchMenuCallback)

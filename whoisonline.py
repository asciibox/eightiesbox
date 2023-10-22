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
                self.util.output(str(index + 1)+". Logging in", 6, 0)
                self.util.goto_next_line()
                continue
                            
            display_str = f"{index + 1}. Username: {user_doc['username']}, Age: {user_doc.get('age', '?')}, Sex: {user_doc.get('sex', '?')}, Hobbies: {user_doc.get('hobbies', '?')}"


            self.util.output(display_str, 6, 0)
            self.util.goto_next_line()

        self.util.wait_with_message(self.launchMenuCallback)

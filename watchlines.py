import threading
import time
from utils import *

class WatchLines:
    def __init__(self, util, launchMenuCallback):
        self.util = util
        self.launchMenuCallback = launchMenuCallback

    def watch_lines(self):
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

        self.util.output_wrap('Which line do you want to watch?', 6, 0)
        self.util.ask(3, self.watch_callback)

    def watch_callback(self, value):
        try:
            line_index = int(value) - 1  # Convert to zero-based index
        except ValueError:
            self.util.output("Invalid input. Please enter a number.", 6, 0)
            self.launchMenuCallback()
            return

        # Check if the chosen line is valid
        if line_index < 0 or line_index >= len(self.util.all_sid_data):
            self.util.output("Invalid line number. Please try again.", 6, 0)
            return

        # Get the sid for the chosen line
        chosen_sid = list(self.util.all_sid_data.keys())[line_index]

        # Start watching the chosen line
        self.start_watching(chosen_sid)

    def start_watching(self, chosen_sid):
        self.util.sid_data.setCurrentAction("wait_for_watching_escape")
        self.util.clear_screen()
        self.is_watching = True
        self.watch_thread = threading.Thread(target=self.update_screen, args=(chosen_sid,))
        self.watch_thread.start()

    def update_screen(self, chosen_sid):
        while self.is_watching:
            chosen_sid_data = self.util.all_sid_data.get(chosen_sid, None)
            if chosen_sid_data:
                for screen_data in chosen_sid_data.screen_data_list:
                    self.util.socketio.emit('draw', screen_data, room=self.util.request_id)
            time.sleep(1)

    def stop_watching(self):
        self.is_watching = False
        if self.watch_thread.is_alive():
            self.watch_thread.join()
        self.launchMenuCallback()

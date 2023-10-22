from pymongo import MongoClient
from areachange import AreaChange

class MessageAreaChange(AreaChange):
    def __init__(self, util, callback=None):
        super().__init__(util)
        self.util = util
        self.displayed_areas = []  # Store the displayed message areas
        self.callback = callback  # Add the callback here

    def show_message_areas(self):
        self.util.clear_screen()
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        user_level = self.sid_data.user_level

        message_areas = list(db['messageareas'].find().sort('order'))

        self.displayed_areas.clear()
        
        areas_found = False
        for i, area in enumerate(message_areas):
            if area['min_level'] <= user_level:
                self.sid_data.setStartX(0)
                self.sid_data.setStartY(i)
                areas_found = True
                self.util.output(f"{i+1}. {area['name']}", 7, 0)
                self.displayed_areas.append(area)  # Add area to displayed_areas list

        if not areas_found:
            self.util.clear_screen()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(0)    
            self.util.output_wrap("No message areas found", 1, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(len(message_areas))
        self.util.output_wrap("Please enter the counter of the message area you'd like to access: ", 7, 0)
        self.util.ask(2, self.process_message_area_id)  # Assuming counter will be at most two digits

    def process_message_area_id(self, input_counter):
        try:
            selected_idx = int(input_counter) - 1
            selected_area = self.displayed_areas[selected_idx]
            self.sid_data.setCurrentMessageArea(selected_area)
            total_messages = self.get_total_messages(selected_area)
            unread_messages = self.get_unread_messages(selected_area)
            self.util.goto_next_line()
            self.util.output_wrap(f"You have accessed the message area: {selected_area['name']}", 7, 0)
            self.util.goto_next_line()
            self.util.output_wrap(f"Total Messages: {total_messages}", 7, 0)
            self.util.goto_next_line()
            self.util.output_wrap(f"Unread Messages: {unread_messages}", 7, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.access_callback)
            
        except (ValueError, IndexError):
            self.util.output_wrap("Invalid counter. Please try again.", 7, 0)
            self.show_message_areas()

    def access_callback(self):
        if self.callback:  # Invoke the callback if it's set
            self.callback()
            return

        self.exit()

    def exit(self):
        self.sid_data.menu.return_from_gosub()
        self.sid_data.setCurrentAction("wait_for_menu")

    def get_total_messages(self, selected_area):
        print(selected_area)
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        count = db['messages'].count_documents({"area_id": selected_area['_id']})
        return count

    def get_unread_messages(self, selected_area):
        user_id = self.util.sid_data.user_document['_id']
        area_id = selected_area['_id']

        # Connect to MongoDB
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']

        # Query read_messages for the current user and selected area
        read_messages_cursor = db['read_messages'].find({
            "user_id": user_id,
            "area_id": area_id
        })

        # Convert the cursor to a list of message IDs that have been read
        read_message_ids = [msg['message_id'] for msg in read_messages_cursor]

        # Count unread messages
        count = db['messages'].count_documents({
            "area_id": area_id,
            "_id": {'$nin': read_message_ids}
        })

        return count

from pymongo import MongoClient
from areachange import AreaChange

class MessageAreaChange(AreaChange):
    def __init__(self, util):
        super().__init__(util)
        self.util = util

    def show_message_areas(self):
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        user_level = self.sid_data.user_level

        # Get message areas sorted by 'order'
        message_areas = list(db['messageareas'].find().sort('order'))


        areas_found = False
        # Display message areas that the user is authorized to access
        for i, area in enumerate(message_areas):
            if area['min_level'] <= user_level:
                self.sid_data.setStartX(0)
                self.sid_data.setStartY(i)
                areas_found = True
                self.util.output(f"ID: {area['_id']} - {area['name']}", 7, 0)

        if (areas_found == False):
            self.util.output("No message areas found", 1,0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return

        # Ask for user input for message area ID
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(len(message_areas))
        self.util.output("Please enter the ID of the message area you'd like to access: ", 7, 0)
        self.ask(40, self.process_message_area_id)

    def process_message_area_id(self, input_id):
        # Validate and process the input ID (use the database to check the ID)
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']

        area = db['messageareas'].find_one({'_id': input_id})
        if area:
            self.sid_data.setCurrentMessageArea(area)
            self.util.output(f"You have accessed the message area: {area['name']}", 7, 0)
            # Continue with further operations here
            self.exit()
        else:
            self.util.output("Invalid ID. Please try again.", 7, 0)
            self.show_message_areas()  # Show the areas again for another attempt

    def exit(self):
        self.sid_data.menu.return_from_gosub()
        self.sid_data.setCurrentAction("wait_for_menu")

from pymongo import MongoClient

class MessageReader :
    def __init__(self, util, callback):
        self.util = util
        self.callback = callback

    def display_menu(self):
        # Clear the screen and set the coordinates
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)

        # Display the menu
        self.util.output("Message Reading Menu", 6, 0)
        self.util.goto_next_line()
        self.util.output("--------------------", 6, 0)
        self.util.goto_next_line()
        
        total_messages = self.get_total_messages()
        unread_messages = self.get_unread_messages()
        
        self.util.output(f"{self.util.sid_data.current_message_area['name']}", 6, 0)
        self.util.goto_next_line()
        self.util.output(f"Total Messages: {total_messages}", 6, 0)
        self.util.goto_next_line()
        self.util.output(f"Unread Messages: {unread_messages}", 6, 0)
        self.util.goto_next_line()
        self.util.output("--------------------", 6, 0)
        self.util.goto_next_line()

        if total_messages == 0:
            self.util.output("No messages found", 7, 0)
        else:
            self.util.output("F - Read Forward", 6, 0)
            self.util.goto_next_line()

            self.util.output("B - Read Backward", 6, 0)
            self.util.goto_next_line()

            self.util.output("U - Read Unread Messages (Forward)", 6, 0)
            self.util.goto_next_line()

            self.util.output("R - Read Unread Messages (Backward)", 6, 0)
            self.util.goto_next_line()
            self.util.goto_next_line()

        self.util.output("Control", 6, 0)
        self.util.goto_next_line()
        self.util.output("-------", 6, 0)
        self.util.goto_next_line()

        self.util.output("X - Exit to Main Menu", 6, 0)
        self.util.goto_next_line()

        self.util.output("H - Help", 6, 0)
        self.util.goto_next_line()
        self.util.goto_next_line()

        self.util.output("Select an option: ", 6, 0)
        self.util.ask(1, self.process_choice)

    def process_choice(self, choice):
        # Implement logic to handle the user's choice.
        if choice.lower() == 'f':
            self.read_forward()
        elif choice.lower() == 'b':
            self.read_backward()
        elif choice.lower() == 'u':
            self.read_unread_forward()
        elif choice.lower() == 'r':
            self.read_unread_backward()
        elif choice.lower() == 'n':
            self.next_message()
        elif choice.lower() == 'p':
            self.previous_message()
        elif choice.lower() == 'm':
            self.mark_for_later()
        elif choice.lower() == 's':
            self.search_by_keyword()
        elif choice.lower() == 'x':
            self.exit_to_main_menu()
        elif choice.lower() == 'h':
            self.show_help()
        else:
            self.util.output("Invalid choice. Please try again.", 6, 0)
            self.display_menu()

    def read_forward(self):
        # Get current area and its id
        current_area = self.util.sid_data.current_message_area
        area_id = current_area['_id']

        # Connect to MongoDB
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']

        # Find the next unread message in the current area
        next_unread_message = db['messages'].find_one(
            {"area_id": area_id, "is_read": False},
            sort=[('_id', 1)])  # Sorting by _id to get oldest unread message

        if next_unread_message:
            # Mark message as read
            db['messages'].update_one(
                {"_id": next_unread_message['_id']},
                {"$set": {"is_read": True}}
            )

            # Display the message
            self.util.clear_screen()
            self.util.output(f"From: {next_unread_message['from']}", 7, 0)
            self.util.goto_next_line()
            self.util.output(f"To: {next_unread_message['to']}", 7, 0)
            self.util.goto_next_line()
            self.util.output(f"Subject: {next_unread_message['subject']}", 7, 0)
            self.util.goto_next_line()
            self.util.output(next_unread_message['content'], 7, 0)
            self.util.goto_next_line()

        else:
            self.util.output("No more unread messages in this area.", 7, 0)


    def read_backward(self):
        pass  # Implement logic to read messages backward

    def read_unread_forward(self):
        pass  # Implement logic to read unread messages forward

    def read_unread_backward(self):
        pass  # Implement logic to read unread messages backward

    def next_message(self):
        pass  # Implement logic to jump to the next message

    def previous_message(self):
        pass  # Implement logic to jump to the previous message

    def mark_for_later(self):
        pass  # Implement logic to mark a message for later

    def search_by_keyword(self):
        pass  # Implement logic to search messages by keyword

    def exit_to_main_menu(self):
        self.callback()
        pass  # Implement logic to exit to the main menu

    def show_help(self):
        pass  # Implement logic to show a help menu


    def get_total_messages(self):
        current_area = self.util.sid_data.current_message_area
        print(self.util.sid_data.current_message_area)
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        count = db['messages'].count_documents({"area_id": current_area['_id']})
        return count

    def get_unread_messages(self):
        current_area = self.util.sid_data.current_message_area
        print(self.util.sid_data.current_message_area)
        # Assuming there's an "is_read" field in the message document to track read/unread status
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        count = db['messages'].count_documents({"area_id": current_area['_id'], "is_read": False})
        return count
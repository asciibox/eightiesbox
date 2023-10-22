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
        self.current_message_id = None

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
        self.db_filter=""
        self.sort_filter=""
        self.next = ""

        if total_messages == 0:
            self.util.output("No messages found", 7, 0)
        else:
            self.util.output("F - Read Forward", 6, 0)
            self.util.goto_next_line()

            self.util.output("B - Read Backward", 6, 0)
            self.util.goto_next_line()

            self.util.output_wrap("U - Read Unread Messages (Forward)", 6, 0)
            self.util.goto_next_line()

            self.util.output_wrap("R - Read Unread Messages (Backward)", 6, 0)
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

    def read_messages_with_filter_and_direction(self, db_filter, sort_direction, next):
        # Get current area and its id
        current_area = self.util.sid_data.current_message_area
        area_id = current_area['_id']
        self.db_filter = db_filter
        self.sort_direction = sort_direction
        self.next = next

        # Connect to MongoDB
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']

        read_messages = db['read_messages'].find({
        "user_id": self.util.sid_data.user_document['_id'],
        "area_id": area_id
        })

        read_message_ids = [msg['message_id'] for msg in read_messages]

        # Build your final filter without is_read
        final_filter = {**db_filter, "area_id": area_id, '_id': {'$nin': read_message_ids}}
        if self.current_message_id is not None:
            final_filter['_id'].update({'$gt': self.current_message_id} if sort_direction == 1 else {'$lt': self.current_message_id})

        next_message = db['messages'].find_one(
            final_filter,
            sort=[('_id', sort_direction)]
        )

        if next_message:
            # Update the current message ID
            self.current_message_id = next_message['_id']

            db['read_messages'].insert_one({
            "user_id": self.util.sid_data.user_document['_id'],
            "message_id": next_message['_id'],
            "area_id": area_id,
            })

            # Display the message header
            self.util.clear_screen()
            self.util.sid_data.startX = 0
            self.util.sid_data.startY = 0
            self.util.output(f"From: {next_message['from']}", 7, 0)
            self.util.goto_next_line()
            self.util.output(f"To: {next_message['to']}", 7, 0)
            self.util.goto_next_line()
            self.util.output_wrap(f"Subject: {next_message['subject']}", 7, 0)
            self.util.goto_next_line()

            # Set up the content lines and index
            self.current_message_content_lines = next_message['content'].split('\n')
            self.current_message_line_index = 0

            self.display_message_content()

            # If you're adding a prompt after the message, place it here.
            #self.util.output_wrap(f"Press Enter to read the {next} message or 'x' to stop: ", 7, 0)
            #self.util.ask(1, self.handle_input_for_reading)

        else:
            self.util.goto_next_line()
            self.util.output_wrap("No more messages matching your criteria.", 7, 0)
            self.util.goto_next_line()
            self.current_message_id = None  # Reset the current message ID as we've reached the end
            self.util.wait_with_message(self.exit_to_main_menu)

    def read_forward(self):
        self.read_messages_with_filter_and_direction({}, 1, 'next')

    def read_unread_forward(self):
        self.read_messages_with_filter_and_direction({}, 1, 'next')

    def read_backward(self):
        self.read_messages_with_filter_and_direction({}, -1, 'previous')

    def read_unread_backward(self):
        self.read_messages_with_filter_and_direction({}, -1, 'previous')

    def handle_input_for_reading(self, user_input):
        if user_input and user_input.lower() == 'x':
            self.exit_to_main_menu()
            self.current_message_id = None  # Reset the current message ID
        else:
            self.read_messages_with_filter_and_direction(self.db_filter, self.sort_direction, self.next)

    def display_message_content(self):
        yHeight_limit = self.util.sid_data.yHeight - 3  # Define a limit, adjust based on your needs

        for i in range(self.current_message_line_index, len(self.current_message_content_lines)):
            line = self.current_message_content_lines[i]

            # Check if you're at the end of the screen
            if self.util.sid_data.startY >= yHeight_limit:
                self.current_message_line_index = i  # Save current index
                self.util.output_wrap("Press any key for next page...", 7, 0)
                self.util.wait_with_message(self.continue_displaying_message)
                return  # Exit the loop and wait for user action

            self.util.output(line, 7, 0)
            self.util.goto_next_line()

        # Display prompt only after the entire message has been read
        self.show_next_message_prompt()

    def continue_displaying_message(self):
        # Clear the screen and reset the coordinates
        self.util.clear_screen()
        self.util.sid_data.startY = 0
        self.util.sid_data.startX = 0

        # If we're here, it means the user pressed a key to see the next page
        # We continue displaying the message from where we left off
        self.display_message_content()

    def show_next_message_prompt(self):
        self.util.output_wrap(f"Press Enter to read the {self.next} message or 'x' to stop: ", 7, 0)
        self.util.ask(1, self.handle_input_for_reading)

  
        
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
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        count = db['messages'].count_documents({"area_id": current_area['_id']})
        return count

    def get_unread_messages(self):
        current_area = self.util.sid_data.current_message_area
        user_id = self.util.sid_data.user_document['_id']
        area_id = current_area['_id']

        # Connect to MongoDB
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']

        # Query read_messages for the current user and area
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
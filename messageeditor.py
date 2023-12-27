from ansieditor import ANSIEditor
from pymongo import MongoClient
from userpicker import UserPicker

class MessageEditor(ANSIEditor):
    def __init__(self, util, callback_on_exit):
        super().__init__(util)
        self.callback_on_exit = callback_on_exit
        self.current_page = 0
        self.setup_interface()
        self.max_height = self.sid_data.yHeight-1

        self.input_values_page = [[]]
        self.color_array_page = [[]]
        self.color_bgarray_page = [[]]
        self.current_line_index_page = []

    def display_editor(self, write_header=True):
        print("DISPLY EDITOR CALLED")
        # Displaying "From:"

        if write_header:
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(0)
            from_user = self.sid_data.user_name
            self.output("From: ", 6, 0)
            self.output(from_user, 11, 0)

            # Moving to next line and displaying "To:"
            self.goto_next_line()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(1)  # Assuming Y index is 0-based
            to_user = self.sid_data.message_data.get("To", "data")
            self.output("To: ", 6, 0)
            self.output(to_user, 14, 4)

            # Moving to next line and displaying "Subject:"
            self.goto_next_line()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(2)  # Assuming Y index is 0-based
            subject = self.sid_data.message_data.get("Subject", "data")
            self.output("Subject: ", 6, 0)
            self.output(subject, 14, 4)

            self.current_line_index = 3  # For navigating vertically among characters
            self.current_line_x = 0

            for idx in range(3, self.max_height):
                self.draw_line(idx)
            self.emit_gotoXY(0, 4)
        else:
            for idx in range(0, self.max_height):
                self.draw_line(idx)
            self.emit_gotoXY(0, 0)

    def setup_interface(self):
        # Setting cursor position for "From:"
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        # Output "From:" in different colors, let's say fg=2 and bg=0
        from_user = self.sid_data.user_name
        self.output("From: ", 6,0)
        self.output(from_user, 11, 0)

        # Go to the next line for "To:"
        self.goto_next_line()

        # Callback method after receiving the input for "To:"
        
        
        # Ask for "To:"
        self.output("To (type 'All' for everybody): ", 6, 0)
        self.ask(35, self.to_input_callback)

    def to_input_callback(self, response):
    # Assume you've connected to MongoDB and got the users_collection object
    # client = MongoClient("mongodb://localhost:27017/")
    # users_collection = client.my_database.users
        if response.upper() == 'ALL':
            self.sid_data.message_data["To"] = response
            self.ask_subject()
            return

        db = self.util.mongo_client['bbs']
        users_collection = db['users']

        existing_user = users_collection.find_one({"username": response, 'chosen_bbs' : self.sid_data.chosen_bbs})
        
        if existing_user is None:
            # If the user does not exist, redirect to UserPicker class
            self.goto_user_picker(response)
        else:
            # If the user exist, proceed to ask_subject
            self.sid_data.message_data["To"] = response
            self.ask_subject()


    def user_picker_callback(self, username):
        self.sid_data.message_data["To"] = username
        self.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        self.util.output("From: ", 6,0 )
        self.util.output(self.util.sid_data.user_name, 11, 0)
        self.util.goto_next_line()
        self.util.output("To: "+username, 6, 0)
        self.ask_subject()

    def goto_user_picker(self, username):
        # You could initialize a UserPicker instance here, or however you've planned to navigate to UserPicker
        # Assume UserPicker is another class handling user picking functionalities
        self.util.sid_data.user_picker = UserPicker(self.util, username, self.user_picker_callback)
        self.util.sid_data.user_picker.show_options()

    def ask_subject(self):
        # Go to the next line for "Subject:"
        self.goto_next_line()

        # Callback method after receiving the input for "Subject:"
        def subject_input_callback(response):
            self.util.sid_data.setStartX(0)
            self.util.sid_data.setStartY(3)
            self.output("Press ESC and use cursor keys (< and >) to save", 6, 0)    
            self.sid_data.message_data["Subject"] = response
            self.util.sid_data.setStartX(0)
            self.util.sid_data.setStartY(4)
            self.util.emit_gotoXY(0, 4)
            self.current_line_index = 3
            self.sid_data.setCurrentAction("wait_for_messageeditor")

        self.output("Subject: ", 6, 0)
        # Ask for "Subject:"
        self.ask(35, subject_input_callback)

    def enter_pressed(self):
        super().enter_pressed()
        self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
        self.current_line_index_page[self.current_page] = self.current_line_index
        
        if self.current_line_index >= self.max_height - 2:
            self.save_current_page_data()
            self.current_page += 1
            self.current_line_index = 0
            self.update_page_data()

    def arrow_down_pressed(self):
        if self.current_line_index < self.max_height - 2:
            self.current_line_index += 1
            self.emit_gotoXY(self.current_line_x, self.current_line_index + 1)
            
            self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
            self.current_line_index_page[self.current_page] = self.current_line_index
            
        elif self.current_page < len(self.input_values_page) - 1:
            self.save_current_page_data()
            self.current_page += 1
            self.current_line_index = 0
            self.update_page_data()

    def arrow_up_pressed(self):
        super().arrow_up_pressed()
        
        self.ensure_page_index_exists(self.current_page, default_value=self.current_line_index)
        self.current_line_index_page[self.current_page] = self.current_line_index
        print(self.current_line_index)
        
        if self.current_line_index <= 6 and self.current_page > 0:
            self.save_current_page_data()
            self.current_page -= 1
            self.update_page_data()
            self.current_line_index = self.current_line_index_page[self.current_page]
            print("self.current_line_index restored: "+str(self.current_line_index))
            self.util.emit_gotoXY(0, self.util.sid_data.yHeight - 4)

    def ensure_page_index_exists(self, index, default_value=0):
        while len(self.current_line_index_page) <= index:
            self.current_line_index_page.append(default_value)

    def update_page_data(self):
         # Ensure the current page exists in the arrays
        while len(self.input_values_page) <= self.current_page:
            self.input_values_page.append([])  # Append an empty list for the new page
        while len(self.color_array_page) <= self.current_page:
            self.color_array_page.append([])
        while len(self.color_bgarray_page) <= self.current_page:
            self.color_bgarray_page.append([])

        self.sid_data.input_values = self.input_values_page[self.current_page]
        self.sid_data.color_array = self.color_array_page[self.current_page]
        self.sid_data.color_bgarray = self.color_bgarray_page[self.current_page]
        self.util.clear_screen()
        self.input_values = self.sid_data.input_values
        self.color_array = self.sid_data.color_array
        self.color_bgarray = self.sid_data.color_bgarray
        print("CLEARED")
        self.sid_data.message_editor.display_editor(self.current_page == 0)

    def save_current_page_data(self):
        self.input_values_page[self.current_page] = self.sid_data.input_values
        self.color_array_page[self.current_page] = self.sid_data.color_array
        self.color_bgarray_page[self.current_page] = self.sid_data.color_bgarray
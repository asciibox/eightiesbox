from ansieditor import ANSIEditor

class MessageEditor(ANSIEditor):
    def __init__(self, util, callback_on_exit):
        super().__init__(util)
        self.callback_on_exit = callback_on_exit
        self.message_data = {}  # A local variable to save all input fields
        self.setup_interface()

    def display_editor(self):
        print("DISPLY EDITOR CALLED")
        # Displaying "From:"
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(0)
        from_user = self.sid_data.user_name
        self.output("From: ", 6, 0)
        self.output(from_user, 11, 0)

        # Moving to next line and displaying "To:"
        self.goto_next_line()
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(1)  # Assuming Y index is 0-based
        to_user = self.message_data.get("To", "data")
        self.output("To: ", 6, 0)
        self.output(to_user, 14, 4)

        # Moving to next line and displaying "Subject:"
        self.goto_next_line()
        self.sid_data.setStartX(0)
        self.sid_data.setStartY(2)  # Assuming Y index is 0-based
        subject = self.message_data.get("Subject", "data")
        self.output("Subject: ", 6, 0)
        self.output(subject, 14, 4)

        self.current_line_index = 3  # For navigating vertically among characters
        self.current_line_x = 0

        print("DISPLY EDITOR FINISHED")
        for idx in range(4, self.max_height):
            self.draw_line(idx)
        self.emit_gotoXY(0, 4)

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
        self.output("To: ", 6, 0)
        self.ask(40, self.to_input_callback)

    def to_input_callback(self, response):
        self.message_data["To"] = response
        self.ask_subject()

    def ask_subject(self):
        # Go to the next line for "Subject:"
        self.goto_next_line()

        # Callback method after receiving the input for "Subject:"
        def subject_input_callback(response):
            self.message_data["Subject"] = response
            self.util.sid_data.setStartX(0)
            self.util.sid_data.setStartY(4)
            self.util.emit_gotoXY(0, 4)
            self.current_line_index = 3
            self.sid_data.setCurrentAction("wait_for_messageeditor")

        self.output("Subject: ", 6, 0)
        # Ask for "Subject:"
        self.ask(40, subject_input_callback)
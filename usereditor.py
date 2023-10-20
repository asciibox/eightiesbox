from basicansi import BasicANSI

class UserEditor(BasicANSI):
    def __init__(self, util, users, callback_on_exit):
        super().__init__(util)

        # Set the current action for the session
        util.sid_data.setCurrentAction("wait_for_user_editor")

        # Retrieve user data from the session
        self.user_name = util.sid_data.user_name
        self.user_level = util.sid_data.user_level

        # Retrieve the users collection from BBS
        self.users = users

        # Store the exit callback
        self.callback_on_exit = callback_on_exit

        # Display the user editor menu for the first time
        self.display_menu()

    def display_menu(self, clear_screen = True):
        """Displays the user editor menu."""

        if (clear_screen):
            self.util.clear_screen()
             # Set output coordinates
            self.util.sid_data.setStartX(0)
            self.util.sid_data.setStartY(0)


        self.util.goto_next_line()
        # Output the menu header
        self.util.output("List of users:", 6, 0)

        # Display list of users
        for user in self.users:
            self.util.goto_next_line()
            self.util.output(user['username'], 11, 0)

        self.util.goto_next_line()

        # Display menu options
        self.util.output("1. Change Username", 6, 0)
        self.util.goto_next_line()
        self.util.output("2. Change User Level", 6, 0)
        self.util.goto_next_line()
        self.util.output("X. Exit to main menu", 6, 0)
        self.util.goto_next_line()

        # Ask for user choice
        self.util.ask(1, self.process_choice)

    def process_choice(self, choice):
        """Processes the user's menu choice."""

        if choice.lower() == 'x':
            self.callback_on_exit()
            return

        try:
            choice_idx = int(choice)
            if choice_idx == 1:
                self.change_username()
            elif choice_idx == 2:
                self.change_user_level()
            else:
                self.util.goto_next_line()
                self.util.output("Invalid choice. Please try again.", 6,0)
                self.util.goto_next_line()
                self.display_menu(False)
                return

        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid input. Please try again.", 6,0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def change_username(self):
        """Ask for existing username before changing."""
        self.util.goto_next_line()
        self.util.output("Enter existing username:", 6, 0)
        self.util.ask(40, self.ask_new_username)

    def save_username(self, new_username):
        """Save the new username."""
        # Logic to save new username
        # Update users collection and session data
        self.user_name = new_username
        self.util.sid_data.user_name = new_username
        self.display_menu()

    def ask_new_username(self, existing_username):
        """Ask for new username."""
        if existing_username in [user['username'] for user in self.users]:
            self.util.goto_next_line()
            self.util.output("Enter new username:", 6, 0)
            self.util.ask(40, self.save_username)
        else:
            self.util.goto_next_line()
            self.util.output("Username not found. Try again!", 6, 0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def change_user_level(self):
        """Ask for existing username before changing user level."""
        self.util.goto_next_line()
        self.util.output("Enter username to change user level:", 6, 0)
        self.util.ask(40, self.ask_new_level)

    def ask_new_level(self, existing_username):
        """Ask for new user level."""
        if existing_username in [user['username'] for user in self.users]:
            self.util.goto_next_line()
            self.util.output("Enter new user level:", 6, 0)
            self.util.ask(40, self.save_user_level)
        else:
            self.util.goto_next_line()
            self.util.output("Username not found. Try again...", 6, 0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def save_user_level(self, new_level):
        """Save the new user level."""
        # Logic to save new user level
        # Update users collection and session data
        try:
            self.user_level = int(new_level)
            self.util.sid_data.user_level = self.user_level
            self.display_menu()
        except ValueError:
            self.util.output("Invalid user level. Please enter a number.", 6,0)
            self.display_menu()

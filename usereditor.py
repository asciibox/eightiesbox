from basicansi import BasicANSI

class UserEditor(BasicANSI):
    def __init__(self, util,  callback_on_exit):
        super().__init__(util)

        # Set the current action for the session
        util.sid_data.setCurrentAction("wait_for_user_editor")

        # Retrieve user data from the session
        self.user_name = util.sid_data.user_name
        self.user_level = self.sid_data.user_document['user_level']

          # Retrieve the users collection from BBS
        mongo_client = util.mongo_client  # Assuming util has a MongoDB client attribute
        db = mongo_client['bbs']
        self.users = list(db['users'].find({}))  # This will fetch all documents from the "users" collection

        # Store the exit callback
        self.callback_on_exit = callback_on_exit

        self.old_username = None  # Initialize with None or the current username if needed

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
        self.util.output_wrap("List of users:", 6, 0)

        # Display list of users
        for user in self.users:
            self.util.goto_next_line()
            self.util.output(user['username'], 11, 0)

        self.util.goto_next_line()

        # Display menu options
        self.util.output_wrap("1. Change Username", 6, 0)
        self.util.goto_next_line()
        self.util.output_wrap("2. Change User Level", 6, 0)
        self.util.goto_next_line()
        self.util.output_wrap("3. Delete user", 6, 0)
        self.util.goto_next_line()
        self.util.output_wrap("X. Exit to main menu", 6, 0)
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
            elif choice_idx == 3:
                self.delete_user()
            else:
                self.util.goto_next_line()
                self.util.output_wrap("Invalid choice. Please try again.", 6,0)
                self.util.goto_next_line()
                self.display_menu(False)
                return

        except ValueError:
            self.util.goto_next_line()
            self.util.outpu_wrapt("Invalid input. Please try again.", 6,0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def save_username(self, new_username):
        """Save the new username."""
        # Check if the new username is unique
        if new_username in [user['username'] for user in self.users]:
            self.util.output_wrap("Username already exists. Choose another.", 6, 0)
            self.display_menu()
            return

        # Update the users collection using the old username
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        update_result = db['users'].update_one({'username': self.old_username}, {'$set': {'username': new_username}})

        # Check if the update was successful
        if update_result.matched_count > 0:
            # Update session data
            self.util.sid_data.user_name = new_username

            # Update local username cache
            self.user_name = new_username

            # Update self.users
            for user in self.users:
                if user['username'] == self.old_username:
                    user['username'] = new_username
                    break

            self.display_menu()

        else:
            self.util.output_wrap("Error updating username. Try again.", 6, 0)
            self.display_menu()

        # Clear the old username now that the operation is complete
        self.old_username = None

    def change_username(self):
        """Ask for existing username before changing."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter existing username:", 6, 0)
        self.util.ask(35, self.ask_new_username)

    def ask_new_username(self, existing_username):
        """Ask for new username."""
        if existing_username in [user['username'] for user in self.users]:
            self.old_username = existing_username  # Store the old username
            self.util.goto_next_line()
            self.util.output_wrap("Enter new username:", 6, 0)
            self.util.ask(35, self.save_username)
        else:
            self.util.goto_next_line()
            self.util.output_wrap("Username not found. Try again!", 6, 0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def change_user_level(self):
        """Ask for existing username before changing user level."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter username to change user level:", 6, 0)
        self.util.ask(35, self.ask_new_level)

    def ask_new_level(self, existing_username):
        """Ask for new user level."""
        if existing_username in [user['username'] for user in self.users]:
            self.util.goto_next_line()
            self.util.output_wrap("Enter new user level:", 6, 0)
            self.util.ask(35, self.save_user_level)
        else:
            self.util.goto_next_line()
            self.util.output_wrap("Username not found. Try again...", 6, 0)
            self.util.goto_next_line()
            self.display_menu(False)
            return

    def save_user_level(self, new_level):
        """Save the new user level."""
        # Logic to save new user level
        if self.old_username is None:
            self.util.output_wrap("No username specified for user level update.", 6, 0)
            self.display_menu()
            return

        try:
            # Attempt to convert the new level to an integer
            user_level_int = int(new_level)

            # Update the users collection using the username
            mongo_client = self.util.mongo_client
            db = mongo_client['bbs']
            update_result = db['users'].update_one(
                {'username': self.old_username},
                {'$set': {'user_level': user_level_int}}
            )

            # Check if the update was successful
            if update_result.matched_count > 0:
                if update_result.modified_count > 0:
                    self.util.output_wrap("User level updated successfully.", 6, 0)
                else:
                    self.util.output_wrap("User level was already set to this value.", 6, 0)

                # Update the local user cache if necessary
                for user in self.users:
                    if user['username'] == self.old_username:
                        user['user_level'] = user_level_int
                        break
                if self.old_username == self.userdata['username']:
                    self.userdata['user_level'] = user_level_int
                self.display_menu()

            else:
                self.util.output_wrap("No matching user found for user level update.", 6, 0)
                self.display_menu()

        except ValueError:
            self.util.output_wrap("Invalid user level. Please enter a number.", 6, 0)
            self.display_menu()


    def delete_user(self):
        """Delete a user."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter username to delete:", 6, 0)
        self.util.ask(35, self.confirm_delete_user)

    def confirm_delete_user(self, username_to_delete):
        """Confirm if the user should be deleted."""
        if username_to_delete not in [user['username'] for user in self.users]:
            self.util.goto_next_line()
            self.util.output_wrap("Username not found. Try again!", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return
        
        self.user_to_delete = username_to_delete  # Store the username temporarily
        self.util.goto_next_line()
        self.util.output_wrap(f"Are you sure you want to delete {username_to_delete}? (Y/N)", 6, 0)
        self.util.ask(1, self.perform_delete_user)  # Asking for just one character (Y/N)

    def perform_delete_user(self, decision):
        """Perform the user deletion if confirmed."""
        if decision.lower() == 'y':
            # Proceed to delete the user
            mongo_client = self.util.mongo_client
            db = mongo_client['bbs']
            delete_result = db['users'].delete_one({'username': self.user_to_delete})

            if delete_result.deleted_count > 0:
                # Update self.users
                self.users = [user for user in self.users if user['username'] != self.user_to_delete]
                self.util.goto_next_line()
                self.util.output_wrap(f"User {self.user_to_delete} deleted successfully.", 6, 0)
            else:
                self.util.goto_next_line()
                self.util.output_wrap("Error deleting user. Try again.", 6, 0)
            
            # Clear the temporary username store
            self.user_to_delete = None
        else:
            self.util.goto_next_line()
            self.util.output_wrap("User deletion cancelled.", 6, 0)
        
        self.util.goto_next_line()
        self.display_menu()
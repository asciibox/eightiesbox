from basicansi import BasicANSI


class MailboxEditor(BasicANSI):  # Class name updated
    def __init__(self, util, callback_on_exit):
       super().__init__(util)
       self.util = util
       self.callback_on_exit = callback_on_exit

       # Set current action and retrieve session data
       util.sid_data.setCurrentAction("wait_for_mailbox_editor")  # Action name updated
       self.sid_data = util.sid_data
       self.mongo_client = util.mongo_client
       self.db = self.mongo_client['bbs']
       self.mailboxes = list(self.db['mailboxes'].find())  # Collection name updated

       self.display_menu()

    def display_menu(self):
       self.util.clear_screen()
       self.util.sid_data.setStartX(0)
       self.util.sid_data.setStartY(0)

       self.util.goto_next_line()
       self.util.output_wrap("Mailbox Editor Menu (Type 'x' to go back):", 6, 0)  # Menu title updated
       self.util.goto_next_line()

       # Display mailboxes with their numeric ID
       for idx, mailbox in enumerate(self.mailboxes, start=1):  # Variable name updated
           self.util.output_wrap(f"{idx}. {mailbox['name']}", 11, 0)  # Field name assumed as 'text'
           self.util.goto_next_line()

       self.util.goto_next_line()
       self.util.output_wrap("Choose action: [E] Edit, [D] Delete", 6, 0)
       self.util.goto_next_line()
       self.util.ask(1, self.choose_action)

    def choose_action(self, action):
        if action.lower() == 'x':
            self.callback_on_exit()
            return

        if action.lower() in ['e', 'd']:
            self.action = action.lower()
            self.util.goto_next_line()
            self.util.output_wrap("Enter the ID of the mailbox:", 6, 0)
            self.util.goto_next_line()
            self.util.ask(5, self.process_mailbox_id)
        else:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid action. Please enter 'E' for Edit or 'D' for Delete.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()

    def process_mailbox_id(self, mailbox_id):
        try:
            mailbox_id = int(mailbox_id) - 1  # Adjusting for zero-based index
            if mailbox_id < 0 or mailbox_id >= len(self.mailboxes):
                raise ValueError

            if self.action == 'e':
                self.edit_mailbox(mailbox_id)
            elif self.action == 'd':
                self.delete_mailbox(mailbox_id)
        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid ID. Please enter a valid numeric ID.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()

    def edit_mailbox(self, mailbox_id):
        """Start the process of editing an mailbox."""
        self.current_mailbox_id = mailbox_id
        self.util.goto_next_line()
        self.util.output_wrap("Enter new text for the mailbox:", 6, 0)
        self.util.ask(100, self.save_mailbox)

    def save_mailbox(self, new_text):
        """Save the edited mailbox."""
        if not new_text.strip():
            self.util.output_wrap("Mailbox text cannot be empty. Try again.", 6, 0)
            self.display_menu()
            return

        # Update the mailbox in the database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        mailbox_to_update = self.mailboxes[self.current_mailbox_id]

        update_result = db['mailboxes'].update_one(
            {'_id': mailbox_to_update['_id']},
            {'$set': {'name': new_text}}
        )

        # Check if the update was successful
        if update_result.matched_count > 0:
            self.util.output_wrap("mailbox updated successfully.", 6, 0)
            # Update local mailbox cache
            self.mailboxes[self.current_mailbox_id]['name'] = new_text
        else:
            self.util.output_wrap("Error updating mailbox. Try again.", 6, 0)

        self.display_menu()

    def delete_mailbox(self, mailbox_id):
        """Start the process of deleting an mailbox."""
        self.current_mailbox_id = mailbox_id
        self.util.goto_next_line()
        mailbox_to_delete = self.mailboxes[mailbox_id]['name']
        self.util.output_wrap(f"Are you sure you want to delete the following mailbox? '{mailbox_to_delete}' (Y/N)", 6, 0)
        self.util.ask(1, self.confirm_delete_mailbox)

    def confirm_delete_mailbox(self, confirmation):
        """Confirm and proceed with deletion of the mailbox."""
        if confirmation.lower() == 'y':
            mongo_client = self.util.mongo_client
            db = mongo_client['bbs']
            mailbox_to_delete = self.mailboxes[self.current_mailbox_id]

            delete_result = db['mailboxes'].delete_one({'_id': mailbox_to_delete['_id'], 'chosen_bbs': self.sid_data.chosen_bbs})

            if delete_result.deleted_count > 0:
                self.util.output_wrap("Mailbox deleted successfully.", 6, 0)
                # Remove the mailbox from the local cache
                del self.mailboxes[self.current_mailbox_id]
            else:
                self.util.output_wrap("Error deleting mailbox. Try again.", 6, 0)
        else:
            self.util.output_wrap("Deletion cancelled.", 6, 0)

        self.display_menu()
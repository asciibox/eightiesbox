from basicansi import BasicANSI

class OnelinerEditor(BasicANSI):
    def __init__(self, util, callback_on_exit):
        super().__init__(util)
        self.util = util
        self.callback_on_exit = callback_on_exit

        # Set current action and retrieve session data
        util.sid_data.setCurrentAction("wait_for_oneliner_editor")
        self.sid_data = util.sid_data
        self.mongo_client = util.mongo_client
        self.db = self.mongo_client['bbs']
        self.oneliners = list(self.db['oneliners'].find({'chosen_bbs': self.sid_data.chosen_bbs}))

        self.display_menu()

    def display_menu(self):
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)

        self.util.goto_next_line()
        self.util.output_wrap("Oneliner Editor Menu (Type 'x' to go back):", 6, 0)
        self.util.goto_next_line()

        # Display oneliners with their numeric ID
        for idx, oneliner in enumerate(self.oneliners, start=1):
            self.util.output_wrap(f"{idx}. {oneliner['text']}", 11, 0)
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
            self.util.output_wrap("Enter the ID of the oneliner:", 6, 0)
            self.util.goto_next_line()
            self.util.ask(5, self.process_oneliner_id)
        else:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid action. Please enter 'E' for Edit or 'D' for Delete.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()

    def process_oneliner_id(self, oneliner_id):
        try:
            oneliner_id = int(oneliner_id) - 1  # Adjusting for zero-based index
            if oneliner_id < 0 or oneliner_id >= len(self.oneliners):
                raise ValueError

            if self.action == 'e':
                self.edit_oneliner(oneliner_id)
            elif self.action == 'd':
                self.delete_oneliner(oneliner_id)
        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid ID. Please enter a valid numeric ID.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()

    def edit_oneliner(self, oneliner_id):
        """Start the process of editing an oneliner."""
        self.current_oneliner_id = oneliner_id
        self.util.goto_next_line()
        self.util.output_wrap("Enter new text for the oneliner:", 6, 0)
        self.util.ask(100, self.save_oneliner)

    def save_oneliner(self, new_text):
        """Save the edited oneliner."""
        if not new_text.strip():
            self.util.output_wrap("Oneliner text cannot be empty. Try again.", 6, 0)
            self.display_menu()
            return

        # Update the oneliner in the database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        oneliner_to_update = self.oneliners[self.current_oneliner_id]

        update_result = db['oneliners'].update_one(
            {'_id': oneliner_to_update['_id'], 'chosen_bbs': self.sid_data.chosen_bbs}, 
            {'$set': {'text': new_text}}
        )

        # Check if the update was successful
        if update_result.matched_count > 0:
            self.util.output_wrap("Oneliner updated successfully.", 6, 0)
            # Update local oneliner cache
            self.oneliners[self.current_oneliner_id]['text'] = new_text
        else:
            self.util.output_wrap("Error updating oneliner. Try again.", 6, 0)

        self.display_menu()

    def delete_oneliner(self, oneliner_id):
        """Start the process of deleting an oneliner."""
        self.current_oneliner_id = oneliner_id
        self.util.goto_next_line()
        oneliner_to_delete = self.oneliners[oneliner_id]['text']
        self.util.output_wrap(f"Are you sure you want to delete the following oneliner? '{oneliner_to_delete}' (Y/N)", 6, 0)
        self.util.ask(1, self.confirm_delete_oneliner)

    def confirm_delete_oneliner(self, confirmation):
        """Confirm and proceed with deletion of the oneliner."""
        if confirmation.lower() == 'y':
            mongo_client = self.util.mongo_client
            db = mongo_client['bbs']
            oneliner_to_delete = self.oneliners[self.current_oneliner_id]

            delete_result = db['oneliners'].delete_one({'_id': oneliner_to_delete['_id'], 'chosen_bbs': self.sid_data.chosen_bbs})

            if delete_result.deleted_count > 0:
                self.util.output_wrap("Oneliner deleted successfully.", 6, 0)
                # Remove the oneliner from the local cache
                del self.oneliners[self.current_oneliner_id]
            else:
                self.util.output_wrap("Error deleting oneliner. Try again.", 6, 0)
        else:
            self.util.output_wrap("Deletion cancelled.", 6, 0)

        self.display_menu()
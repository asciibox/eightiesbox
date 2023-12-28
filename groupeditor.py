from pymongo import MongoClient

class GroupEditor:
    def __init__(self, util, callback_on_exit):
        self.util = util
        self.mongo_client = util.mongo_client
        self.db = self.mongo_client['bbs']
        self.groups_collection = self.db['groups']
        self.callback_on_exit = callback_on_exit

    def display_menu(self):
        self.list_groups()
        self.util.output("Control", 6, 0)
        self.util.goto_next_line()
        self.util.output("-------", 6, 0)
        self.util.goto_next_line()

        self.util.output("C - Create a new group", 6, 0)
        self.util.goto_next_line()
        self.util.output("E - Edit group name", 6, 0)
        self.util.goto_next_line()
        self.util.output("D - Delete group", 6, 0)
        self.util.goto_next_line()

        self.util.output("X - Exit to Main Menu", 6, 0)
        self.util.goto_next_line()

        # self.util.output("H - Help", 6, 0)
        self.util.goto_next_line()
        self.util.goto_next_line()

        self.util.output("Select an option: ", 6, 0)
        self.util.ask(1, self.process_choice)

    def process_choice(self, choice):
        # Implement logic to handle the user's choice.
        if choice.lower() == 'e':
            self.edit_groups()
        elif choice.lower() == 'd':
            self.remove_group()
        elif choice.lower() == 'c':
            self.add_group()
        elif choice.lower() == 'x':
            self.callback_on_exit()
        else:
            self.util.output("Invalid choice. Please try again.", 6, 0)
            self.display_menu()


    def list_groups(self):
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        self.groups = list(self.groups_collection.find({'chosen_bbs' : self.util.sid_data.chosen_bbs}))
        for index, group in enumerate(self.groups):
            self.util.output_wrap(f"{index+1}: {group['name']}", 6, 0)
            self.util.goto_next_line()

    def add_group(self):
        self.util.goto_next_line()
        self.util.output_wrap('Enter new group name:', 6, 0)
        self.util.ask(35, self.add_group_callback)

    def add_group_callback(self, group_name):
        self.groups_collection.insert_one({"name": group_name, 'chosen_bbs' : self.util.sid_data.chosen_bbs})
        self.util.output_wrap("Group added.", 6, 0)
        self.display_menu()

    def edit_groups(self):
        self.list_groups()
        self.util.output_wrap('Enter index of group to edit:', 6,0)
        self.util.ask(3, self.edit_group_callback)

    def edit_group_callback(self, index):
        try:
            index = int(index)-1
            if index < 0 or index >= len(self.groups):
                self.util.output_wrap("Invalid index. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.util.output_wrap('Enter index of group to edit:', 6, 0)
                self.util.ask(3, self.edit_group_callback)
                return

            self.current_group = self.groups[index]
            self.util.goto_next_line()
            self.util.output_wrap('Enter the new name for the group:', 6, 0);
            self.util.ask(35, self.update_group_name)
        except ValueError:
            self.util.output_wrap("Please enter a valid index.", 6, 0)
            # return
            self.display_menu()


    def update_group_name(self, new_name):
        if not new_name:
            self.util.output_wrap("Group name cannot be empty.", 6, 0)
            self.util.goto_next_line()
            self.util.output_wrap('"Enter new name for the group:', 6, 0);
            self.util.ask(35, self.update_group_name)
            return

        self.groups_collection.update_one(
            {'_id': self.current_group['_id'], 'chosen_bbs': self.util.sid_data.chosen_bbs},
            {'$set': {'name': new_name}}
        )
        self.util.output_wrap("Group name updated.", 6, 0)
        self.util.goto_next_line()
        self.edit_groups()

    def remove_group(self):
            self.list_groups()
            self.util.output_wrap('Enter index of group to remove:', 6, 0)
            self.util.ask(3, self.remove_group_callback)

    def remove_group_callback(self, index):
        try:
            index = int(index)-1
            if index < 0 or index >= len(self.groups):
                self.util.output_wrap("Invalid index. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.util.output_wrap('Enter index of group to remove:', 6, 0)
                self.util.ask(3, self.remove_group_callback)
                return

            group_to_remove = self.groups[index]
            self.groups_collection.delete_one({'_id': group_to_remove['_id'], 'chosen_bbs': self.util.sid_data.chosen_bbs})
            self.util.output_wrap("Group removed.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
        except ValueError:
            self.util.output_wrap("Please enter a valid index.", 6, 0)
            self.display_menu()


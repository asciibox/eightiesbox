from areamenu import AreaMenu

class MessageAreaMenu(AreaMenu):
    def __init__(self, util, callback_on_exit):
        super().__init__(util, callback_on_exit, "Message")
         # Set the current action for the session
        util.sid_data.setCurrentAction("wait_for_message_area")
        mongo_client = util.mongo_client  # Assuming you have a mongo_client in util
        db = mongo_client['bbs']
        self.areas = list(db['messageareas'].find({ 'chosen_bbs' : util.sid_data.chosen_bbs}))
        self.areas.sort(key=lambda x: x.get('order', 0))
        self.start()
        
    def edit_origin(self, selected_area):
        """Edit the Origin line for the selected message area."""
        
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(10)
        self.util.output_wrap(f"Editing Origin for {selected_area['name']}:")
        self.util.ask(35, self.save_origin)
        
    def save_origin(self, new_origin):
        """Save the new Origin line."""
        
        # Your logic to save the new Origin goes here. For now, it will just
        # print a confirmation message and go back to the menu.
        
        self.util.output_wrap(f"Origin saved as: {new_origin}")
        self.display_menu()

    def create_new_message_area(self):
        """Prompt for the new name of the message area."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter the name of the new message area:", 6, 0)
        self.util.ask(35, self.ask_for_order)

    def ask_for_order(self, new_area_name):
        """Prompt for the order of the new message area."""
        self.new_area_name = new_area_name  # Store the name temporarily
        self.util.goto_next_line()
        self.util.output_wrap("Enter the order number for the new message area (1-9999):", 6, 0)
        self.util.ask(4, self.store_new_message_area)

    def store_new_message_area(self, order):
        """Store the new message area in MongoDB."""

        try:
            order = int(order)
            if not (1 <= order <= 9999):
                raise ValueError("Invalid range")

        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid order number. It must be a number between 1 and 9999.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        # Continue with storing the new message area...
        # (the rest of the code remains the same)

        # Insert new message area
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        db['messageareas'].insert_one({
            'name': self.new_area_name,
            'min_level': 0,
            'order': order,
            'chosen_bbs' : self.sid_data.chosen_bbs
        })

        # Update self.areas to include new area
        self.areas.append({'name': self.new_area_name, 'min_level': 0, 'order': order})

        # Sort self.areas based on the order
        self.areas = sorted(self.areas, key=lambda k: k['order'])
        
        self.util.goto_next_line()
        self.util.output_wrap(f"Message area '{self.new_area_name}' created successfully.", 6, 0)
        self.util.goto_next_line()
        self.display_menu()

    def change_order_message_area(self):
        """Change the order of a message area."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter the number of the message area you want to change:", 6, 0)
        self.util.ask(35, self.ask_new_order)

    def ask_new_order(self, idx):
        """Ask for the new order value for the selected message area."""
        try:
            idx = int(idx) - 1  # Convert input to zero-based index
            if idx < 0 or idx >= len(self.areas):
                self.util.goto_next_line()
                self.util.output_wrap("Invalid number. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.display_menu()
                return
        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid input. Please enter a number.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        self.util.goto_next_line()
        self.util.output_wrap("Enter the new order value:", 6, 0)
        self.util.ask(35, lambda new_order: self.save_new_order(idx, new_order))

    def save_new_order(self, idx, new_order):
        """Save the new order value in the database and update self.areas."""
        try:
            new_order = int(new_order)
        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid input. Order value must be an integer.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        # Update the database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        area_id = self.areas[idx]['_id']
        db['messageareas'].update_one({'_id': area_id}, {'$set': {'order': new_order}})

        # Update self.areas
        self.areas[idx]['order'] = new_order
        self.areas.sort(key=lambda x: x.get('order', 0))

        # Redraw the menu
        self.display_menu()

    def rename_message_area(self):
        """Start the process of renaming a message area."""
        self.util.goto_next_line()
        self.util.output_wrap("Enter the number of the message area you want to rename:", 6, 0)
        self.util.ask(35, self.ask_new_message_area_name)

    def ask_new_message_area_name(self, idx):
        """Ask for the new name for the selected message area."""
        try:
            idx = int(idx) - 1  # Convert input to zero-based index
            if idx < 0 or idx >= len(self.areas):
                self.util.goto_next_line()
                self.util.output_wrap("Invalid number. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.display_menu()
                return
        except ValueError:
            self.util.goto_next_line()
            self.util.output_wrap("Invalid input. Please enter a number.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        self.util.goto_next_line()
        self.util.output("Enter the new name for the message area:", 6, 0)
        self.util.ask(35, lambda new_name: self.save_new_message_area_name(idx, new_name))

    def save_new_message_area_name(self, idx, new_name):
        """Save the new name in the database and update self.areas."""
        # Update the database
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        area_id = self.areas[idx]['_id']
        db['messageareas'].update_one({'_id': area_id}, {'$set': {'name': new_name}})

        # Update self.areas
        self.areas[idx]['name'] = new_name

        # Redraw the menu
        self.display_menu()

    def set_new_min_level(self, choice_idx, new_level):
        try:
            new_level = int(new_level)
            area_id = self.areas[choice_idx]['_id']  # get the area id from the selected choice index
            
            # Update the database, code for saving new min_level
            mongo_client = self.util.mongo_client
            db = mongo_client['bbs']
            update_result = db['messageareas'].update_one({'_id': area_id}, {'$set': {'min_level': new_level}})
            
            if update_result.modified_count == 1:
                self.areas[choice_idx]['min_level'] = new_level  # update local data structure
                self.util.output_wrap(f"Successfully updated min_level to {new_level}", 6, 0)
            else:
                self.util.output_wrap("Failed to update min_level in the database.", 6, 0)
            
            self.display_menu()
            
        except ValueError:
            self.util.output_wrap("Invalid input for min_level. Please try again.", 6, 0)
            self.display_menu()

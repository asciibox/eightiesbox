from basicansi import BasicANSI

class MessageAreaMenu(BasicANSI):
    def __init__(self, util,  user_level, callback_on_exit):
        super().__init__(util)
        
        # Set the current action for the session
        util.sid_data.setCurrentAction("wait_for_message_area")
        
        # Store provided parameters
        # Connect to MongoDB and read areas
        mongo_client = util.mongo_client  # Assuming you have a mongo_client in util
        db = mongo_client['bbs']
        self.areas = list(db['messageareas'].find())
        self.areas.sort(key=lambda x: x.get('order', 0))
        
        self.user_level = self.sid_data.user_level
        self.user_name = self.sid_data.user_name
        print("SETTING")
        print(callback_on_exit)
        self.callback_on_exit = callback_on_exit
        
        # Initialize the area menu stack
        self.area_menu_stack = []
        
        # Display the menu for the first time
        self.display_menu()

    def display_menu(self):
        """Displays the message area menu."""
        
        self.util.clear_screen()
        # Set the output coordinates
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        
        # Clear the screen and output the menu header
        self.util.output("Message Areas", 6,0 )
        self.util.goto_next_line()
        
        # Loop through areas and display them
        for idx, area in enumerate(self.areas):
            order_display = area.get('order', 'N/A')  # If 'order' is not available, display 'N/A'
            self.util.output(f"{idx+1}. {area['name']} (Order: {order_display})", 6, 0)
            self.util.goto_next_line()
                
        self.util.goto_next_line()
        self.util.output("C. Create new message area", 6,0)
        self.util.goto_next_line()
        self.util.output("O. Change order of a message area", 6,0)
        self.util.goto_next_line()
        self.util.output("R. Rename message area", 6,0)
        self.util.goto_next_line()
        self.util.output("X. Exit to main menu", 6,0)
        self.util.goto_next_line()
        # Ask for user choice
        self.util.ask(1, self.process_choice)
    
    def process_choice(self, choice):
        """Processes the user's menu choice."""
        
        # Exit to main menu
        if choice.lower() == 'c':
            self.create_new_message_area()
            return
        elif choice.lower() == 'o':
            self.change_order_message_area()
            return
        elif choice.lower() == 'r':
            self.rename_message_area()
            return
        if choice.lower() == 'x':
            self.callback_on_exit()
            return
        
        # Validate choice and perform corresponding action
        try:
            choice_idx = int(choice) - 1
            selected_area = self.areas[choice_idx]
            
            if self.user_level >= selected_area['min_level']:
                self.edit_origin(selected_area)
            else:
                self.util.output("You don't have permission to access this area.", 6,0)
                self.display_menu()
                
        except (ValueError, IndexError):
            self.util.output("Invalid choice. Please try again.", 6,0 )
            self.display_menu()
            
    def edit_origin(self, selected_area):
        """Edit the Origin line for the selected message area."""
        
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(10)
        self.util.output(f"Editing Origin for {selected_area['name']}:")
        self.util.ask(40, self.save_origin)
        
    def save_origin(self, new_origin):
        """Save the new Origin line."""
        
        # Your logic to save the new Origin goes here. For now, it will just
        # print a confirmation message and go back to the menu.
        
        self.util.output(f"Origin saved as: {new_origin}")
        self.display_menu()

    def create_new_message_area(self):
        """Prompt for the new name of the message area."""
        self.util.goto_next_line()
        self.util.output("Enter the name of the new message area:", 6, 0)
        self.util.ask(40, self.ask_for_order)

    def ask_for_order(self, new_area_name):
        """Prompt for the order of the new message area."""
        self.new_area_name = new_area_name  # Store the name temporarily
        self.util.goto_next_line()
        self.util.output("Enter the order number for the new message area (1-9999):", 6, 0)
        self.util.ask(4, self.store_new_message_area)

    def store_new_message_area(self, order):
        """Store the new message area in MongoDB."""

        try:
            order = int(order)
            if not (1 <= order <= 9999):
                raise ValueError("Invalid range")

        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid order number. It must be a number between 1 and 9999.", 6, 0)
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
            'min_level': 1,
            'order': order
        })

        # Update self.areas to include new area
        self.areas.append({'name': self.new_area_name, 'min_level': 1, 'order': order})

        # Sort self.areas based on the order
        self.areas = sorted(self.areas, key=lambda k: k['order'])
        
        self.util.goto_next_line()
        self.util.output(f"Message area '{self.new_area_name}' created successfully.", 6, 0)
        self.util.goto_next_line()
        self.display_menu()

    def change_order_message_area(self):
        """Change the order of a message area."""
        self.util.goto_next_line()
        self.util.output("Enter the number of the message area you want to change:", 6, 0)
        self.util.ask(40, self.ask_new_order)

    def ask_new_order(self, idx):
        """Ask for the new order value for the selected message area."""
        try:
            idx = int(idx) - 1  # Convert input to zero-based index
            if idx < 0 or idx >= len(self.areas):
                self.util.goto_next_line()
                self.util.output("Invalid number. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.display_menu()
                return
        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid input. Please enter a number.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        self.util.goto_next_line()
        self.util.output("Enter the new order value:", 6, 0)
        self.util.ask(40, lambda new_order: self.save_new_order(idx, new_order))

    def save_new_order(self, idx, new_order):
        """Save the new order value in the database and update self.areas."""
        try:
            new_order = int(new_order)
        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid input. Order value must be an integer.", 6, 0)
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
        self.util.output("Enter the number of the message area you want to rename:", 6, 0)
        self.util.ask(40, self.ask_new_message_area_name)

    def ask_new_message_area_name(self, idx):
        """Ask for the new name for the selected message area."""
        try:
            idx = int(idx) - 1  # Convert input to zero-based index
            if idx < 0 or idx >= len(self.areas):
                self.util.goto_next_line()
                self.util.output("Invalid number. Please try again.", 6, 0)
                self.util.goto_next_line()
                self.display_menu()
                return
        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid input. Please enter a number.", 6, 0)
            self.util.goto_next_line()
            self.display_menu()
            return

        self.util.goto_next_line()
        self.util.output("Enter the new name for the message area:", 6, 0)
        self.util.ask(40, lambda new_name: self.save_new_message_area_name(idx, new_name))

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
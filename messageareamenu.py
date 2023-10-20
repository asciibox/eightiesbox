from basicansi import BasicANSI

class MessageAreaMenu(BasicANSI):
    def __init__(self, util, areas, user_level, callback_on_exit):
        super().__init__(util)
        
        # Set the current action for the session
        util.sid_data.setCurrentAction("wait_for_message_area")
        
        # Store provided parameters
        self.areas = areas
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
            if self.user_level >= area['min_level']:
                self.util.output(f"{idx+1}. {area['name']}")
                
        self.util.goto_next_line()
        self.util.output("X. Exit to main menu", 6,0)
        
        # Ask for user choice
        self.util.ask(1, self.process_choice)
    
    def process_choice(self, choice):
        """Processes the user's menu choice."""
        
        # Exit to main menu
        if choice.lower() == 'x':
            print("CALLBACK")
            print(self.callback_on_exit)
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

# Example usage:
areas = [
    {'name': 'General', 'min_level': 1},
    {'name': 'Tech Talk', 'min_level': 2},
    {'name': 'Off Topic', 'min_level': 1}
]

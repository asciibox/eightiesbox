from basicansi import BasicANSI

class AreaMenu(BasicANSI):
    def __init__(self, util, callback_on_exit, headline_type):
        super().__init__(util)
        
        self.headline_type = headline_type
        # Store provided parameters
        # Connect to MongoDB and read areas
        
        
        self.user_level = self.sid_data.user_level
        self.user_name = self.sid_data.user_name
        self.callback_on_exit = callback_on_exit
        
        # Initialize the area menu stack
        self.area_menu_stack = []
        
    def start(self): 
        # Display the menu for the first time
        self.display_menu()

    def display_menu(self):
        """Displays the message area menu."""
        
        self.util.clear_screen()
        # Set the output coordinates
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        
        # Clear the screen and output the menu header
        self.util.output(self.headline_type+" areas", 6,0 )
        self.util.goto_next_line()
        
        # Loop through areas and display them
        for idx, area in enumerate(self.areas):
            order_display = area.get('order', 'N/A')  # If 'order' is not available, display 'N/A'
            self.util.output(f"{idx+1}. {area['name']} (Order: {order_display})", 6, 0)
            self.util.goto_next_line()
                
        self.util.goto_next_line()
        if self.headline_type=="Message":
            self.util.output("C. Create new message area", 6,0)
            self.util.goto_next_line()
            self.util.output("O. Change order of a message area", 6,0)
            self.util.goto_next_line()
            self.util.output("R. Rename message area", 6,0)
        else:
            self.util.output("C. Create new file area", 6,0)
            self.util.goto_next_line()
            self.util.output("O. Change order of a file area", 6,0)
            self.util.goto_next_line()
            self.util.output("R. Rename file area", 6,0)
        self.util.goto_next_line()
        self.util.output("X. Exit to main menu", 6,0)
            
        self.util.goto_next_line()
        # Ask for user choice
        self.util.ask(1, self.process_choice)
    
    def process_choice(self, choice):
        """Processes the user's menu choice."""
        
        # Exit to main menu
        if self.headline_type=="Message":
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
        else:
            if choice.lower() == 'c':
                self.create_new_file_area()
                return
            elif choice.lower() == 'o':
                self.change_order_file_area()
                return
            elif choice.lower() == 'r':
                self.rename_file_area()
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
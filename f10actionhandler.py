class F10ActionHandler:
    def __init__(self, util):
        self.util = util
        self.current_user_index = 0  # To keep track of the current selected user
        self.previous_action = None


    def get_requesting_users(self):
        print(self.util.sid_data.incoming_requests)
        return [req['from'] for req in self.util.sid_data.incoming_requests if req['status'] == 'received']
        
    def handle_F10(self):

        requesting_users = self.get_requesting_users()
        if self.util.sid_data.current_action == 'in_chat':
            self.util.statusinfo("You are currently chatting with "+self.util.sid_data.current_chat_partner+" and cannot accept new requests. Press ESC to leave conversation.")
            return
            
        if not requesting_users:
           
            self.util.statusinfo("No pending requests")
            return

        self.util.status_bar_paused = True
        # Change the current action to wait_for_f10_action
        self.previous_action = self.util.sid_data.current_action
        
        
        # Show the first requesting user in the status bar
        self.show_status_bar_request(requesting_users)
    
    def show_status_bar_request(self, requesting_users):

        self.util.sid_data.previous_action = self.util.sid_data.current_action
        self.util.sid_data.setCurrentAction("wait_for_f10_action")
        # Show the current user in the status bar using yHeight for last line
        self.util.sid_data.current_chat_partner = requesting_users[self.current_user_index % len(requesting_users)]
        
        self.util.statusinfo(f"Press ENTER to accept request from: {self.util.sid_data.current_chat_partner} - ESC to leave F10 menu")

  
        

    def handle_key(self, key):
        requesting_users = self.get_requesting_users()
        if key == 'ArrowLeft':
            if self.current_user_index > 0:
                self.current_user_index -= 1
                self.show_status_bar_request(requesting_users)
        elif key == 'ArrowRight':
            if self.current_user_index < len(requesting_users):
                self.current_user_index += 1
                self.show_status_bar_request(requesting_users)
        elif key == 'Enter':
            self.util.status_bar_paused = False
            self.accept_current_request()
        elif key == 'Escape':
            self.util.status_bar_paused = False
            self.exit_F10_mode()
    
    def accept_current_request(self):
        requesting_users = self.get_requesting_users()
        to_remove = None  # Initialize the variable to store the dictionary to be removed
        self.util.sid_data.copy_action = False
        if requesting_users:
            selected_user = requesting_users[self.current_user_index % len(requesting_users)]
            
            for request in self.util.sid_data.incoming_requests:
                if request['from'] == selected_user:
                    request['status'] = 'ACCEPTED'
                    self.util.sid_data.chat_partner = request['sid_data']  # Set the chat_partner
                    self.util.clear_screen()
                    self.util.sid_data.setStartX(0)
                    self.util.sid_data.setStartY(0)
                    self.util.statusinfo(f"You are chatting with {selected_user}")
                    
                    to_remove = request  # Assign the request to be removed

                    # Now update the outgoing request for the other user
                    for other_sid, other_sid_data in self.util.all_sid_data.items():
                        if other_sid_data.user_document and other_sid_data.user_document["username"] == selected_user:
                            for out_req in other_sid_data.outgoing_requests:
                                if out_req['to'] == self.util.sid_data.user_document["username"]:
                                    out_req['status'] = 'ACCEPTED'
                                    break

                    # Set current state to in_chat
                    self.util.sid_data.setCurrentAction("in_chat")
                    
                    break

        # Remove the accepted request
        if to_remove:
            self.util.sid_data.incoming_requests.remove(to_remove)

                
    
    def exit_F10_mode(self):
        self.util.update_status_bar()
        self.util.sid_data.setCurrentAction(self.previous_action)  # Or set it to whatever default state you have

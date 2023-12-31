from pymongo import MongoClient
from userpickeronline import UserPickerOnline
import asyncio



class MultilineChat:
    def __init__(self, util):
        self.util = util
        self.stop_waiting = False
    
    def ask_username(self):
        if self.count_online_users()>1:
            self.util.output("User you want to chat with: ", 6, 0)
            self.util.ask(35, self.to_input_callback)
        else:
            self.util.output("No users online, please wait", 1, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
    
    def is_user_online(self, username_to_check):
        for sid, sid_data in self.util.all_sid_data.items():
            user_doc = sid_data.user_document
            if user_doc and user_doc['username'] == username_to_check:
                return True
        return False

    def to_input_callback(self, response):
        db = self.util.mongo_client['bbs']
        users_collection = db['users']

        existing_user = users_collection.find_one({"username": response, 'chosen_bbs' : self.util.sid_data.chosen_bbs})
        
        if existing_user is None:
            # If the user does not exist, redirect to UserPicker class
            self.goto_user_picker(response)
        else:
            self.request_chat(response)

    def count_online_users(self):
        online_count = 0
        for sid, sid_data in self.util.all_sid_data.items():
            if sid_data.user_document:  # Checks if the user is logged in
                online_count += 1
        return online_count

    def request_chat(self, username):
        if username == self.util.sid_data.user_name:
            self.util.goto_next_line()
            self.util.output("You cannot chat with yourself", 6, 1)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return

        if not self.is_user_online(username):
            self.util.goto_next_line()
            self.util.output(username+" is not online", 6, 1)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return

        print("If not any")
        if not any(request['to'] == username for request in self.util.sid_data.outgoing_requests):
            # Append the new request if the username is not found
            self.util.sid_data.outgoing_requests.append({
                "to": username,
                "status": "sent"
            })
            print ("Request sent to " + username)
        else:
            # Username already exists in the outgoing requests
            print ("Request to " + username + " already exists.")

        if username not in self.util.sid_data.contacted_users:
            self.util.sid_data.contacted_users.append(username)

        # Find the sid_data for the user being requested and record the chat request
        for sid, sid_data in self.util.all_sid_data.items():
            if sid_data.user_document and sid_data.user_document["username"] == username:
                # Append to incoming_requests only if the username isn't already in the list
                if not any(request['from'] == self.util.sid_data.user_document["username"] for request in sid_data.incoming_requests):
                    sid_data.incoming_requests.append({
                        "from": self.util.sid_data.user_document["username"],
                        "status": "received",
                        "sid_data": self.util.sid_data  # Store the sid_data of the requester here
                    })

                # Store the sid_data of the receiver in the last outgoing request
                # Assuming the last request is the current one
                self.util.sid_data.outgoing_requests[-1]["sid_data"] = sid_data  

                # Append to contacted_users only if the username isn't already in the list
                if self.util.sid_data.user_document["username"] not in sid_data.contacted_users:
                    sid_data.contacted_users.append(self.util.sid_data.user_document["username"])

        self.show_contacted_users()



    def show_contacted_users(self):
        self.util.goto_next_line()
        self.util.output("Users you have contacted:", 6, 0)
        self.util.goto_next_line()
        for username in self.util.sid_data.contacted_users:
            self.util.output(username, 6, 0)
            self.util.goto_next_line()
        asyncio.run(self.wait_for_accepted_request())


    async def wait_for_accepted_request(self, timeout=60):
        self.util.sid_data.previous_action = self.util.sid_data.current_action
        self.util.sid_data.setCurrentAction("wait_for_multi_line_chat")
        
        start_time = asyncio.get_event_loop().time()
        time_passed = 1
        while True:
            # Check for time elapsed
            elapsed_time = asyncio.get_event_loop().time() - start_time
            if elapsed_time > timeout:
                print("Timeout reached")
                self.remove_user_from_requests(self.util.sid_data.user_name)
                self.exit()
                return
                break
            if self.stop_waiting:
                print("Waiting stopped.")
                self.remove_user_from_requests(self.util.sid_data.user_name)
                self.exit()
                return
                break

            # Check for accepted requests
            for request in self.util.sid_data.outgoing_requests:
                if request['status'] == 'ACCEPTED':
                    self.util.sid_data.current_chat_partner = request['to']
                    self.accept_request(request['to'])
                    self.util.sid_data.setChatCallback(self.exit)
                    return
            self.util.sid_data.startX = 0
            self.util.sid_data.cursorX = 0
            self.util.output("Waiting for acceptance ("+str(time_passed)+"/60)", 6, 0)
            time_passed += 1
            # Sleep for a small duration, asynchronously
            await asyncio.sleep(1)  # Sleep for 5 seconds

    def stop_waiting_for_request(self):
        self.stop_waiting = True

    def accept_request(self, from_username):
        to_remove = None
        for request in self.util.sid_data.outgoing_requests:
            if request['to'] == from_username:
                request['status'] = "ACCEPTED"
                self.util.sid_data.chat_partner = request['sid_data']  # Set the chat_partner
                to_remove = request
                break

        if to_remove:
            self.util.sid_data.outgoing_requests.remove(to_remove)

            # Notify the user and start chat
            self.util.sid_data.copy_action = False
            self.util.goto_next_line()
            self.util.output(f"Request from {from_username} has been ACCEPTED.", 6, 0)
            self.util.clear_screen()
            self.util.sid_data.setStartX(0)
            self.util.sid_data.setStartY(0)
            self.util.statusinfo(f"You are chatting with {from_username}")
            self.util.sid_data.setCurrentAction("in_chat")
        else:
            print("Error: Request not found")

            

    def goto_user_picker(self, username):
            # You could initialize a UserPicker instance here, or however you've planned to navigate to UserPicker
            # Assume UserPicker is another class handling user picking functionalities
            self.util.sid_data.user_picker = UserPickerOnline(self.util, username, self.user_picker_callback)
            self.util.sid_data.user_picker.show_options()

    def user_picker_callback(self, username):
        self.request_chat(username)

    def exit(self):
        self.util.sid_data.menu.return_from_gosub()
        self.util.sid_data.setCurrentAction("wait_for_menu")

    def remove_user_from_requests(self, username):
        # Remove from outgoing_requests
        self.util.sid_data.outgoing_requests = [request for request in self.util.sid_data.outgoing_requests if request['to'] != username]

        # Remove from contacted_users
        if username in self.util.sid_data.contacted_users:
            self.util.sid_data.contacted_users.remove(username)

        # Iterate over all_sid_data to remove from incoming_requests and contacted_users of other users
        for sid, sid_data in self.util.all_sid_data.items():
            # Remove from incoming_requests
            if sid_data.user_document:
                sid_data.incoming_requests = [request for request in sid_data.incoming_requests if request['from'] != username]

                # Remove from contacted_users
                if username in sid_data.contacted_users:
                    sid_data.contacted_users.remove(username)

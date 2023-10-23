from pymongo import MongoClient
from userpicker import UserPicker
import asyncio



class MultilineChat:
    def __init__(self, util):
        self.util = util
        self.stop_waiting = False
    
    def ask_username(self):
        self.util.output("User you want to chat with: ", 6, 0)
        self.util.ask(40, self.to_input_callback)
        
    def to_input_callback(self, response):
        db = self.util.mongo_client['bbs']
        users_collection = db['users']

        existing_user = users_collection.find_one({"username": response})
        
        if existing_user is None:
            # If the user does not exist, redirect to UserPicker class
            self.goto_user_picker(response)
        else:
            self.request_chat(response)

    def request_chat(self, username):
        # Record the chat request in the requester's sid_data
        self.util.sid_data.outgoing_requests.append({
            "to": username,
            "status": "sent"
        })

        if username not in self.util.sid_data.contacted_users:
            self.util.sid_data.contacted_users.append(username)

        # Find the sid_data for the user being requested and record the chat request
        for sid, sid_data in self.util.all_sid_data.items():
            if sid_data.user_document and sid_data.user_document["username"] == username:
                sid_data.incoming_requests.append({
                    "from": self.util.sid_data.user_document["username"],
                    "status": "received",
                    "sid_data": self.util.sid_data  # Store the sid_data of the requester here
                })
                self.util.sid_data.outgoing_requests[-1]["sid_data"] = sid_data  # Store the sid_data of the receiver here

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
                self.exit()
                return
                break
            if self.stop_waiting:
                print("Waiting stopped.")
                self.exit()
                return
                break

            # Check for accepted requests
            print(self.util.sid_data.incoming_requests)
            for request in self.util.sid_data.outgoing_requests:
                print(request)
                if request['status'] == 'ACCEPTED':
                    
                    self.accept_request(request['to'])
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
        self.util.output(f"Request from {from_username} has been ACCEPTED.", 6, 0)
        self.util.sid_data.setCurrentAction("in_chat")


    def goto_user_picker(self, username):
            # You could initialize a UserPicker instance here, or however you've planned to navigate to UserPicker
            # Assume UserPicker is another class handling user picking functionalities
            self.util.sid_data.user_picker = UserPicker(self.util, username, self.user_picker_callback)
            self.util.sid_data.user_picker.show_options()

    def user_picker_callback(self, username):
        self.request_chat(username)

    def exit(self):
        self.util.sid_data.menu.return_from_gosub()
        self.util.sid_data.setCurrentAction("wait_for_menu")

from utils import *
from actions import *
from sessiondata import *
from oneliners import *

class UserRegistration:
    def __init__(self, goto_next_line, ask, askPassword, askYesNo, output, usernameCallback, mongo_client, sid_data, wait, launchMenuCallback):
        self.goto_next_line = goto_next_line
        self.ask = ask
        self.askYesNo = askYesNo
        self.output = output
        self.usernameCallback = usernameCallback
        self.mongo_client = mongo_client
        self.sid_data = sid_data
        self.wait = wait
        self.launchMenuCallback = launchMenuCallback
        self.askPassword = askPassword

        self.userdata = {
            "username": "",
            "email": "",
            "age": 0,
            "sex" : "",
            "hobbies" : "",
            "password" : "",
        }


        goto_next_line()
        self.askYesNo("Are you a new user?", self.new_user_callback)

    def ask(self, length, callback):
        user_input = input()
        callback(user_input)

    def new_user_callback(self, result):
        if result == 'Y' or result == 'y':
            self.goto_next_line()
            self.output("Please enter your new username: ", 6, 0)
            self.ask(40, self.username_callback)
        else:
            self.goto_next_line()
            self.output("Please enter your name: ", 6, 0)
            self.ask(40, self.usernameCallback)

    def username_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please enter your new username: ", 6, 0)
            self.ask(40, self.username_callback)
            return
        self.userdata['username'] = input
        db = self.mongo_client['bbs']
        users_collection = db['users']

        existing_user = users_collection.find_one({"username": input})
        # If username does not exist, insert the new user data
        if existing_user is None:
           self.goto_next_line()
           self.output("Please enter your new password: ", 6, 0)
           self.askPassword(40, self.password_callback)
        else:
            self.goto_next_line()
            self.output("This username is already taken", 1, 0)
            self.goto_next_line()
            self.output("Please enter your new username: ", 6, 0)
            self.ask(40, self.username_callback)
        
    def password_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please enter your new password: ", 6, 0)
            self.askPassword(40, self.password_callback)
            return
        self.userdata['password'] = input
        self.goto_next_line()
        self.output("Please repeat your new paswword: ", 6, 0)
        self.askPassword(40, self.password_repetition_callback)

    def password_repetition_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please repeat your new password: ", 6, 0)
            self.ask(40, self.password_repetition_callback)
            return
        if input != self.userdata['password']:
            self.goto_next_line()
            self.output("Wrong password repetition", 1, 0)
            self.goto_next_line()
            self.output("Please enter your new password: ", 6, 0)
            self.askPassword(40, self.password_callback) # Certainly not self.password_repetition_callback
            return

        self.sid_data.setInputType("text")
        self.goto_next_line()
        self.output("Please enter your email address: ", 6, 0)
        self.ask(40, self.email_callback)

    def email_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please enter your email address: ", 6, 0)
            self.ask(40, self.email_callback)
            return
        db = self.mongo_client['bbs']
        users_collection = db['users']

        existing_email = users_collection.find_one({"email": input})
        # If username does not exist, insert the new user data
        if existing_email is None:
            self.userdata['email'] = input
            self.goto_next_line()
            self.output("Please enter your age: ", 6, 0)
            self.ask(2, self.age_callback)
        else:
            self.goto_next_line()
            self.output("This email address is already taken", 1, 0)
            self.goto_next_line()
            self.output("Please enter your email address: ", 6, 0)
            self.ask(40, self.email_callback) 

    def age_callback(self, input):
        if input == '' or not input.isnumeric():
            if not input.isnumeric():
                self.goto_next_line()
                self.output("Please enter a number", 1, 0);
            self.goto_next_line()
            self.output("Please enter your age: ", 6, 0)
            self.ask(2, self.age_callback)
            return
        self.userdata['age'] = input
        self.goto_next_line()
        self.output("Please enter your sex (M/F/O): ", 6, 0)
        self.ask(1, self.sex_callback, [ "m", "o", "f" ])

    def sex_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please enter your sex (M/F/O): ", 6, 0)
            self.ask(1, self.sex_callback, [ "m", "o", "f" ])
            return
        self.userdata['sex'] = input
        self.goto_next_line()
        self.output("What are your interests or hobbies? ", 6, 0)
        self.ask(55, self.hobbies_callback)

    def hobbies_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("What are your interests or hobbies? ", 6, 0)
            self.ask(55, self.hobbies_callback)
            return
        self.userdata['hobbies'] = input
        self.goto_next_line()
        self.askYesNo("Do you want to create account with our board?", self.creation_callback)

    def creation_callback(self, result):
        if result == 'n' or result =='N':
            self.usernameCallback("")
            return
        else:
            self.goto_next_line()
            db = self.mongo_client['bbs']
            users_collection = db['users']

            existing_user = users_collection.find_one({"username": self.userdata["username"]})
            # If username does not exist, insert the new user data
            if existing_user is None:
                users_collection.insert_one(self.userdata)
                self.goto_next_line()
                self.output("User created successfully.", 6, 0)
                bbs = OnelinerBBS(self.mongo_client, self.sid_data, self.goto_next_line, self.output, self.askYesNo, self.ask, self.wait, self.launchMenuCallback)
                bbs.show_oneliners()
            else:
                self.goto_next_line()
                self.output("Another user has just take this username. Please choose another.", 6, 0)
                self.goto_next_line()
                self.output("Please enter your new username: ", 6, 0)
                self.ask(40, username_exists_callback)

        pass

    def username_exists_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output("Please enter your new username: ", 6, 0)
            self.ask(40, self.username_callback)
            return
        self.userdata['username'] = input
        self.creation_callback('y')
        


    

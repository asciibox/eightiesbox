from email_validator import validate_email, EmailNotValidError
from utils import *
from sessiondata import *
from oneliners import *
import bcrypt

class UserRegistration:
    def __init__(self, util, launchMenuCallback):
        self.password_input = ""
        self.util = util
        self.goto_next_line = util.goto_next_line
        self.ask = util.ask
        self.askYesNo = util.askYesNo
        self.output = util.output
        self.output_wrap = util.output_wrap
        self.usernameCallback = util.usernameCallback
        self.mongo_client = util.mongo_client
        self.sid_data = util.sid_data
        self.wait = util.wait
        self.launchMenuCallback = launchMenuCallback
        self.askPassword = util.askPassword

        self.userdata = {
            "username": "",
            "email": "",
            "age": 0,
            "sex" : "",
            "hobbies" : "",
            "password" : "",
        }

        self.askYesNo("Are you a new user?", self.new_user_callback)

    def ask(self, length, callback):
        user_input = input()
        callback(user_input)

    def new_user_callback(self, result):
        if result == 'Y' or result == 'y':
            self.goto_next_line()
            self.output_wrap("Please enter your new username: ", 6, 0)
            self.ask(35, self.username_callback)
        else:
            self.goto_next_line()
            self.output_wrap("Please enter your name: ", 6, 0)
            self.ask(35, self.usernameCallback)

    def username_callback(self, input):
        input = input.lower().strip()
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your new username: ", 6, 0)
            self.ask(35, self.username_callback)
            return
        self.userdata['username'] = input
        db = self.mongo_client['bbs']
        users_collection = db['users']

        existing_user = users_collection.find_one({"username": input, 'chosen_bbs': self.sid_data.chosen_bbs})
        # If username does not exist, insert the new user data
        if existing_user is None:
           self.goto_next_line()
           self.output_wrap("Please enter your new password: ", 6, 0)
           self.askPassword(35, self.password_callback)
        else:
            self.goto_next_line()
            self.output_wrap("This username is already taken", 1, 0)
            self.goto_next_line()
            self.output_wrap("Please enter your new username: ", 6, 0)
            self.ask(35, self.username_callback)
        
    def password_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your new password: ", 6, 0)
            self.askPassword(35, self.password_callback)
            return
        self.password_input = input
        hashed_password = bcrypt.hashpw(input.encode('utf-8'), bcrypt.gensalt())
        self.userdata['password'] = hashed_password.decode('utf-8')
        self.goto_next_line()
        self.output_wrap("Please repeat your new pasword: ", 6, 0)
        self.askPassword(35, self.password_repetition_callback)

    def password_repetition_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please repeat your new password: ", 6, 0)
            self.askPassword(35, self.password_repetition_callback)
            return
        if input != self.password_input:
            self.goto_next_line()
            self.output_wrap("Wrong password repetition", 1, 0)
            self.goto_next_line()
            self.output_wrap("Please enter your new password: ", 6, 0)
            self.askPassword(35, self.password_callback) # Certainly not self.password_repetition_callback
            return

        self.sid_data.setInputType("text")
        self.goto_next_line()
        self.output_wrap("Please enter your email address: ", 6, 0)
        self.ask(35, self.email_callback)

    def email_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your email address: ", 6, 0)
            self.ask(35, self.email_callback)
            return
        
        try:
            # Validate the email and get the normalized email
            valid_email = validate_email(input, check_deliverability=False).email
        except EmailNotValidError as e:
            # If the email is invalid, show the error message and ask again
            self.goto_next_line()
            self.output_wrap(str(e), 6, 0)
            self.goto_next_line()
            self.output_wrap("Please enter your email address: ", 6, 0)
            self.ask(35, self.email_callback)
            return
        
        db = self.mongo_client['bbs']
        users_collection = db['users']

        existing_email = users_collection.find_one({"email": input, "chosen_bbs" : self.sid_data.chosen_bbs})
        # If username does not exist, insert the new user data
        if existing_email is None:
            self.userdata['email'] = input
            self.goto_next_line()
            self.output_wrap("Please enter your age: ", 6, 0)
            self.ask(2, self.age_callback)
        else:
            self.goto_next_line()
            self.output_wrap("This email address is already taken", 1, 0)
            self.goto_next_line()
            self.output_wrap("Please enter your email address: ", 6, 0)
            self.ask(35, self.email_callback) 

    def age_callback(self, input):
        if input == '' or not input.isnumeric():
            if not input.isnumeric():
                self.goto_next_line()
                self.output_wrap("Please enter a number", 1, 0);
            self.goto_next_line()
            self.output_wrap("Please enter your age: ", 6, 0)
            self.ask(2, self.age_callback)
            return
        self.userdata['age'] = input
        self.goto_next_line()
        self.output_wrap("Please enter your sex (M/F/O): ", 6, 0)
        self.ask(1, self.sex_callback, [ "m", "o", "f" ])

    def sex_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your sex (M/F/O): ", 6, 0)
            self.ask(1, self.sex_callback, [ "m", "o", "f" ])
            return
        self.userdata['sex'] = input
        self.goto_next_line()
        self.output_wrap("What are your interests or hobbies? ", 6, 0)
        self.ask(55, self.hobbies_callback)

    def hobbies_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("What are your interests or hobbies? ", 6, 0)
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
            self.userdata['user_level'] = 0
            self.userdata['chosen_bbs'] = self.sid_data.chosen_bbs

            existing_user = users_collection.find_one({"username": self.userdata["username"], "chosen_bbs" : self.sid_data.chosen_bbs})
            # If username does not exist, insert the new user data
            if existing_user is None:
                insert_result = users_collection.insert_one(self.userdata)
                new_user_id = insert_result.inserted_id

                # Update self.userdata to include the new _id
                self.userdata.update({"_id": new_user_id})

                # Update self.sid_data.user_document to include the new _id
                self.sid_data.user_document = {**self.userdata, "_id": new_user_id}
                
                self.util.create_defaults(new_user_id, db)

                self.goto_next_line()
                self.output("User created successfully.", 6, 0)
                bbs = OnelinerBBS(self.util)
                bbs.show_oneliners()
            else:
                self.goto_next_line()
                self.output_wrap("Another user has just take this username. Please choose another.", 6, 0)
                self.goto_next_line()
                self.output_wrap("Please enter your new username: ", 6, 0)
                self.ask(35, self.username_exists_callback)

        pass

    def username_exists_callback(self, input):
        if input == '':
            self.goto_next_line()
            self.output_wrap("Please enter your new username: ", 6, 0)
            self.ask(35, self.username_callback)
            return
        self.userdata['username'] = input
        self.creation_callback('y')
        


    

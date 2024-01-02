from pycode.renderer import Renderer 

class ProfileRenderer(Renderer):
    def __init__(self, util, return_function):
        super().__init__(util, return_function)  # Call the constructor of the parent class
        
    def submit_function(self):
        # Retrieve user input values
        mypassword = self.input_values.get("password", "")
        user_data = {
            "username": self.input_values.get("username", ""),
            "email": self.input_values.get("email", ""),
            "sex": self.input_values.get("sex", ""),
            "social_media_1": self.input_values.get("social_media_1", ""),
            "social_media_2": self.input_values.get("social_media_2", ""),
            "website": self.input_values.get("website", ""),
            "hobbies": self.input_values.get("interests", ""),  # Mapping 'interests' to 'hobbies'
        }

        # Only hash and set new password if mypassword is not empty
        if mypassword:
            hashed_password = bcrypt.hashpw(mypassword.encode('utf-8'), bcrypt.gensalt())
            new_password = hashed_password.decode('utf-8')
            user_data["password"] = new_password

        # Connect to MongoDB
        db = self.util.mongo_client['bbs']
        users_collection = db['users']

        # User ID to update
        user_id = self.util.sid_data.user_document['_id']

        # Update the user document
        users_collection.update_one({"_id": user_id}, {"$set": user_data})

        self.return_function()
        pass
    
    

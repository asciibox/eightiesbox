from pycode.renderer import Renderer
import bcrypt

class ProfileRenderer(Renderer):
    def __init__(self, util, return_function, filename=None, db_filename=None):
        super().__init__(util, return_function, filename, db_filename)  # Call the constructor of the parent class
        
    def submit_function(self):
        # Retrieve user input values
        mypassword = self.input_values.get("password", "")
        user_data = {
            "display_username": self.input_values.get("display_username", ""),
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

        # Retrieve the updated user document
        updated_user_document = users_collection.find_one({"_id": user_id})

        # Assign the updated document to sid_data.user_document
        if updated_user_document:
            self.util.sid_data.user_document = updated_user_document
        else:
            # Handle case where user document is not found
            print("User document not found.")

        self.return_function()
        pass
    
    

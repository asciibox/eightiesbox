from pymongo import MongoClient
class UpdateUsers:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client

    def add_display_usernames(self):
        # Access the database and collection
        db = self.mongo_client['bbs']
        users_collection = db['users']

        # Update 'display_username' field to be equal to 'username' for all users
        updated_count = users_collection.update_many(
            {},
            [{"$set": {"display_username": "$username"}}]
        ).modified_count

        return updated_count

# Usage example
if __name__ == "__main__":
    mongo_client = MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
    updater = UpdateUsers(mongo_client)
    updated_count = updater.add_display_usernames()
    print(f"Updated {updated_count} users.")

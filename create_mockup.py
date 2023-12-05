from pymongo import MongoClient
import random
import string

mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['bbs']
users_collection = db['users']

def clear_collections():
    global db

    # Collections to clear
    collections_to_clear = [
        'users'
    ]
    for collection_name in collections_to_clear:
        collection = db[collection_name]
        collection.delete_many({})  # Deletes all documents in the collection
        print(f"Cleared collection: {collection_name}")

def create_random_users():
    global db, users_collection
    warning_message = (
        "Warning: This application will populate the 'bbs' database with random user data."
        "\nDo you wish to proceed? (yes/no): "
    )
    user_response = input(warning_message)
    
    if user_response.lower() not in ["yes", "y"]:
        print("Operation cancelled by the user.")
        return

    clear_collections()

    names = ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve']
    sexes = ['M', 'F']
    hobbies = ['reading', 'cycling', 'gaming', 'fishing', 'painting']
    
    for _ in range(100):
        name = random.choice(names) + str(random.randint(1, 100))
        email = name.lower() + "@example.com"
        age = random.randint(18, 60)
        sex = random.choice(sexes)
        hobby = random.choice(hobbies)
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        userdata = {
            "username": name,
            "email": email,
            "age": age,
            "sex": sex,
            "hobbies": hobby,
            "password": password,
            "user_level" : 0
        }

        existing_user = users_collection.find_one({"username": userdata["username"]})
        if existing_user is None:
            insert_result = users_collection.insert_one(userdata)
            new_user_id = insert_result.inserted_id

            # Update userdata to include the new _id
            userdata.update({"_id": new_user_id})

            # Here, you could also update self.sid_data.user_document if necessary
            # self.sid_data.user_document = {**userdata, "_id": new_user_id}

    print("Random users have been successfully created.")

    mailboxes_collection = db['mailboxes']
    for id in range(1, 101):
        mailboxes_collection.insert_one({"name": f"EightiesBox Box Nr. {id}"})


# Call the function to create random users

create_random_users()

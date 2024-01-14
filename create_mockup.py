from pymongo import MongoClient
import random
import string
import bcrypt
from datetime import datetime, timedelta


mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client['bbs']
users_collection = db['users']

def clear_collections():
    global db

    # Collections to clear
    collections_to_clear = [
        'users', 'timeline_entries', 'mailboxes'
    ]
    for collection_name in collections_to_clear:
        collection = db[collection_name]
        collection.delete_many({})  # Deletes all documents in the collection
        print(f"Cleared collection: {collection_name}")

def create_random_users(hq_id):
    global db, users_collection
   

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
            "user_level" : 0,
            "chosen_bbs" : hq_id
        }

        existing_user = users_collection.find_one({"username": userdata["username"], "chosen_bbs" : 1})
        if existing_user is None:
            insert_result = users_collection.insert_one(userdata)
            new_user_id = insert_result.inserted_id

            # Update userdata to include the new _id
            userdata.update({"_id": new_user_id})

            # Here, you could also update self.sid_data.user_document if necessary
            # self.sid_data.user_document = {**userdata, "_id": new_user_id}

    print("Random users have been successfully created.")




def create_random_timeline_entries(hq_id):
    global db
    # User data
    userdata = {
        "username": "data",
        "email": "obachmann@ymail.com",
        "age": 42,
        "sex": 'm',
        "hobbies": "",
        "password": "data",  # This will be encrypted
        "user_level": 32000,
        "groups": "Sysop",
        "chosen_bbs" : hq_id
    }

    # Encrypt the password
    hashed_password = bcrypt.hashpw(userdata['password'].encode('utf-8'), bcrypt.gensalt())
    userdata['password'] = hashed_password.decode('utf-8') # Store as a string in the database

    # Insert user data into the database
    users_collection = db['users']
    user_id = users_collection.insert_one(userdata).inserted_id

    # Timestamp entries collection
    timeline_entries_collection = db['timeline_entries']

    counter = 1
    for _ in range(1, 301):
        timestamp = datetime.now() + timedelta(minutes=counter-1)
        document = {
            "text": "some_text " + str(counter),  # The actual text
            "timestamp": timestamp,
            "user_id": user_id,  # Replace with the actual user ID
            "chosen_bbs": hq_id  # Replace with the actual BBS HQ ID
        }
        counter += 1
        timeline_entries_collection.insert_one(document)

    print("Timestamp entries have been created")




def create_mailboxes():
    mailboxes_collection = db['mailboxes']
    
    # Insert the "EightiesBox HQ (Headquarter)" mailbox first
    hq_mailbox_id = mailboxes_collection.insert_one({"name": "EightiesBox HQ (Headquarter)"}).inserted_id

    # Create the other 100 mailboxes
    for id in range(1, 101):
        mailboxes_collection.insert_one({"name": f"EightiesBox Box Nr. {id}"})

    # Return the inserted ID of the "EightiesBox HQ (Headquarter)" mailbox
    return hq_mailbox_id



warning_message = (
    "Warning: This application will populate the 'bbs' database with random user data."
    "\nDo you wish to proceed? (yes/no): "
)
user_response = input(warning_message)

if user_response.lower() not in ["yes", "y"]:
    print("Operation cancelled by the user.")
else:
    clear_collections()
    hq_id = str(create_mailboxes())
    # Call the function to create random users
    create_random_timeline_entries(hq_id)
    create_random_users(hq_id)


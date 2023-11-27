from pymongo import MongoClient

# Configuration for MongoDB Connection
mongo_client = MongoClient('mongodb://localhost:27017/')  # Replace with your MongoDB connection string
db = mongo_client['bbs']  # Replace with your database name

# Collections to clear
collections_to_clear = [
    'upload_token',
    'upload_requests',
    'uploads',
    'upload_files',
    'files',
    'to_be_edited',
    'oneliners'
]

def clear_collections(collections):
    for collection_name in collections:
        collection = db[collection_name]
        collection.delete_many({})  # Deletes all documents in the collection
        print(f"Cleared collection: {collection_name}")

def confirm_and_clear():
    response = input("Are you sure you want to clear all specified collections? This cannot be undone. (yes/no): ").strip().lower()
    if response == 'yes':
        clear_collections(collections_to_clear)
        print("All specified collections have been cleared.")
    else:
        print("Operation canceled. No changes were made.")

if __name__ == "__main__":
    confirm_and_clear()

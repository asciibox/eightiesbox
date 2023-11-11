from google.cloud import storage
import socketio
import datetime

class Deletefile:
    def __init__(self, util):
        self.util = util

    def query_file_by_id(self):
        self.util.goto_next_line()
        self.util.output("Enter file ID or press Enter to exit: ", 6, 0)
        self.util.ask(40, self.process_file_id)  # Ensure correct signature for ask method
        # The check for an empty string should be inside the callback method

    def process_file_id(self, file_id):
        # Iterate over the files to find the one with the matching counter
        if file_id == "":
            self.util.sid_data.menu.return_from_gosub()    
            self.util.sid_data.setCurrentAction("wait_for_menu")
            return

        try:
            file_id_num = int(file_id)
        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid ID format.", 7, 0)
            self.query_file_by_id()
            return

        # Iterate over the files to find the one with the matching index
        files = self.util.mongo_client["bbs"]["files"].find()
        for index, file in enumerate(files, start=1):
            if index == file_id_num:
                # Confirm deletion with the user
                self.util.goto_next_line()
                self.util.output(f"Confirm deletion of file: {file['filename']} (y/n)", 7, 0)
                self.util.ask(1, lambda confirm: self.confirm_deletion(confirm, file))
                return

        # If file not found by index
        self.util.goto_next_line()
        self.util.output("File with given index not found.", 7, 0)
        self.query_file_by_id()
        
    def confirm_deletion(self, confirm, file):
        if confirm.lower() == 'y':
            # Proceed with file deletion
            self.delete_file(file)
        else:
            self.util.output("Deletion cancelled.", 7, 0)
            self.query_file_by_id()

    def delete_file(self, file):
        file_document = self.util.mongo_client["bbs"]["files"].find_one({"_id": file['_id']})
        if file_document:
            # Delete file from external storage if applicable
            if 'path' in file_document:
                try:
                    # Assuming storage_url is the URL to the file in Google Cloud Storage
                    storage_client = storage.Client()
                    blob_name = file_document['path']
                    bucket = storage_client.bucket("eightiesbox_uploaded")
                    blob = bucket.blob(blob_name)
                    blob.delete()
                except Exception as e:
                    self.util.output(f"Error deleting file from external storage: {e}", 7, 0)
                    return

            # Delete file from the database
            try:
                self.util.mongo_client["bbs"]["files"].delete_one({"_id": file['_id']})
                self.util.output("File successfully deleted.", 7, 0)
            except Exception as e:
                self.util.output(f"Error deleting file from database: {e}", 7, 0)
        else:
            self.util.output("File ID not found.", 7, 0)
            self.query_file_by_id()

    
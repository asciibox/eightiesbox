# ... your existing imports ...
from google.cloud import storage
import socketio
import datetime

class Download:
    def __init__(self, util, download_invisible_files):
        self.util = util
        self.download_queue = []
        self.download_invisible_files = download_invisible_files

    def add_to_download_queue(self, file):
        # Create a signed URL for the file to be downloaded
        storage_client = storage.Client()
        bucket = storage_client.bucket('eightiesbox_uploaded')
        blob = bucket.blob(file['path'])

        # Use different quotes for the filename or escape the quotes inside the f-string
        # Set the content disposition for the response header
        response_disposition = f'attachment; filename="{file["filename"]}"'

        url = blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=15),
            method="GET",
            response_disposition=response_disposition,
        )

        self.download_queue.append(url)
        self.util.output(f"Added to queue: {file['filename']}", 7, 0)
        self.util.goto_next_line()

    def query_file_by_id(self):
        self.util.goto_next_line()
        self.util.output("Enter file ID or press Enter to exit: ", 6, 0)
        self.util.ask(35, self.process_file_id)  # Ensure correct signature for ask method
        # The check for an empty string should be inside the callback method

    def process_file_id(self, file_id):
        if not file_id:  # If file_id is None or an empty string
            if self.download_queue:
                self.emit_download_event()  # Emit download event if queue is not empty
            else:
                self.util.output("Download queue is empty. Returning to menu.", 7, 0)
                self.util.sid_data.menu.return_from_gosub()
                self.util.sid_data.setCurrentAction("wait_for_menu")
            return  # Exit the function to avoid further processing

        # Proceed with the rest of the function for non-empty file_id
        try:
            file_id_num = int(file_id)
        except ValueError:
            self.util.goto_next_line()
            self.util.output("Invalid ID format.", 7, 0)
            self.query_file_by_id()
            return
        
        # Iterate over the files to find the one with the matching counter
        files = self.util.mongo_client["bbs"]["files"].find()
        for index, file in enumerate(files, start=1):
            if index == file_id_num:
                if self.download_invisible_files == False and file['visible_file']==False:
                    self.util.goto_next_line()
                    self.util.output(f"File is not visible", 1, 0)
                    self.util.goto_next_line()
                else:
                    self.util.goto_next_line()
                    self.util.output(f"Filename: {file['filename']}", 7, 0)
                    self.util.goto_next_line()
                    self.add_to_download_queue(file)
                    self.query_file_by_id()
                    return  # Return after adding to queue
        else:
            self.util.goto_next_line()
            self.util.output("File ID not found.", 7, 0)
            self.query_file_by_id()

 
    def emit_download_event(self):
        if self.download_queue:
            # Emit an event to the client with the download queue
            print(self.download_queue)
            sid = self.util.request_id  # Get the Session ID
 
            self.util.socketio.emit('download_ready', {'files': self.download_queue}, room=sid)
            self.download_queue = []  # Clear the queue after emitting

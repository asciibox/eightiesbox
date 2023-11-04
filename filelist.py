import datetime

class Filelist:
    def __init__(self, util):
        self.util = util
        self.line_count = 0
        self.file_cursor = 0  # Local instance variable to keep track of cursor position
        self.counter = 1
        self.util.clear_screen()

    def show_file_listing(self):

        db = self.util.mongo_client["bbs"]
        collection = db["files"]

        # Retrieve all documents starting from the current cursor
        files = collection.find().skip(self.file_cursor)

        fg_color = 7  # White or light grey text
        bg_color = 0  # Black or default background

        for file in files:
            # Convert upload date from ObjectId to a readable date, if necessary
            timestamp = file['_id'].generation_time
            upload_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            file_details = [
                f"ID: {self.counter} Filename: {file['filename']}",
                f"File Size: {file['file_size']}",
                f"Upload Date: {upload_date}",
                "Description:"
            ] + file.get('description', [])

            for detail in file_details:
                self.util.output(detail, fg_color, bg_color)
                self.util.goto_next_line()
                self.line_count += 1
                if self.line_count >= self.util.sid_data.yHeight - 2:
                    self.pause_listing()
                    return  # Exit the function to wait for user input

            self.util.output("-" * 35, fg_color, bg_color)  # Separator line
            self.util.goto_next_line()
            self.line_count += 1
            self.file_cursor += 1  # Increment local cursor position
            self.counter += 1  # Increment the counter for the next file

            if self.line_count >= self.util.sid_data.yHeight - 2:
                self.pause_listing()
                return
        self.util.output("File listing ended", 6, 0)
        self.util.goto_next_line()
        self.util.wait_with_message(self.exit_callback)

    def pause_listing(self):
        self.util.askYesNo("Do you want to continue viewing the file list?", self.continue_listing)

    def continue_listing(self, response):
        self.util.goto_next_line()
        if response.lower() in ['y', 'yes']:
            self.line_count = 0  # Reset line count
            self.show_file_listing()  # Continue listing files starting from the current cursor
        else:
            self.util.output("Listing terminated by user.", 6, 0)
            # Handle cleanup and reset actions here
            self.util.sid_data.menu.return_from_gosub()
            self.util.sid_data.setCurrentAction("wait_for_menu")
            # Return to a previous menu or perform another action as needed

    def exit_callback(self):
        self.util.sid_data.menu.return_from_gosub()
        self.util.sid_data.setCurrentAction("wait_for_menu")

    # Add any other methods needed for the Filelist class here

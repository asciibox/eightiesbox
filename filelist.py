import datetime

class Filelist:
    def __init__(self, util):
        self.util = util
        self.line_count = 0
        self.file_cursor = 0  # Local instance variable to keep track of cursor position
        self.counter = 1
        self.util.clear_screen()

    def show_file_listing(self, show_visible_files):
        self.util.clear_screen()
        self.util.emit_gotoXY(0,0)
        db = self.util.mongo_client["bbs"]
        collection = db["files"]

        # Retrieve all documents starting from the current cursor
        files = collection.find().skip(self.file_cursor)


        for file in files:
            if show_visible_files == True and file['visible_file']==False:
                self.counter += 1  # Increment the counter for the next file
                print("SKIPPING")
                print(file)
                continue
            elif show_visible_files == False and file['visible_file']==True:
                print("SKIPPING")
                print(file)
                self.counter += 1  # Increment the counter for the next file
                continue
                
            # Convert upload date from ObjectId to a readable date, if necessary
            timestamp = file['_id'].generation_time
            upload_date = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            file_details = [
                f"ID: {self.counter} Filename: {file['filename']}",
                f"File Size: {file['file_size']}",
                f"Upload Date: {upload_date}",
                f"File visible: {file['visible_file']}",
                "Description:"
            ]

            # Ensure that the description is always a list
            description = file.get('description', [])
            if not isinstance(description, list):
                description = [description]  # Make it a list even if it's a single string

            # Then extend the file_details list with the description
            file_details.extend(description)

            if file['visible_file']:
                fg_color = 7  # White or light grey text
                bg_color = 0  # Black or default background
            else:
                fg_color = 1  # Red
                bg_color = 0  # Black or default background

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

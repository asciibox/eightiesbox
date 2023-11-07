# ... your existing imports ...
from google.cloud import storage
import socketio
import datetime
from uploadeditor import UploadEditor
from menubar_editfileeditor import MenuBarEditFileEditor

class EditFile(UploadEditor):
    def __init__(self, util):
        super().__init__(util)
        self.util = util
        self.download_queue = []

    def start(self):
        self.clear_screen()
        self.util.sid_data.color_array = []
        self.util.sid_data.color_bgarray = []

        # Check if self.first_document is set
        if not hasattr(self, 'first_document') or not self.first_document:
            self.util.goto_next_line()
            self.util.output("No file selected.", 7, 0)
            self.exit()
            return

        # Assuming 'description' is a list of strings as seen in the image
        # If the selected file is already available in self.first_document, use it directly
        if 'description' in self.first_document:
            # Set input values from the description
            self.util.sid_data.input_values = self.first_document['description']
            
            # Initialize color_array and color_bgarray with empty lists
            self.util.sid_data.color_array = []
            self.util.sid_data.color_bgarray = []
            
            # Fill up color_array and color_bgarray
            for line in self.first_document['description']:
                # Create a list with the value 7 for each character in the line for color_array
                self.util.sid_data.color_array.append([7] * len(line))
                # Create a list with the value 0 for each character in the line for color_bgarray
                self.util.sid_data.color_bgarray.append([0] * len(line))

        else:
            # Handle the case where there is no description or the structure is different
            self.util.sid_data.input_values = []
        print("INPUT VALUES")
        print(self.util.sid_data.input_values)
        # Now that input_values is set up, call display_editor
        self.display_editor(self.util.sid_data.color_array, self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None)
        self.util.sid_data.setCurrentAction("wait_for_editfile")
        self.update_first_line()

    def query_file_by_id(self):
        self.util.goto_next_line()
        self.util.output("Enter file ID or press Enter to exit: ", 6, 0)
        self.util.ask(40, self.process_file_id)  # Ensure correct signature for ask method
        # The check for an empty string should be inside the callback method

    def process_file_id(self, file_id):
        # Assuming file_id is a string and needs to be converted to integer
        if file_id:
            try:
                file_id_num = int(file_id)
            except ValueError:
                self.util.goto_next_line()
                self.util.output("Invalid ID format. Please enter a number.", 7, 0)
                self.query_file_by_id()
                return

            # Retrieve all files and find one with the matching index
            files = self.util.mongo_client["bbs"]["files"].find()
            for index, file in enumerate(files, start=1):
                if index == file_id_num:
                    self.first_document = file
                    self.ask_change_filename()
                    return
            else:
                self.util.goto_next_line()
                self.util.output("File ID not found.", 7, 0)
                self.query_file_by_id()
        else:
            # If the user just presses enter, exit or proceed with another action
            self.exit()

    def ask_change_filename(self):
        self.util.goto_next_line()
        self.util.output(self.first_document['filename'], 6,0)
        self.util.goto_next_line()
        self.util.output("Change filename? (Y/N): ", 7, 0)
        self.util.ask(1, self.process_filename_change_decision)

    def process_filename_change_decision(self, decision):
        if decision.lower() == 'y':
            self.util.goto_next_line()
            self.util.output("Enter new filename: ", 7, 0)
            self.util.ask(40, self.change_filename)
        elif decision.lower() == 'n':
            self.ask_file_visibility_change()  # Proceed with the next step if the user doesn't want to change the filename
        else:
            self.util.goto_next_line()
            self.util.output("Invalid choice. Please enter Y or N.", 7, 0)
            self.ask_change_filename()

    def change_filename(self, new_filename):
        # Assuming self.first_document is the document retrieved from the database
        if not self.first_document:
            self.util.goto_next_line()
            self.util.output("No file selected for renaming.", 7, 0)
            self.query_file_by_id()
            return

        # Check if new filename is not empty and does not already exist
        if new_filename and not self.util.mongo_client["bbs"]["files"].find_one({"filename": new_filename}):
            # Update the filename in the database
            update_result = self.util.mongo_client["bbs"]["files"].update_one(
                {"_id": self.first_document["_id"]},
                {"$set": {"filename": new_filename}}
            )

            # Check if the update was successful
            if update_result.modified_count > 0:
                self.util.goto_next_line()
                self.util.output("Filename updated successfully.", 7, 0)
                self.exit()
            else:
                self.util.goto_next_line()
                self.util.output("No changes made to filename.", 7, 0)
                self.exit()
        else:
            self.util.goto_next_line()
            if new_filename:
                self.util.output("Filename already exists or is invalid. Try again.", 7, 0)
            else:
                self.util.output("Filename cannot be empty. Try again.", 7, 0)

            self.ask_change_filename()  # Ask again for a new filename

        # Proceed with the next step
        self.ask_file_visibility_change()
        
    def escape2FileEditEditor(self):
        sub_menus = {
            'File': ['Save and exit', 'Exit without saving'],
            'Edit': ['Clear description', 'Leave menu bar'],
        }
        self.sid_data.setMenuBar(MenuBarEditFileEditor(sub_menus, self.util, self.first_document['_id']))

        self.sid_data.setCurrentAction("wait_for_menubar_ansieditor")

    def ask_file_visibility_change(self):
        # Check the current visibility status of the file
        if self.first_document['visible_file']:
            self.util.goto_next_line()
            self.util.output("File is currently visible. Change visibility to invisible? (Y/N): ", 7, 0)
        else:
            self.util.goto_next_line()
            self.util.output("File is currently invisible. Change visibility to visible? (Y/N): ", 7, 0)
        
        self.util.ask(1, self.process_visibility_change_decision)

    def process_visibility_change_decision(self, decision):
        if decision.lower() == 'y':
            new_visibility = not self.first_document['visible_file']
            # Update the file visibility in the database
            update_result = self.util.mongo_client["bbs"]["files"].update_one(
                {"_id": self.first_document["_id"]},
                {"$set": {"visible_file": new_visibility}}
            )

            # Check if the update was successful
            if update_result.modified_count > 0:
                visibility_status = "visible" if new_visibility else "invisible"
                self.util.goto_next_line()
                self.util.output(f"File visibility updated to {visibility_status}.", 7, 0)
            else:
                self.util.goto_next_line()
                self.util.output("No changes made to file visibility.", 7, 0)
            
            self.start()  # Proceed with the next step
        elif decision.lower() == 'n':
            self.start()  # Proceed with the next step if the user doesn't want to change visibility
        else:
            self.util.goto_next_line()
            self.util.output("Invalid choice. Please enter Y or N.", 7, 0)
            self.ask_file_visibility_change()  # Ask again for the visibility decision

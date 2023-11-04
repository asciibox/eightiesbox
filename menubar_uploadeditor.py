from pymongo import MongoClient
from menutexteditor import *
from menubar import MenuBar

''' When editing a menu '''
class MenuBarUploadEditor(MenuBar):
    def __init__(self, sub_menus, util, file_id):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_uploadeditor")
        self.current_filename = ""
        self.file_id = file_id
        
        

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[current_menu]][self.current_sub_menu_indexes[current_menu]]

            if selected_option == "Leave menu bar":
                self.leave_menu_bar()
            elif selected_option == "Save and proceed":
                # Assuming 'files container' is a collection in your database
                # and you have a method to get the database client, e.g., self.util.get_db_client()
                db_client = self.util.get_db_client()
                files_collection = db_client['files_container']
                
                # Update the document with the _id of self.file_id with the description from self.util.sid_data.input_values
                update_result = files_collection.update_one(
                    {'_id': self.file_id},  # Query for the specific document by _id
                    {'$set': {'description': self.util.sid_data.input_values}}  # Set the new description
                )
                
                # Check if the update was successful and act accordingly
                if update_result.modified_count == 1:
                    self.output("File description updated successfully.", 6,0)
                    self.wait_with_message(self.leave_menu_bar)
                    # Add any additional steps here if needed after a successful update
                else:
                    self.output("Failed to update file description.", 6, 0)
                    self.wait_with_message(self.leave_menu_bar)

                # After save functionality, proceed with other tasks or redraw the menu
                # self.draw_sub_menu()  # For example, to redraw the sub-menu

            elif selected_option == "Save and exit":
                # Add save functionality here as well before exiting
                self.leave_menu_bar()
            elif selected_option == "Exit without saving":
                self.leave_menu_bar()
            else:
                print("Hello world")

        else:
            self.in_sub_menu = True
            self.draw_sub_menu()  # This function is assumed to draw the sub-menu


   

    def leave_menu_bar(self):
        self.sid_data.upload_editor.clear_screen()
        self.sid_data.upload_editor.update_first_line()
        self.sid_data.upload_editor.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None )
        self.sid_data.setCurrentAction("wait_for_uploadeditor")
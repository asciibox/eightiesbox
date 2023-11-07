from pymongo import MongoClient
from menutexteditor import *
from menubar import MenuBar
from bson.objectid import ObjectId

class MenuBarEditFileEditor(MenuBar):
    def __init__(self, sub_menus, util, file_id):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, util)
        # Add any additional properties or methods specific to MenuBarANSI here
        util.sid_data.setCurrentAction("wait_for_menubar_editfile")
        self.current_filename = ""
        self.file_id = file_id
        
        

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[current_menu]][self.current_sub_menu_indexes[current_menu]]

            if selected_option == "Clear description":        
                self.util.sid_data.color_array=[]
                self.util.sid_data.color_bgarray=[]
                self.util.sid_data.input_values=[]
                self.leave_menu_bar()
            if selected_option == "Leave menu bar":
                self.leave_menu_bar()
            elif selected_option == "Save and exit":
                # Assuming 'files container' is a collection in your database
                mongo_client = self.util.mongo_client
                db = mongo_client['bbs']
                
                files_collection = db['files']
                
                # Update the document with the _id of self.file_id with the description from self.util.sid_data.input_values
                update_result = files_collection.update_one(
                    {'_id': self.file_id},  # Query for the specific document by _id
                    {'$set': {'description': self.util.sid_data.input_values}}  # Set the new description
                )
                
                # Check if the update was successful and act accordingly
                if update_result.modified_count == 1:

                    to_be_edited_collection = db['to_be_edited']
    
                    try:
                        file_id_obj = ObjectId(self.file_id)
                        # Attempt to delete the document with the given file_id
                        delete_result = to_be_edited_collection.delete_one({'file_id': file_id_obj})
                        
                        # Check if the document was deleted
                        if delete_result.deleted_count == 1:
                            pass
                        else:
                            print(f"No entry found with file_id: {self.file_id}")

                    except Exception as e:
                            # Handle any exceptions that occur during the delete operation
                            print(f"An error occurred while attempting to remove the entry: {e}")
                            return False
                
                    self.output("File description updated successfully.", 6,0)
                    self.util.wait_with_message(self.proceed_callback)
                    # Add any additional steps here if needed after a successful update
                    self.exit()
                else:
                    self.output("Failed to update file description.", 6, 0)
                    self.util.wait_with_message(self.proceed_callback)
                    self.exit()
                    
                # After save functionality, proceed with other tasks or redraw the menu
                # self.draw_sub_menu()  # For example, to redraw the sub-menu

            elif selected_option == "Exit without saving":
                self.exit()
            else:
                print("Hello world")

        else:
            self.in_sub_menu = True
            self.draw_sub_menu()  # This function is assumed to draw the sub-menu


    def proceed_callback(self):
        self.sid_data.setCurrentAction("wait_for_editfile")
        self.sid_data.edit_file.start()

    def leave_menu_bar(self):
        self.sid_data.edit_file.clear_screen()
        self.sid_data.edit_file.update_first_line()
        self.sid_data.edit_file.display_editor(self.util.sid_data.color_array,self.util.sid_data.color_bgarray, self.util.sid_data.input_values, None )
        self.sid_data.setCurrentAction("wait_for_editfile")
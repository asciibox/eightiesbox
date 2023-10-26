from userpicker import *


class UserPickerOnline(UserPicker):
    def __init__(self, util, existing_username, launchMenuCallback):
        super().__init__(util, existing_username, launchMenuCallback)
        
        # Get online usernames from all_sid_data
        self.online_usernames = [sid_data.user_document['username'] for sid, sid_data in self.util.all_sid_data.items() if sid_data.user_document]
        current_username = self.util.sid_data.user_name
        if current_username in self.online_usernames:
            self.online_usernames.remove(current_username)
            
        # Overriding the total_users and total_pages for online users
        self.total_users = len(self.online_usernames)
        self.total_pages = self.total_users // self.users_per_page
        if self.total_users % self.users_per_page != 0:
            self.total_pages += 1

    def show_page(self, page_number):
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        self.util.output(f"Page: {page_number + 1}/{self.total_pages}", 6, 0)
        
        # Only query for online users from the MongoDB collection
        start_index = page_number * self.users_per_page
        end_index = start_index + self.users_per_page
        query_filter = {'username': {'$in': self.online_usernames}}
        self.users_on_page = list(self.users_collection.find(query_filter)[start_index:end_index])
        
        # Reset current_selection when switching pages
        self.current_selection = 0

        # Draw usernames
        self.draw_users()

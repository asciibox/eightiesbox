from pymongo import MongoClient

class UserPicker:
    def __init__(self, util, existing_username, launchMenuCallback):
        self.util = util
        self.util.sid_data.setCurrentAction('wait_for_userpicker')
        self.launchMenuCallback = launchMenuCallback
        self.current_page = 0  # Starts with the first page
        self.users_per_page = self.util.sid_data.yHeight - 1  # -1 for the page indicator line
        self.current_selection = 0  # The currently selected username index on the page

        db = self.util.mongo_client['bbs']
        self.users_collection = db['users']

        self.total_users = self.users_collection.count_documents({'chosen_bbs': self.sid_data.chosen_bbs})
        self.total_pages = self.total_users // self.users_per_page
        if self.total_users % self.users_per_page != 0:
            self.total_pages += 1  # Add an extra page if there are remaining users

    def show_options(self):
        self.show_page(self.current_page)
        # Highlight the first user by default
        self.current_selection = 0
        self.draw_users()

    def show_page(self, page_number):
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)
        self.util.output(f"Page: {page_number + 1}/{self.total_pages}", 6, 0)

        start_index = page_number * self.users_per_page
        end_index = start_index + self.users_per_page
        self.users_on_page = list(self.users_collection.find({'chosen_bbs': self.sid_data.chosen_bbs})[start_index:end_index])
        
        # Reset current_selection when switching pages
        self.current_selection = 0
        
        # Draw usernames
        self.draw_users()

    def draw_users(self):
        for i, user in enumerate(self.users_on_page):
            self.util.sid_data.setStartY(i + 1)
            self.util.sid_data.setStartX(0)
            fg_color = 11 if i == self.current_selection else 6  # Highlight if current selection
            self.util.output(user['username'], fg_color, 0)

    def draw_single_user(self, index, fg_color):
        self.util.sid_data.setStartY(index + 1)
        self.util.sid_data.setStartX(0)
        self.util.output(self.users_on_page[index]['username'], fg_color, 0)

    def handle_key(self, key):
        if key == 'ArrowRight':
            if self.current_page < self.total_pages - 1:
                self.current_page += 1
                self.show_page(self.current_page)
        elif key == 'ArrowLeft':
            if self.current_page > 0:
                self.current_page -= 1
                self.show_page(self.current_page)
        elif key == 'ArrowDown':
            if self.current_selection < min(len(self.users_on_page) - 1, self.users_per_page - 1):
                # Redraw the current selection with non-highlight color
                self.draw_single_user(self.current_selection, 6)

                self.current_selection += 1

                # Redraw the new selection with highlight color
                self.draw_single_user(self.current_selection, 11)

        elif key == 'ArrowUp':
            if self.current_selection > 0:
                # Redraw the current selection with non-highlight color
                self.draw_single_user(self.current_selection, 6)

                self.current_selection -= 1

                # Redraw the new selection with highlight color
                self.draw_single_user(self.current_selection, 11)
        elif key == 'Enter':
            selected_username = self.users_on_page[self.current_selection]['username']
            self.launchMenuCallback(selected_username)  # Call the callback with the selected username
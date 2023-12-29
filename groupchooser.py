class GroupChooser:
    def __init__(self, util, callback, turned_on_group_string):
        self.util = util
        self.mongo_client = util.mongo_client
        self.db = self.mongo_client['bbs']
        self.groups_collection = self.db['groups']
        self.load_groups()
        self.current_selection = 0
        self.selected_groups = set()
        self.callback = callback

        # Populate selected_groups with the groups from turned_on_group_string
        turned_on_groups = turned_on_group_string.split(',')
        for group_name in turned_on_groups:
            group_name = group_name.strip()
            if any(group['name'] == group_name for group in self.groups):
                self.selected_groups.add(group_name)

    def load_groups(self):
        self.groups = list(self.groups_collection.find({'chosen_bbs': self.util.sid_data.chosen_bbs}))

    def draw_groups(self):
        self.util.clear_screen()
        for i, group in enumerate(self.groups):
            self.util.sid_data.setStartY(i)
            self.util.sid_data.setStartX(2)

            status = "on " if group['name'] in self.selected_groups else "off"
            fg_color = 11 if i == self.current_selection else 6  # Highlight if current selection

            self.util.output(f"{group['name']} - {status}", fg_color, 0)

    def toggle_group(self):
        group_name = self.groups[self.current_selection]['name']
        if group_name in self.selected_groups:
            self.selected_groups.remove(group_name)
        else:
            self.selected_groups.add(group_name)

        self.draw_single_group(self.current_selection, 11)

    def draw_single_group(self, index, fg_color):
        self.util.sid_data.setStartY(index)
        self.util.sid_data.setStartX(2)

        status = "on " if self.groups[index]['name'] in self.selected_groups else "off"
        self.util.output(f"{self.groups[index]['name']} - {status}", fg_color, 0)

    def handle_key(self, key):
        if key == 'ArrowDown':
            if self.current_selection < len(self.groups) - 1:
                self.draw_single_group(self.current_selection, 6)
                self.current_selection += 1
                self.draw_single_group(self.current_selection, 11)
        elif key == 'ArrowUp':
            if self.current_selection > 0:
                self.draw_single_group(self.current_selection, 6)
                self.current_selection -= 1
                self.draw_single_group(self.current_selection, 11)
        elif key == 'Enter':
            self.toggle_group()
        elif key == 'Escape':
            self.util.sid_data.setCurrentAction("wait_for_menubox")
            self.callback(self.get_selected_groups_string())


    def get_selected_groups_string(self):
        return ','.join(self.selected_groups)

    # Add other necessary methods and functionalities

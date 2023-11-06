from pymongo import MongoClient
from areachange import AreaChange

class FileAreaChange(AreaChange):
    def __init__(self, util, callback=None):
        super().__init__(util)
        self.util = util
        self.displayed_areas = []  # Store the displayed file areas
        self.callback = callback  # Add the callback here

    def show_file_areas(self):
        self.util.clear_screen()
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        user_level = self.sid_data.user_document['user_level']

        file_areas = list(db['fileareas'].find().sort('order'))

        self.displayed_areas.clear()
        
        areas_found = False
        for i, area in enumerate(file_areas):
            if area['min_level'] <= user_level:
                self.sid_data.setStartX(0)
                self.sid_data.setStartY(i)
                areas_found = True
                self.util.output(f"{i+1}. {area['name']}", 7, 0)
                self.displayed_areas.append(area)  # Add area to displayed_areas list

        if not areas_found:
            self.util.clear_screen()
            self.sid_data.setStartX(0)
            self.sid_data.setStartY(0)    
            self.util.output_wrap("No file areas found", 1, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.exit)
            return

        self.sid_data.setStartX(0)
        self.sid_data.setStartY(len(file_areas))
        self.util.output_wrap("Please enter the counter of the file area you'd like to access: ", 7, 0)
        self.util.ask(2, self.process_file_area_id)  # Assuming counter will be at most two digits

    def process_file_area_id(self, input_counter):
        try:
            selected_idx = int(input_counter) - 1
            selected_area = self.displayed_areas[selected_idx]
            self.sid_data.setCurrentFileArea(selected_area)
            total_files = self.get_total_files(selected_area)
            self.util.goto_next_line()
            self.util.output_wrap(f"You have accessed the file area: {selected_area['name']}", 7, 0)
            self.util.goto_next_line()
            self.util.output_wrap(f"Total Files: {total_files}", 7, 0)
            self.util.goto_next_line()
            self.util.wait_with_message(self.access_callback)
            
        except (ValueError, IndexError):
            self.util.output_wrap("Invalid counter.", 7, 0)
            self.util.goto_next_line()
            self.util.askYesNo("Do you want to stop creating a new file ?", self.invalid_counter_callback)
        

    def invalid_counter_callback(self, response):
        if response.lower() == 'y':
            self.exit()
        else:
            self.show_file_areas()
            

    def access_callback(self):
        if self.callback:  # Invoke the callback if it's set
            self.callback()
            return

        self.exit()

    def exit(self):
        self.sid_data.menu.return_from_gosub()
        self.sid_data.setCurrentAction("wait_for_menu")

    def get_total_files(self, selected_area):
        mongo_client = self.util.mongo_client
        db = mongo_client['bbs']
        count = db['files'].count_documents({"area_id": selected_area['_id']})
        return count


        return count

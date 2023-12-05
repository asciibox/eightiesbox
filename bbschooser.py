from basicansi import BasicANSI

class BBSChooser(BasicANSI):
    def __init__(self, util):
        super().__init__(util)
        
        self.startFile = 'welcome'

        self.util = util
        self.util.sid_data.setCurrentAction('wait_for_bbschooser')
        self.current_page = 0
        self.bbs_per_page = self.util.sid_data.yHeight - 9  # Adjust for frame and page indicator
        self.current_selection = 0  # The currently selected BBS index on the page

        db = self.util.mongo_client['bbs']
        self.mailboxes_collection = db['mailboxes']

        self.ensure_default_bbs()

        self.total_bbs = self.mailboxes_collection.count_documents({})
        self.total_pages = self.total_bbs // self.bbs_per_page
        if self.total_bbs % self.bbs_per_page != 0:
            self.total_pages += 1

        self.draw_frame()
        self.show_page(self.current_page)

    def ensure_default_bbs(self):
        if self.mailboxes_collection.count_documents({}) == 0:
            self.mailboxes_collection.insert_one({"name": "EightiesBox HQ (Headquarter)"})


    def draw_frame(self):
        # Start with the top-left corner
        self.sid_data.startX=0
        self.sid_data.startY=0
        self.util.output("+", 11, 4)

        # Draw the top horizontal line
        print(self.sid_data.xWidth )
        print(self.sid_data.yHeight )
        for i in range(1, self.sid_data.xWidth-1):
            self.util.output("-", 11, 4)

        # End with the top-right corner
        self.util.output("+", 11, 4)

        # Draw vertical lines
        for y in range(1, self.sid_data.yHeight - 4):
            self.sid_data.startX = 0
            self.sid_data.startY = y
            self.util.output("|", 11, 4)
            self.sid_data.startX = self.sid_data.xWidth - 1
            self.util.output("|", 11, 4)

        # Start with the bottom-left corner
        self.sid_data.startX = 0
        self.sid_data.startY = self.sid_data.yHeight - 4
            
        self.util.output("+", 11, 4)

        # Draw the bottom horizontal line
        for i in range(1, self.sid_data.xWidth-1):
            self.util.output("-", 11, 4)

        # End with the bottom-right corner
        self.util.output("+", 11, 4)

        self.sid_data.startX = 2
        self.sid_data.startY = 2
        self.util.output("Press C to create a new BBS", 6, 0)


  
    def show_page(self, page_number):
      
        self.util.sid_data.setStartX(2)
        self.util.sid_data.setStartY(1)
        self.util.output(f"Page: {page_number + 1}/{self.total_pages} - Please choose the BBS you want to login to using cursor UP/DOWN (< and > arrows) and by pressing ENTER", 6, 0)


        start_index = page_number * self.bbs_per_page
        end_index = start_index + self.bbs_per_page
        self.bbs_on_page = list(self.mailboxes_collection.find()[start_index:end_index])

        # Reset current_selection when switching pages
        self.current_selection = 0
        
        # Draw BBS names
        self.draw_bbses()

    def draw_bbses(self):
        for i, bbs in enumerate(self.bbs_on_page):
            self.util.sid_data.setStartY(i + 4)  # Adjust for frame and page indicator
            self.util.sid_data.setStartX(2)
            fg_color = 11 if i == self.current_selection else 6  # Highlight if current selection
            self.util.output(bbs['name'], fg_color, 0)  # Assuming 'name' is the field for BBS name

    def draw_single_bbs(self, index, fg_color):
        self.util.sid_data.setStartY(index + 4)  # Adjust for frame and page indicator
        self.util.sid_data.setStartX(2)
        self.util.output(self.bbs_on_page[index]['name'], fg_color, 0)

    def handle_key(self, key):
        print(key)
        if key == 'ArrowRight':
            if self.current_page < self.total_pages - 1:
                self.util.clear_screen()
                self.draw_frame()
                self.current_page += 1
                self.show_page(self.current_page)
        elif key == 'ArrowLeft':
            if self.current_page > 0:
                self.util.clear_screen()
                self.draw_frame()
                self.current_page -= 1
                self.show_page(self.current_page)
        elif key == 'ArrowDown':
            print(self.bbs_per_page )
            if self.current_selection < min(len(self.bbs_on_page) - 1, self.bbs_per_page - 1):
                # Redraw the current selection with non-highlight color
                self.draw_single_bbs(self.current_selection, 6)

                self.current_selection += 1

                # Redraw the new selection with highlight color
                self.draw_single_bbs(self.current_selection, 11)

        elif key == 'ArrowUp':
            if self.current_selection > 0:
                # Redraw the current selection with non-highlight color
                self.draw_single_bbs(self.current_selection, 6)

                self.current_selection -= 1

                # Redraw the new selection with highlight color
                self.draw_single_bbs(self.current_selection, 11)
        elif key == 'Enter':
            print(self.current_selection)
            self.login(self.current_selection)


    def login(self, current_selection):
        
        data2 = { 'filename' : self.startFile+'-'+str(self.util.sid_data.xWidth)+'x'+str(self.util.sid_data.yHeight), 'x' : self.util.sid_data.xWidth, 'y': self.util.sid_data.yHeight }
        self.util.clear_screen()
        self.util.show_file(data2, self.util.emit_current_string)
        self.util.goto_next_line()
        
        self.util.output_wrap("Please enter your name: ", 3, 0)
        self.util.ask(35, self.util.usernameCallback)


    # Usage
    def choose_bbs(self, data):
        print("choose bbs")
        print(data)
        self.sid_data.setBBSChooser(BBSChooser(self))
        self.sid_data.bbsChooser.draw_frame()
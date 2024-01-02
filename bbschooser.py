from basicansi import BasicANSI
from pycode.renderer import Renderer

class BBSChooser(BasicANSI):
    def __init__(self, util):
        super().__init__(util)
        
        self.startFile = 'welcome'

        self.util = util
        self.util.sid_data.setCurrentAction('wait_for_bbschooser')
        self.current_page = 0
        self.bbs_per_page = 5
        self.current_selection = 0  # The currently selected BBS index on the page

        db = self.util.mongo_client['bbs']
        self.mailboxes_collection = db['mailboxes']

        self.ensure_default_bbs()

        self.total_bbs = self.mailboxes_collection.count_documents({})

        # Calculate the number of entries on the first and subsequent pages
        entries_on_first_page = self.bbs_per_page
        entries_on_other_pages = self.util.sid_data.yHeight - 10

        # Calculate total pages
        if self.total_bbs > entries_on_first_page:
            remaining_entries = self.total_bbs - entries_on_first_page
            additional_pages = (remaining_entries + entries_on_other_pages - 1) // entries_on_other_pages
            self.total_pages = 1 + additional_pages
        else:
            self.total_pages = 1 if self.total_bbs > 0 else 0

        self.draw_frame(16, 0)
        self.show_page(self.current_page)

        self.sid_data.setRenderer(Renderer(self.util, None))
        if self.sid_data.xWidth > 80:
            self.sid_data.renderer.render_page("html/startpage.html")
        if self.sid_data.xWidth > 40:
            self.sid_data.renderer.render_page("html/startpage_medium.html")
        else:
            self.sid_data.renderer.render_page("html/startpage_small.html")
    def ensure_default_bbs(self):
        if self.mailboxes_collection.count_documents({}) == 0:
            self.mailboxes_collection.insert_one({"name": "EightiesBox HQ (Headquarter)"})


    def draw_frame(self, yHeight, page):
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
        for y in range(1, yHeight - 6):
            self.sid_data.startX = 0
            self.sid_data.startY = y
            self.util.output("|", 11, 4)
            self.sid_data.startX = self.sid_data.xWidth - 1
            self.util.output("|", 11, 4)

        # Start with the bottom-left corner
        self.sid_data.startX = 0
        self.sid_data.startY = yHeight - 6
            
        self.util.output("+", 11, 4)

        # Draw the bottom horizontal line
        for i in range(1, self.sid_data.xWidth-1):
            self.util.output("-", 11, 4)

        # End with the bottom-right corner
        self.util.output("+", 11, 4)

        self.sid_data.startX = 2
        self.sid_data.startY = 2
        self.util.output("Press C to create a new BBS", 6, 0)

        if page == 0:
            self.sid_data.startX = 2
            self.sid_data.startY = yHeight - 4
            if (self.sid_data.yHeight>50):
                self.util.output("Impressum: Oliver Bachmann, Luisenstr. 34, 76137 Karlsruhe, Germany", 6, 0)
            else:
                self.util.output("Oliver Bachmann, Luisenstr. 34", 6, 0)
                self.sid_data.startX = 2
                self.sid_data.startY = yHeight - 3
                self.util.output("76137 Karlsruhe, Germany", 6,0 )


  
    def show_page(self, page_number):
      
        if page_number == 0:
            self.bbs_per_page = 5
            start_index = 0
            end_index = 5
        else:
            self.bbs_per_page = self.util.sid_data.yHeight - 10  # Or any other calculation for long list
            start_index = (page_number-1) * self.bbs_per_page + 5
            end_index = start_index + self.bbs_per_page
        self.bbs_on_page = list(self.mailboxes_collection.find()[start_index:end_index])

        self.util.sid_data.setStartX(2)
        self.util.sid_data.setStartY(1)
        self.util.output(f"Page: {page_number + 1}/{self.total_pages} - Please choose the BBS you want to login to using cursor UP/DOWN (< and > arrows) and by pressing ENTER", 6, 0)


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
                self.draw_frame(self.util.sid_data.yHeight, self.current_page - 1)
                self.current_page += 1
                self.show_page(self.current_page)
        elif key == 'ArrowLeft':
            if self.current_page > 0:
                if self.current_page > 1:
                    self.util.clear_screen()
                    self.draw_frame(self.util.sid_data.yHeight, self.current_page + 1)
                    self.current_page -= 1
                    self.show_page(self.current_page)
                else:
                    self.util.clear_screen()
                    self.draw_frame(15, self.current_page)
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
            # Get the selected BBS document
            selected_bbs = self.bbs_on_page[self.current_selection]

            # Convert the ObjectId to a string
            bbs_id_str = str(selected_bbs['_id'])

            # Store the string representation of the unique ID of the BBS
            self.util.sid_data.chosen_bbs = bbs_id_str

            # Now you can emit the event with the string ID
            self.util.socketio.emit('set_chosen_bbs', {'chosen_bbs': self.sid_data.chosen_bbs})

            self.login(self.current_selection)
            
        elif key == 'C' or key =='c':
            self.util.sid_data.chosen_bbs = ""
            self.login(0)


    def login(self, current_selection):
        
        data2 = { 'filename' : self.startFile+'-'+str(self.util.sid_data.xWidth)+'x'+str(self.util.sid_data.yHeight), 'x' : self.util.sid_data.xWidth, 'y': self.util.sid_data.yHeight }
        self.util.clear_screen()
        self.util.show_file(data2, self.util.emit_current_string)
        self.util.goto_next_line()
        
        if self.util.sid_data.chosen_bbs == "":
            self.util.output_wrap("Please enter the name of the new BBS: ", 3, 0)
            self.util.ask(35, self.util.bbsCallback)
        else:
            self.util.output_wrap("Please enter your name: ", 3, 0)
            self.util.ask(35, self.util.usernameCallback)


    # Usage
    def choose_bbs(self, data):
        self.sid_data.setBBSChooser(BBSChooser(self))
        self.sid_data.bbsChooser.draw_frame()
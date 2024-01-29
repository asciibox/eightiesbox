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
        self.current_x = 0

        self.TOP = 21

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

        
        if self.sid_data.xWidth > 80:
            self.sid_data.setRenderer(Renderer(self.util, None, "html/startpage.html"))
        elif self.sid_data.xWidth > 40:
            self.sid_data.setRenderer(Renderer(self.util, None, "html/startpage_medium.html"))
        else:
            self.sid_data.setRenderer(Renderer(self.util, None, "html/startpage_small.html"))
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
        self.util.output("Press Control-C to create a new BBS", 6, 0)

        if page == 0:
            self.sid_data.startX = 2
            self.sid_data.startY = yHeight - 4
            if (self.sid_data.yHeight>40):
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
            self.util.emit_link(len(bbs['name']), bbs['_id'], self.bbs_clicked, 'bbs_click'+str(bbs['_id']), self.util.sid_data.startX, self.util.sid_data.startY)
            self.util.output(bbs['name'], fg_color, 0)  # Assuming 'name' is the field for BBS name

    def draw_single_bbs(self, index, fg_color):
        self.util.sid_data.setStartY(index + 4)  # Adjust for frame and page indicator
        self.util.sid_data.setStartX(2)
        self.util.output(self.bbs_on_page[index]['name'], fg_color, 0)

    def handle_key(self, key, key_status_array):
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

            self.bbs_clicked(bbs_id_str)
            return
            
        elif (key == 'C' or key == 'c') and key_status_array[1]==True:
            self.util.sid_data.chosen_bbs = ""
            self.login()
            return
        
        elif key == 'Backspace':
            originating_session_sid_data = self.util.all_sid_data.get(self.util.request_id)
            if originating_session_sid_data:
                originating_line_number = originating_session_sid_data.screen_line_number

                if originating_line_number is not None:
                    if originating_session_sid_data.current_action == "wait_for_bbschooser" and originating_session_sid_data.xWidth > 50:
                        # Check if the current line is not empty
                        if len(originating_session_sid_data.current_text[originating_line_number]) > 0:
                            # Remove the last character
                            originating_session_sid_data.current_text[originating_line_number] = \
                                originating_session_sid_data.current_text[originating_line_number][:-1]

                            # Update the cursor position
                            new_cursor_pos = len(originating_session_sid_data.current_text[originating_line_number])
                            originating_session_sid_data.current_x[originating_line_number] = new_cursor_pos

                            # Broadcast the update
                            self.broadcast_clear_line(originating_line_number+self.TOP)
                            self.broadcast_update(originating_session_sid_data.current_text[originating_line_number], 
                                                originating_line_number, 
                                                self.util.request_id)

        elif len(key) == 1:
            originating_session_sid_data = self.util.all_sid_data.get(self.util.request_id)
            if originating_session_sid_data:
                originating_line_number = originating_session_sid_data.screen_line_number

                if originating_line_number is not None:
                    if originating_session_sid_data.current_action == "wait_for_bbschooser" and originating_session_sid_data.xWidth > 50:
                        # Append key to the correct line of the originating session
                        while len(originating_session_sid_data.current_text) <= originating_line_number:
                            originating_session_sid_data.current_text.append("")
                        while len(originating_session_sid_data.current_x) <= originating_line_number:
                            originating_session_sid_data.current_x.append(0)
                        originating_session_sid_data.current_text[originating_line_number] += key

                        if len(originating_session_sid_data.current_text[originating_line_number]) >= originating_session_sid_data.xxWidth:
                                        # If new cursor position is beyond the width, handle line break and shift
                                        half_width = originating_session_sid_data.xxWidth // 2
                                        current_text = self.get_current_line_text(originating_session_sid_data, originating_line_number)
                                        shifted_text = current_text[-half_width:]
                                        self.broadcast_clear_line( originating_line_number + self.TOP)
                                        originating_session_sid_data.current_text[originating_line_number] = shifted_text

                        self.broadcast_update(originating_session_sid_data.current_text[originating_line_number], originating_line_number, self.util.request_id)
                else:
                    print("Error: Originating line number not found for session", self.util.request_id)
            else:
                print("Error: Session data not found for request ID", self.util.request_id)


                   

   # Broadcast update method
    def broadcast_update(self, text, line_number, origin_sid):
        for sid, sid_data in self.util.all_sid_data.items():
            if sid_data.current_action == "wait_for_bbschooser" and sid_data.xWidth > 50:
                self.update_session_line(sid, sid_data, text, line_number)

    def broadcast_clear_line(self, line_number):
        for sid, sid_data in self.util.all_sid_data.items():
                self.util.clear_session_line(sid, sid_data, line_number)

    # Update session line method
    def update_session_line(self, sid, sid_data, text, line_number):
        sid_data.setStartX(0)
        sid_data.setStartY(line_number+self.TOP)
        sid_data.util.output(text, 7, 0)  # Adjust colors as needed

    def redraw_text_at_line(self, sid, sid_data, text, line_number):
        # Update the current session
        # self.update_session_line(sid, sid_data, text, line_number+self.TOP)

        # Broadcast the update to all other sessions
        self.broadcast_update(text, line_number+self.TOP, sid)

    def get_current_line_text(self, session_sid_data, line_number):
        # Check if the line number is valid
        if 0 <= line_number < len(session_sid_data.current_text):
            # Return the text of the specified line
            cltext = session_sid_data.current_text[line_number]
            return cltext
        else:
            # Return an empty string or handle the error if the line number is invalid
            return ""

    def bbs_clicked(self, bbs_id_str):
        # Store the string representation of the unique ID of the BBS
        print(bbs_id_str)
        self.util.sid_data.chosen_bbs = bbs_id_str

        # Now you can emit the event with the string ID
        self.util.socketio.emit('set_chosen_bbs', {'chosen_bbs': self.sid_data.chosen_bbs})

        self.util.socketio.emit('getJWTToken', {'chosen_bbs': self.sid_data.chosen_bbs, 'sid': self.util.request_id }) 

    def login(self):
        
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
    def choose_bbs(self):
        self.sid_data.setBBSChooser(BBSChooser(self))
        self.sid_data.bbsChooser.draw_frame()
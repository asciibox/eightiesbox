from pymongo import MongoClient
from menubar import MenuBar

class MenuBarANSIEditor(MenuBar):
    def __init__(self, sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line):
        # Call the constructor of the parent class (MenuBar)
        super().__init__(sub_menus, sid_data, output_function, ask_function, mongo_client, goto_next_line, clear_screen, emit_gotoXY, clear_line)
        # Add any additional properties or methods specific to MenuBarANSI here
        

        # Add ANSI-specific methods here if needed
    def choose_field(self):
        if self.in_sub_menu:
            current_menu = self.current_main_menu_index
            selected_option = self.sub_menus[self.main_menu[self.current_main_menu_index]][self.current_sub_menu_indexes[current_menu]]
            if selected_option=="Load ANSI":
                self.load_ansi()
            elif selected_option=="Save ANSI":
                self.save_ansi()
            elif selected_option=="Leave menu bar":
                self.leave_menu_bar()                
            else:
                print("Hello world")
            # Perform the action associated with selected_option here.
        else:
            self.in_sub_menu = True
            self.draw_sub_menu()

    def leave_menu_bar(self):
        self.sid_data.setCurrentAction("wait_for_ansieditor")
        # self.sid_data.setANSIEditor(ANSIEditor(self.sid_data, self.output, self.ask, self.goto_next_line, self.clear_screen, self.emit_gotoXY, self.clear_line))
        self.sid_data.ansi_editor.clear_screen()
        self.sid_data.ansi_editor.update_first_line()
        self.sid_data.ansi_editor.display_editor()

    def load_ansi(self):
        print("ANSI")

    def save_ansi(self):
        print("ANSI")
from basicansi import BasicANSI
from usereditor import UserEditor
from ansieditor import ANSIEditor
from menu import Menu
from menubox import MenuBox

class AdminMenu(BasicANSI):
    def __init__(self, util, callback_on_exit):
        super().__init__(util)
        self.callback_on_exit = callback_on_exit
        self.util = util

    def start(self): 
        self.display_menu()

    def display_menu(self):
        self.util.clear_screen()
        self.util.sid_data.setStartX(0)
        self.util.sid_data.setStartY(0)

        menu_options = [
            "1. User editor",
            "2. ANSI editor",
            "3. Menu editor",
            "4. Oneliner editor",
            "5. BBS editor",
            "6. Logout",
            "X. Exit to main menu"
        ]

        for option in menu_options:
            self.util.output(option, 6, 0)
            self.util.goto_next_line()

        self.util.ask(1, self.process_choice)

    def process_choice(self, choice):
        choice = choice.lower()
        if choice == '1':
            self.util.sid_data.setUserEditor(UserEditor(self.util, self.display_menu))
        elif choice == '2':
            self.util.sid_data.setANSIEditor(ANSIEditor(self.util))
            self.util.sid_data.ansi_editor.start()
            self.util.sid_data.setCurrentAction("wait_for_ansieditor")
        elif choice == '3':
            self.sid_data.setMenu(Menu(self.util, [["" for _ in ['Type', 'Data', 'Key', 'Sec', 'Groups', 'HideOnSec']] for _ in range(50)], 50, None)) 
            self.sid_data.setMenuBox(MenuBox(self.util))
            # Implement Menu editor functionality
            pass
        elif choice == '4':
            # Implement Oneliner editor functionality
            pass
        elif choice == '5':
            # Implement BBS editor functionality
            pass
        elif choice == '6':
            self.util.clear_screen()
            self.util.emit_clear_cookie(self.sid_data.chosen_bbs)
            self.util.choose_bbs()
        elif choice == 'x':
             self.util.load_menu()
        else:
            self.util.output_wrap("Invalid choice. Please try again.", 6, 0)
            self.display_menu()

    def doNothing(self):
        pass  # Placeholder for any required callback that does nothing

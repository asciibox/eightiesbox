socketio = None  # Declare as a global variable

class SessionData:
    def __init__(self):
        self.accept_keys = []
        self.ansi_editor = None
        self.ansi_editor_values = [] # Todo remove and change two editors to one
        self.callback = None
        self.color_array = []  # Initialize an empty 2D array
        self.color_bgarray = []  # Initialize an empty 2D array
        self.current_action = None
        self.cursorX = 0
        self.cursorY = 0
        self.localinput = ""
        self.insert = False
        self.currentPos = 0
        self.maxLength = 0
        self.inputType = ''
        self.input_values = []
        self.map_character_set = False
        self.menu = None
        self.menu_bar = None
        self.menu_box = None
        self.menu_current_index = 0  # To keep track of the current selected menu item
        self.menu_items = []  # To hold the menu items
        self.menutexteditor = None
        self.sauceWidth = 80 # The loaded number of characters on the screen horizontally (effective editing width)
        self.sauceHeight = 25 # The loaded number of characters vertically in the sauce record (effective editing height)
        self.startX = 0
        self.startY = 0
        self.user_name = ""
        self.view_start = 0
        self.xWidth = 0 # The total characters on the screen horizontally
        self.yHeight = 0 # Those vertically

    def move_cursor_up(self):
        self.menu_current_index = (self.menu_current_index - 1) % len(self.menu_items)
        
    def move_cursor_down(self):
        self.menu_current_index = (self.menu_current_index + 1) % len(self.menu_items)
        
    def select_menu_item(self):
        selected_item = self.menu_items[self.menu_current_index]
        # Perform action for selected item

    def setXWidth(self, x):
        self.xWidth = x

    def setYHeight(self, y):
        self.yHeight = y

    def setSauceWidth(self, x):
        self.sauceWidth = x

    def setSauceHeight(self, y):
        self.sauceHeight = y

    # Setter methods
    def setCursorX(self, x):
        self.cursorX = x

    def setCursorY(self, y):
        self.cursorY = y

    def setStartX(self, x):
        self.startX = x

    def setStartY(self, y):
        self.startY = y

    def setLocalInput(self, input):
        self.localinput = input
        
    def setCurrentPos(self, pos):
        self.currentPos = pos

    def setMaxLength(self, length):
        self.maxLength = length

    def setCurrentAction(self, action):
        self.current_action = action

    def setInsert(self, insert):
        self.insert = insert

    def setCallback(self, callback):
        self.callback = callback

    def setInputType(self, inputType):
        self.inputType = inputType

    def setAcceptKeys(self, char_array):
        uppercase_char_array = []

        for char in char_array:
            uppercase_char_array.append(char.upper())
        self.accept_keys = uppercase_char_array

    def setMenuBox(self, menuBox):
        self.menu_box = menuBox

    def setUserName(self, username):
        self_user_name = username

    def setMenuTextEditor(self, menutexteditor):
        self.menutexteditor = menutexteditor

    def setMenuBar(self, menu_bar):
        self.menu_bar = menu_bar

    def setMapCharacterSet(self, value):
        self.map_character_set = value

    def setANSIEditor(self, value):
        self.ansi_editor = value

    def setViewStart(self, value):
        self.view_start = value

    def setMenu(self, value):
        self.menu = value
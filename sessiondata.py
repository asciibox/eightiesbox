socketio = None  # Declare as a global variable

class SessionData:
    def __init__(self):
        self.accept_keys = []
        self.ansi_editor = None
        self.ansi_editor_values = [] # Todo remove and change two editors to one
        self.callback = None
        self.color_array = []  # Initialize an empty 2D array
        self.color_bgarray = []  # Initialize an empty 2D array
        self.copy_color_array = []  # Initialize an empty 2D array
        self.copy_color_bgarray = []  # Initialize an empty 2D array
        self.current_file_area = None
        self.current_message_area = None
        self.currentPos = 0
        self.current_action = None
        self.cursorX = 0
        self.cursorY = 0
        self.file_area_menu = None
        self.insert = False
        self.localinput = ""
        self.maxLength = 0
        self.inputType = ''
        self.input_values = []
        self.chat_partner = None
        self.contacted_users = []
        self.copy_input_values = []
        self.copy_action = True
        self.current_chat_partner = ""
        self.chat_callback = None
        self.f10actionhandler = None
        self.incoming_requests = []
        self.last_activity_timestamp = None
        self.map_character_set = False
        self.multi_line_chat = None
        self.menu = None
        self.menu_bar = None
        self.menu_box = None
        self.menu_current_index = 0  # To keep track of the current selected menu item
        self.menu_items = []  # To hold the menu items
        self.menutexteditor = None
        self.message_area_menu = None
        self.message_editor = None
        self.message_area_change = None
        self.message_data = {}  # A local variable to save all input fields
        self.message_reader = None
        self.outgoing_requests = []
        self.previous_action = None
        self.remaining_time = 180*60  # 3 hours in minutes
        self.stored_time = 0  # Stored time in minutes
        self.sauceWidth = 80 # The loaded number of characters on the screen horizontally (effective editing width)
        self.sauceHeight = 25 # The loaded number of characters vertically in the sauce record (effective editing height)
        self.startX = 0
        self.startY = 0
        self.user_document = None # Holds all user data, id, name and security level (user_level)
        self.user_editor = None
        self.user_name = ""
        self.user_picker = None
        self.upload_token = ''
        self.upload_editor = None
        self.util = None
        self.view_start = 0
        self.who_is_online = None
        self.xWidth = 0 # The total characters on the screen horizontally
        self.yHeight = 0 # Those vertically
        self.download = None
        self.edit_file = None
        self.delete_file = None
        self.status_bar_paused = False
        self.bbschooser = None
        self.max_scroll_length = 35
        self.screen_data_list = []
        self.watchlines = None
        self.last_emitted_index = -1
        self.clear_command_issued = False
        self.group_editor = None
        self.group_chooser = None
        self.profile_renderer = None
        self.renderer = None
        self.callbacks = {}
    
        

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
        print("action set to "+action)
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
        self.user_name = username

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

    def setMessageAreaMenu(self, value):
        self.message_area_menu = value
    
    def setUserEditor(self, value):
        self.user_editor = value

    def setFileAreaMenu(self, value):
        self.file_area_menu = value

    def setMessageEditor(self, value):
        self.message_editor = value

    def setMessageAreaChange(self, value):
        self.message_area_change = value

    def setFileAreaChange(self, value):
        self.file_area_change = value

    def setCurrentMessageArea(self, value):
        self.current_message_area = value

    def setCurrentFileArea(self, value):
        self.current_file_area = value

    def SetMessageData(self, value):
        self.message_data = value

    def setMessageReader(self, value):
        self.message_reader = value

    def setWhoIsOnline(self, value):
        self.who_is_online = value

    def setMultilineChat(self, value):
        self.multi_line_chat = value

    def setF10ActionHandler(self, value):
        self.f10actionhandler = value

    def setChatCallback(self, value):
        self.chat_callback = value

    def setUploadToken(self, value):
        self.upload_token = value
    
    def setUploadEditor(self, value):
        self.upload_editor = value

    def setFilelist(self, value):
        self.filelist = value

    def setDownload(self, value):
        self.download = value

    def setEditFile(self, value):
        self.edit_file = value

    def setDeletefile(self, value):
        self.delete_file = value

    def setBBSChooser(self, value):
        self.bbschooser = value

    def setMaxScrollLength(self, value):
        self.max_scroll_length = value

    def setGroupChooser(self, value):
        self.group_chooser = value
    
    def setProfileRenderer(self, value):
        self.profile_renderer = value

    def setRenderer(self, value):
        self.renderer = value

    def store_screen_data(self, ascii_codes=None, currentColor=None, backgroundColor=None, blink=None, x=None, y=None, command=None):
        screen_data = {
            'ascii_codes': ascii_codes,
            'currentColor': currentColor,
            'backgroundColor': backgroundColor,
            'blink': blink,
            'x': x,
            'y': y,
            'command': command  # New field to handle special commands like 'clear'
        }
        self.screen_data_list.append(screen_data)

    def setWatchLines(self, watchlines):
        self.watchlines = watchlines

    def setGroupEditor(self, value):
        self.group_editor = value

    def get_callback(self, callback_name):
        """ Retrieve a callback function and its parameter by its name. """
        return self.callbacks.get(callback_name, None)
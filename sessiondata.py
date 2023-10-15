socketio = None  # Declare as a global variable

class SessionData:
    def __init__(self):
        self.current_action = None
        self.startX = 0
        self.startY = 0
        self.cursorX = 0
        self.cursorY = 0
        self.localinput = ""
        self.insert = False
        self.currentPos = 0
        self.maxLength = 0
        self.callback = None
        self.inputType = ''
        self.accept_keys = []
        self.menu_current_index = 0  # To keep track of the current selected menu item
        self.menu_items = []  # To hold the menu items
        self.menu_box = None
        self.menutexteditor = None
        self.ansi_editor = None
        self.xWidth = 0
        self.yHeight = 0
        self.user_name = ""
        self.menu_bar = None
        self.input_values = []
        self.map_character_set = False
        self.color_array = []  # Initialize an empty 2D array
        self.color_bgarray = []  # Initialize an empty 2D array
        self.ansi_editor_values = [] # Todo remove and change two editors to one
        self.list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
        self.list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,223,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]
        target_values = [223, 176, 177, 178, 220]
        for i, value in enumerate(self.list2):
            if value in target_values:
                self.list2[i] = -1
    
        self.list1.append(220)
        self.list2.append(223)


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

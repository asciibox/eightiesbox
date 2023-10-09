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
        print("Set localinput to "+self.localinput)
        
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
        print("Assigned ")
        print(uppercase_char_array)
        self.accept_keys = uppercase_char_array

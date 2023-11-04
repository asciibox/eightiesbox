from ansieditor import *

class UploadEditor(ANSIEditor):
    def __init__(self, util):
        super().__init__(util)
        self.util.sid_data.color_array=[]
        self.util.sid_data.color_bgarray=[]
        self.util.sid_data.input_values=[]
        self.start()

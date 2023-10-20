class Sauce:
    def __init__(self, columns=0, rows=0, title="", author="", group="", date="", filesize=0,
                 ice_colors=False, use_9px_font=False, font_name="", comments=""):
        self.columns = columns
        self.rows = rows
        self.title = title
        self.author = author
        self.group = group
        self.date = date
        self.filesize = filesize
        self.ice_colors = ice_colors
        self.use_9px_font = use_9px_font
        self.font_name = font_name
        self.comments = comments
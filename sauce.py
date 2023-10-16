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

def get_sauce(bytes):
    if len(bytes) >= 128:
        sauce_bytes = bytes[-128:]
        if sauce_bytes[:7].decode("utf-8") == "SAUCE00":
            title = sauce_bytes[7:42].decode("utf-8").rstrip('\0')
            author = sauce_bytes[42:62].decode("utf-8").rstrip('\0')
            group = sauce_bytes[62:82].decode("utf-8").rstrip('\0')
            date = sauce_bytes[82:90].decode("utf-8").rstrip('\0')
            filesize = int.from_bytes(sauce_bytes[90:94], byteorder='little')
            datatype = sauce_bytes[94]
            if datatype == 5:
                columns = sauce_bytes[95] * 2
                rows = filesize // (columns * 2)
            else:
                columns = int.from_bytes(sauce_bytes[96:98], byteorder='little')
                rows = int.from_bytes(sauce_bytes[98:100], byteorder='little')
            number_of_comments = sauce_bytes[104]
            rawcomments = sauce_bytes[-(number_of_comments * 64 + 128):-128].decode("utf-8")
            comments = '\n'.join([rawcomments[i*64:(i+1)*64].rstrip('\0') for i in range(number_of_comments)])
            flags = sauce_bytes[105]
            ice_colors = (flags & 0x01) == 1
            use_9px_font = (flags >> 1 & 0x02) == 2
            font_name = sauce_bytes[106:128].decode("utf-8").replace('\0', "")
            font_name = "IBM VGA" if font_name == "" else font_name
            if filesize == 0:
                filesize = len(bytes) - 128
                if number_of_comments:
                    filesize -= number_of_comments * 64 + 5
            return Sauce(columns, rows, title, author, group, date, filesize, ice_colors, use_9px_font, font_name, comments)
    sauce = Sauce()
    sauce.filesize = len(bytes)
    return sauce

def append_sauce_to_string(sauce, string):
    sauce_bytes = bytearray(128)  # Initialize a byte array of length 128 for the SAUCE record

    # Populate the SAUCE record byte array with the values from the Sauce object
    sauce_bytes[0:7] = b'SAUCE00'
    sauce_bytes[7:42] = sauce.title.encode('utf-8').ljust(35, b'\0')
    sauce_bytes[42:62] = sauce.author.encode('utf-8').ljust(20, b'\0')
    sauce_bytes[62:82] = sauce.group.encode('utf-8').ljust(20, b'\0')
    sauce_bytes[82:90] = sauce.date.encode('utf-8').ljust(8, b'\0')
    sauce_bytes[90:94] = sauce.filesize.to_bytes(4, byteorder='little')
    # Assume datatype 5 for binary files, adjust as necessary
    if sauce.columns and sauce.rows:
        sauce_bytes[94] = 5
        sauce_bytes[95] = sauce.columns // 2
        # Compute filesize based on columns and rows if it's not provided
        sauce_bytes[90:94] = (sauce.columns * sauce.rows * 2).to_bytes(4, byteorder='little')
    else:
        # For other datatypes, you might want to set the appropriate datatype value and file type
        pass  # Replace with your logic for other datatypes

    # Assume no comments, ice_colors or use_9px_font for simplicity
    # You can add logic to handle these fields if they are relevant to your use case

    # Convert the SAUCE record byte array to a string
    sauce_string = sauce_bytes.decode('latin-1')  # latin-1 encoding will preserve the byte values
    
    if string[-128:-121] == 'SAUCE00':
        # Replace the existing SAUCE record
        string = string[:-128] + sauce_string
    else:
        # Append the SAUCE record
        string += sauce_string
    
    return string

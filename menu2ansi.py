import os

ESC = "\u001B["
OSC = "\u001B]"
BEL = "\u0007"
SEP = ";"

isBrowser = False  # Not applicable for a Python script
isTerminalApp = False  # Detecting Terminal.app is non-trivial in Python
isWindows = os.name == 'nt'

def cursor_to(x, y=None):
    if y is None:
        return f"{ESC}{x + 1}G"
    return f"{ESC}{y + 1}{SEP}{x + 1}H"

def cursor_move(x, y):
    codes = []
    if x < 0:
        codes.append(f"{ESC}{-x}D")
    elif x > 0:
        codes.append(f"{ESC}{x}C")

    if y < 0:
        codes.append(f"{ESC}{-y}A")
    elif y > 0:
        codes.append(f"{ESC}{y}B")
    return "".join(codes)

def cursor_up(count=1):
    return f"{ESC}{count}A"

def cursor_down(count=1):
    return f"{ESC}{count}B"

def cursor_forward(count=1):
    return f"{ESC}{count}C"

def cursor_backward(count=1):
    return f"{ESC}{count}D"

def cursor_left():
    return f"{ESC}G"

def cursor_save_position():
    return f"{ESC}s" if not isTerminalApp else "\u001B7"

def cursor_restore_position():
    return f"{ESC}u" if not isTerminalApp else "\u001B8"

def cursor_get_position():
    return f"{ESC}6n"

def cursor_next_line():
    return f"{ESC}E"

def cursor_prev_line():
    return f"{ESC}F"

def cursor_hide():
    return f"{ESC}?25l"

def cursor_show():
    return f"{ESC}?25h"

def erase_lines(count):
    return "".join([f"{ESC}2K{ESC}1A" for _ in range(count - 1)]) + f"{ESC}2K"

def erase_end_line():
    return f"{ESC}K"

def erase_start_line():
    return f"{ESC}1K"

def erase_line():
    return f"{ESC}2K"

def erase_down():
    return f"{ESC}J"

def erase_up():
    return f"{ESC}1J"

def erase_screen():
    return f"{ESC}2J"

# Define ANSI escape codes
def wrap_ansi16(offset=0):
    return lambda code: f"\033[{code + offset}m"

def wrap_ansi256(offset=0):
    return lambda code: f"\033[{38 + offset};5;{code}m"

def wrap_ansi16m(offset=0):
    return lambda red, green, blue: f"\033[{38 + offset};2;{red};{green};{blue}m"

# Helper functions
def rgb_to_ansi256(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return int(((r - 8) / 247) * 24) + 232
    return 16 + (36 * int(r / 255 * 5)) + (6 * int(g / 255 * 5)) + int(b / 255 * 5)

def hex_to_rgb(hex_val):
    hex_val = hex_val.lstrip("#")
    return tuple(int(hex_val[i:i+2], 16) for i in (0, 2, 4))

def hex_to_ansi256(hex_val):
    return rgb_to_ansi256(*hex_to_rgb(hex_val))

# Define styles
styles = {
    'modifier': {
        'reset': [0, 0],
        'bold': [1, 22],
        'dim': [2, 22],
        'italic': [3, 23],
        'underline': [4, 24],
        'overline': [53, 55],
        'inverse': [7, 27],
        'hidden': [8, 28],
        'strikethrough': [9, 29]
    },
    'color': {
        'black': [30, 39],
        'red': [31, 39],
        'green': [32, 39],
        'yellow': [33, 39],
        'blue': [34, 39],
        'magenta': [35, 39],
        'cyan': [36, 39],
        'white': [37, 39],
        'black_Bright': [90, 39],
        'red_bright': [91, 39],
        'green_bright': [92, 39],
        'yellow_bright': [93, 39],
        'blue_bright': [94, 39],
        'magenta_bright': [95, 39],
        'cyan_bright': [96, 39],
        'white_bright': [97, 39],
        'gray': [90, 39],
        'grey': [90, 39],
        'ansi': wrap_ansi16(),
        'ansi256': wrap_ansi256(),
        'ansi16m': wrap_ansi16m()
    },
    'bg_color': {
        'bg_black': [40, 49],
        'bg_red': [41, 49],
        'bg_green': [42, 49],
        'bg_yellow': [43, 49],
        'bg_blue': [44, 49],
        'bg_magenta': [45, 49],
        'bg_cyan': [46, 49],
        'bg_white': [47, 49],
        'bg_black_bright': [100, 49],
        'bg_red_bright': [101, 49],
        'bg_green_bright': [102, 49],
        'bg_yellow_bright': [103, 49],
        'bg_blue_bright': [104, 49],
        'bg_magenta_bright': [105, 49],
        'bg_cyan_bright': [106, 49],
        'bg_white_bright': [107, 49],
        'bg_gray': [100, 49],
        'bg_grey': [100, 49],
        'bg_ansi': wrap_ansi16(10),
        'bg_ansi256': wrap_ansi256(10),
        'bg_ansi16m': wrap_ansi16m(10)
    }
}

# Generate the styles for Python
def assemble_styles():
    for group_name, group in styles.items():
        for style_name, style in group.items():
            if isinstance(style, list):
                group[style_name] = {
                    'open': f"\033[{style[0]}m",
                    'close': f"\033[{style[1]}m"
                }

# Initialize the styles
assemble_styles()

# To call the foreground and background colors
def colorize_text(text, fg_color, bg_color):
    fg = styles['color'].get(fg_color, {}).get('open', '') if isinstance(styles['color'].get(fg_color, {}), dict) else styles['color'].get(fg_color, '')('')
    bg = styles['bg_color'].get(bg_color, {}).get('open', '') if isinstance(styles['bg_color'].get(bg_color, {}), dict) else styles['bg_color'].get(bg_color, '')('')
    reset = styles['modifier']['reset']['close']

    return f"{fg}{bg}{text}{reset}"

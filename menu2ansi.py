import os

ESC = "\033["  # or "\x1B["
OSC = "\033]"  # or "\x1B]"
BEL = "\007"   # or "\x07"
SEP = ";"

isBrowser = False  # Not applicable for a Python script
isTerminalApp = False  # Detecting Terminal.app is non-trivial in Python
isWindows = os.name == 'nt'

def cursor_to(x, y=None):
    reset_sequence = f"{ESC}0m"  # ANSI reset sequence
    if y is None:
        return reset_sequence + f"{ESC}{x + 1}G"
    return reset_sequence + f"{ESC}{y + 1}{SEP}{x + 1}H"


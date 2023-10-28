import codecs
from stransi import Ansi

# Load the ANSI file with cp437 encoding
with codecs.open("ansi/welcome-120x70.ANS", "r", encoding="cp437") as f:
    text_content = f.read()

    # Filter out the specific ANSI escape code
filtered_content = text_content.replace("[?7h", "")

text = Ansi(filtered_content)

instructions = list(text.instructions())

print(instructions)
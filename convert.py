import base64

def base64_to_ansi(base64_file_path, ansi_file_path):
    try:
        # Read the base64 encoded file
        with open(base64_file_path, "r") as base64_file:
            base64_data = base64_file.read()

        # Decode the base64 data to ANSI (assuming the base64 encoded data is ANSI text)
        print("x1")
        ansi_data = base64.b64decode(base64_data);
        print("x2")
        ansi_data = convert_current_string(ansi_data)
        print(ansi_data)
        ansi_data = ansi_data.decode('cp1252')
        print("x3")
        # Write the ANSI data to a new file
        with open(ansi_file_path, "w", encoding='cp1252') as ansi_file:
            ansi_file.write(ansi_data)

        print(f"Successfully converted {base64_file_path} to {ansi_file_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

def map_value(value, list1, list2):
    try:
        index = list1.index(value)
        return list2[index]
    except ValueError:
        return value  # returns the original value if not found in list1
    except IndexError:
        print(f"Index out of range in list2 for value {value}")
        return value  # returns the original value if index out of range in list2
    
def convert_current_string(currentBytes):

    list1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 13, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255]
    list2 = [0,1,2,3,4,5,6,7,8,9,13,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,225,237,243,250,241,209,170,186,191,8976,172,189,188,161,171,187,9617,9618,9619,9474,9508,9569,9570,9558,9557,9571,9553,9559,9565,9564,9563,9488,9492,9524,9516,9500,9472,9532,9566,9567,9562,9556,9577,9574,9568,9552,9580,9575,9576,9572,9573,9561,9560,9554,9555,9579,9578,9496,9484,9608,9604,9612,9616,9600,945,-1,915,960,931,963,181,964,934,920,937,948,8734,966,949,8745,8801,177,8805,8804,8992,8993,247,8776,176,8729,183,8730,8319,178,9632,160]

    if currentBytes:
        ascii_codes = [b for b in currentBytes]

        mapped_ascii_codes = [map_value(code, list2, list1) for code in ascii_codes]

        # Convert the mapped ASCII codes back into a byte array
        new_bytes = bytes(mapped_ascii_codes)

        return new_bytes
    return bytes([])  # Return an empty byte array if there's no data
# Usage
base64_to_ansi("base64.txt", "output.ans")
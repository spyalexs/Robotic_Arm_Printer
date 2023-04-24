#load in the gcode file as an array of gcode lines

import os


def Load_GCode(filename):
    #leave of .gcode when naming the file

    #find gcode file
    path_to_parts = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Test_Parts")
    path_to_file = os.path.join(path_to_parts, filename, str(filename + ".gcode"))
    print(str("Loading: " + path_to_file))

    #open gcode file
    file = open(path_to_file, 'r')
    gcode_raw = file.read()

    #seperate into lines
    lines_raw = gcode_raw.split('\n')

    #remove comments from file
    lines = []
    for line in lines_raw:
        if len(line) > 1:
            if line[0] != ';':
                lines.append(line)

    return lines

if __name__ == "__main__":
    Load_GCode("Test_Part_1")

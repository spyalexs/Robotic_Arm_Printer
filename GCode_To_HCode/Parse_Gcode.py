from Load_Gcode import Load_GCode 

def Parse_Gcode(lines):
    #give lines from loaded gcode
    #returns succes state and an array of points if succes for

    location_lines = []

    #look for trouble lines - if present fail
    #these include anyline to indicate a positional set on any axis other than the extruder and relative positioning
    #look for tool changes
    #also look for arc motion lines - not supported
    for line in lines:
        #get command name
        components = line.split(" ")
        line_name = components[0]

        if(line[0] == "T" and line_name != "T0"):
            print("Tool change detected, failing!")
            return False, None
        
        if line_name == "G92":

    
    print("Success")


if __name__ == "__main__":
    lines = Load_GCode("Test_Part_1")
    Parse_Gcode(lines)

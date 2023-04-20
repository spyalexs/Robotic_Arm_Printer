from Load_Gcode import Load_GCode 
from HCode_Point import HCodePoint

def Parse_Gcode(lines):
    #give lines from loaded gcode
    #returns succes state and an array of points if succes for

    location_lines = []

    #look for trouble lines - if present fail
    #these include anyline to indicate a positional set on any axis other than the extruder and relative positioning
    #look for tool changes
    #also look for arc motion lines - not supported
    points = []
    previous_x = 0
    previous_y = 0
    previous_z = 0


    for line in lines:
        #get command name
        components = line.split(" ")
        line_name = components[0]

        if(line[0] == "T" and line_name != "T0"):
            print("Tool change detected, failing!")
            return False, None
        if line_name == "G92":
            if("X" in line or "Y" in line or "Z" in line):
                print("Resetting Key Axis detected, failing!")
                return False, None
        if line_name == "G91":
            print("Relative Mode Detected, Not Supported, Failing!")
            return False, None
        if line_name == "G2" or line_name == "G3":
            print("Arc Detected, Not Supported, Failing")
            return False, None
        
        #get known points all with x,y,z
        if line_name == "G1" or line_name == "G0":
            
            #get all movement data from line
            for component in components:
                if "X" in component:
                    previous_x = float(component[1:])                
                if "Y" in component:
                    previous_y = float(component[1:])                
                if "Z" in component:
                    previous_z = float(component[1:])

            #add a point with the updated data 
            points.append(HCodePoint(previous_x, previous_y, previous_z))
    
    print(len(points))
        


if __name__ == "__main__":
    lines = Load_GCode("Test_Part_1")
    Parse_Gcode(lines)

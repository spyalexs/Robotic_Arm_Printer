import os
import HCode_Point

def WriteHcode(points, filename):
    good_name = False
    counter = 0
    file = None

    while good_name == False:
        real_filename = filename
        if counter != 0:
            real_filename = f"{filename}{str(counter)}"

        #check to make sure no other file exists
        path_to_parts = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "Test_Parts")
        path_to_file = os.path.join(path_to_parts, filename, str(real_filename + ".hcode"))

        if not os.path.isfile(path_to_file):
            good_name = True
            
            file = open(path_to_file, 'w')

        counter += 1

    # write all the points
    for point in points:
        file.write(str(point.angles[0]) + " " + 
                   str(point.angles[1]) + " "  + 
                   str(point.angles[2]) + " " + 
                   str(point.angles[3]) + " " + 
                   str(point.angles[4]) + " " + 
                   str(point.angles[5]) + "#location#" +
                    str(point.location[0]) + " " +  
                    str(point.location[1]) + " " +  
                    str(point.location[2]) + " " +  
                    str(point.location[3]) + " " +  
                    str(point.location[4]) + " " +  
                    str(point.location[5]) + "\n")

    file.close()

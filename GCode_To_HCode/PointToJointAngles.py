import numpy as np
import math
#pseudo code for Ikin solver


#load screw axis

#compute overhead - G and S terms

#try base theta angles - from last point
#   get distance

#newton-raphson to find next point -- should naturally converdge to point on path -- if I discretize hard enought my path will be close enought
    #retry to tolerance - determined by cost function - convergence to point
    #points should be like a tenth of a mm apart

def defineArm():
    #define a list of the screw axis and the home matrix for the arm
    s1 = np.array([0,1,0,0,0,0]) #joint 1 screw
    s2 = np.array([0,0,1,5,0,0]) #joint 2 screw    
    s3 = np.array([0,0,1,15,0,0]) #joint 3 screw
    s4 = np.array([0,0,1,23,0,0]) #joint 4 screw    
    s5 = np.array([0,1,0,0,0,0]) #joint 5 screw
    s6 = np.array([0,0,1,30,0,0]) #joint 6 screw

    home_matrix = np.transpose(np.array([np.array([1,0,0,0]),np.array([0,1,0,0]),np.array([0,0,1,0]),np.array([0,35,0,1])]))

    return np.array([s1,s2,s3,s4,s5,s6]), home_matrix

def runIkin(ScrewList, HomeMatrix, Approx):
    #Input: 
        #ScrewList - a 6 by 6 matrix containing the screw joints that define arm motion
        #HomeMatrix - a transformation matrix to the "home" location of the robot
    print("Hello")

def getPositionFromAngles(ScrewList, HomeMatrix, Angles):
    if len(Angles) != len(ScrewList):
        print("Angle Screw List Miss-Match... Failing")
        return
    
    #create skew symetric matrix
    def skewify(wx, wy, wz):
        return np.transpose(np.array([[0,-wz, wy],[wz,0,-wx],[-wy,wx,0]]))

    counter = 0
    trans_list = [] # list for transformation matrices
    rolling_transform = np.eye(4) # all transforms multiplied together
    for axis in ScrewList:
        skew = skewify(axis[0], axis[1], axis[2])

        #calculate transform from matrix exponential
        rot = np.add(np.add(np.eye(3), np.multiply(math.sin(Angles[counter]), skew)), np.multiply((1 - math.cos(Angles[counter])),np.matmul(skew, skew))) #rodrigues therom
        g = np.add(np.multiply(Angles[counter], np.eye(3)), np.add(np.multiply((1 - math.cos(Angles[counter])), skew), np.multiply((Angles[counter] - math.sin(Angles[counter])), np.matmul(skew, skew))))
        gv = np.matmul(g, axis[3:])
        transform = np.transpose(np.array([[rot[0][0],rot[0][1], rot[0][2], 0],[rot[1][0],rot[1][1], rot[1][2], 0],[rot[2][0],rot[2][1], rot[2][2], 0],[gv[0], gv[1], gv[2], 1]]))
        
        #store for later use
        trans_list.append(transform)
        rolling_transform = np.matmul(rolling_transform, transform)

        counter += 1

    rolling_transform = np.matmul(rolling_transform, HomeMatrix)

        
    
    

if __name__ == "__main__":
    Screwlist, home = defineArm()
    getPositionFromAngles(Screwlist, home, np.array([0,0,0,0,0,math.pi/2]))

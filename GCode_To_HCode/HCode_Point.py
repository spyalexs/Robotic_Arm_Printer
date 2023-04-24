from PointToJointAngles import runIKin, runFKin
import numpy as np
import math

class HCodePoint:
    #basic struct for a point, allows room for more data later

    x = 0
    y = 0
    z = 0

    angles = []
    location = []

    movement_time = 1

    def __init__ (self, X, Y, Z, previous_angles, arm_screw_list, arm_home, previous_time):
        #covert to new orgin
        self.x, self.y, self.z = self.transformPosition(X,Y,Z)

        #get the angles
        self.angles, self.location = runIKin(arm_screw_list, arm_home, np.array([3.1415,0,0, self.x,self.y,self.z]), previous_angles)

        #calculate movement time
        self.getMoveTime(arm_screw_list, arm_home, previous_angles, previous_time)

    def transformPosition(self, X, Y, Z):
        mm_per_in = 25.4
        
        #steps to inches...
        x = X / mm_per_in
        y = Z / mm_per_in
        z = Y / mm_per_in

        #new orgin for the sake of Ikin
        x = x + 4
        y = y 
        z = z + 4
        return x, y, z
    
    def getMoveTime(self, arm_screw_list, arm_home, previous_angles, previous_time):
        #the time is rolling from the first motion
        #find the time the movement will take from the previous point to this one

        movement_rate = 3 #in per sec

        previous_position = runFKin(arm_screw_list, arm_home, previous_angles)
        
        dist = math.sqrt((self.x - previous_position[3])**2 + (self.y - previous_position[4])**2 + (self.z - previous_position[5])**2)
        self.movement_time = dist / movement_rate + previous_time


        



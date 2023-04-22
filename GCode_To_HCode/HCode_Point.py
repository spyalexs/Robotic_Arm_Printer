from PointToJointAngles import runIKin
import numpy as np
import math

class HCodePoint:
    #basic struct for a point, allows room for more data later

    x = 0
    y = 0
    z = 0

    angles = []
    location = []

    def __init__ (self, X, Y, Z, previous_angles, arm_screw_list, arm_home):
        #covert to new orgin
        self.x, self.y, self.z = self.transformPosition(X,Y,Z)

        #get the angles
        self.angles, self.location = runIKin(arm_screw_list, arm_home, np.array([3.1415,0,0, self.x,self.y,self.z]), previous_angles)

    def transformPosition(self, X, Y, Z):
        mm_per_in = 25.4
        
        #steps to inches...
        x = X / mm_per_in
        y = Z / mm_per_in
        z = Y / mm_per_in

        #new orgin for the sake of Ikin
        x = x + 4
        y = y + 6
        z = z + 4
        return x, y, z

        



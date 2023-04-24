import numpy as np
from scipy.spatial.transform import Rotation as SciRot
import math
from random import random
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

    home_matrix = np.transpose(np.array([np.array([1,0,0,0]),
                                         np.array([0,1,0,0]),
                                         np.array([0,0,1,0]),
                                         np.array([0,35,0,1])]))

    return np.array([s1,s2,s3,s4,s5,s6]), home_matrix

def runFKin(ScrewList, HomeMatrix, Angles):
    if len(Angles) != len(ScrewList):
        print("Angle Screw List Miss-Match... Failing")
        return
    
    #create skew symetric matrix
    def skewify(wx, wy, wz):
        return np.array([[0,-wz, wy],[wz,0,-wx],[-wy,wx,0]])

    counter = 0
    trans_list = [] # list for transformation matrices
    rolling_transform = np.eye(4) # all transforms multiplied together
    for axis in ScrewList:
        skew = skewify(axis[0], axis[1], axis[2])

        #calculate transform from matrix exponential
        rot = np.add(np.add(np.eye(3), np.multiply(math.sin(Angles[counter]), skew)), np.multiply((1 - math.cos(Angles[counter])),np.matmul(skew, skew))) #rodrigues therom
        g = np.add(np.multiply(Angles[counter], np.eye(3)), np.add(np.multiply((1 - math.cos(Angles[counter])), skew), np.multiply((Angles[counter] - math.sin(Angles[counter])), np.matmul(skew, skew))))
        gv = np.matmul(g, axis[3:])
        transform = np.array([[rot[0][0],rot[0][1], rot[0][2], gv[0]],
                    [rot[1][0],rot[1][1], rot[1][2], gv[1]],
                    [rot[2][0],rot[2][1], rot[2][2], gv[2]],
                    [0,0,0,1]])
        
        rolling_transform = np.matmul(rolling_transform, transform)
        #print(rolling_transform)


        counter += 1

    rolling_transform = np.matmul(rolling_transform, HomeMatrix)  

    #get euler from transform
    euler = SciRot.from_matrix(rolling_transform[:3,:3]).as_euler("xyz", degrees=False)

    return [euler[0], euler[1], euler[2], rolling_transform[0][3],rolling_transform[1][3],rolling_transform[2][3]]
    
def getJacobians(ScrewList, Angles):

    if len(Angles) != len(ScrewList):
        print("Angle Screw List Miss-Match... Failing")
        return
    
    #create skew symetric matrix
    def skewify(wx, wy, wz):
        return (np.array([[0,-wz, wy],[wz,0,-wx],[-wy,wx,0]]))

    rolling_transform = np.eye(4)
    space_jacobian_transpose = [] # this is intially transposed -- fix after all terms are addded
    counter = 0
    rolling_adjoint_map = np.eye(6) # the transform between the current axis and the spce frame
    adjoint_list = []
    for axis in ScrewList:
        #calculate jacobian column
        space_jacobian_transpose.append(np.matmul(rolling_adjoint_map, axis))
        adjoint_list.append(rolling_adjoint_map)

        skew = skewify(axis[0], axis[1], axis[2])

        #calculate adjoint from matrix exponential
        rot = np.add(np.add(np.eye(3), np.multiply(math.sin(Angles[counter]), skew)), np.multiply((1 - math.cos(Angles[counter])),np.matmul(skew, skew))) #rodrigues therom
        g = np.add(np.multiply(Angles[counter], np.eye(3)), np.add(np.multiply((1 - math.cos(Angles[counter])), skew), np.multiply((Angles[counter] - math.sin(Angles[counter])), np.matmul(skew, skew))))
        gv = np.matmul(g, axis[3:])
        transform = np.array([[rot[0][0],rot[0][1], rot[0][2], gv[0]],
                    [rot[1][0],rot[1][1], rot[1][2], gv[1]],
                    [rot[2][0],rot[2][1], rot[2][2], gv[2]],
                    [0,0,0,1]])
        
        rolling_transform = np.matmul(rolling_transform, transform)

        psb_skew = skewify(rolling_transform[0][3], rolling_transform[1][3], rolling_transform[2][3])
        rot_psb = np.matmul(psb_skew, rot)
        adjoint_map = np.array([[rot[0][0],rot[0][1], rot[0][2], 0,0,0],
                               [rot[1][0],rot[1][1], rot[1][2], 0,0,0],
                               [rot[2][0],rot[2][1], rot[2][2], 0,0,0],
                               [rot_psb[0][0], rot_psb[0][1], rot_psb[0][2], rot[0][0],rot[0][1], rot[0][2]],
                               [rot_psb[1][0], rot_psb[1][1], rot_psb[1][2], rot[1][0],rot[1][1], rot[1][2]],
                               [rot_psb[2][0], rot_psb[2][1], rot_psb[2][2], rot[2][0],rot[2][1], rot[2][2]]])
        
        rolling_adjoint_map = np.matmul(rolling_adjoint_map, adjoint_map)
        
        counter +=1

    # #go through the adjoints to backwork body jacobain
    # adjoint_list.remove(0)
    # adjoint_list.append(np.eye(6))
    # counter = 0
    # for adjoint in adjoint_list:
    #     #joint to ee
    #     rolling_adjoint_map = np.matmul(np.linalg.inv(adjoint), rolling_adjoint_map)


    #     counter +=1
          
  


    #actual space jacobian
    space_jacobian = np.transpose(np.array(space_jacobian_transpose))
    body_jacobian = np.matmul(np.linalg.inv(rolling_adjoint_map), space_jacobian)
    
    return space_jacobian, body_jacobian

def runIKin(ScrewList, HomeMatrix, target, guess):
    #ensure the target it a np matrix
    target = np.array(target)

    def findApproximationError(cp, tp):
        rw = 1
        pw = 1
        yw = 1

        Xw = 1
        Yw = 1
        Zw = 1

        return math.sqrt(rw*(cp[0]-tp[0])**2 + pw*(cp[1]-tp[1])**2 + yw*(cp[2]-tp[2])**2 + Xw*(cp[3]-tp[3])**2 + Yw*(cp[4]-tp[4])**2 + Zw*(cp[5]-tp[5])**2)

    tol = 1e-6
    counter = 0
    current_guess = guess
    running_error = 100000
    solved = False

    #run till position solved
    while solved == False:   
        counter = 0
 
        while running_error > tol: # run till tolerance is met

            #compute the difference in position from the current guess
            current_position = np.array(runFKin(ScrewList, HomeMatrix, current_guess))
            difference = target - current_position

            #get the jacobians
            js, jb = getJacobians(ScrewList, current_guess)

            delta_theta = np.matmul(np.linalg.pinv(js), (difference))

            current_guess = current_guess + delta_theta

            #normalize current guess
            inner_counter = 0
            while inner_counter < len(current_guess):
                current_guess[inner_counter] = current_guess[inner_counter] % (math.pi * 2)
                inner_counter += 1

            running_error = findApproximationError(current_position, target)
            counter += 1

            #timeout if not converging
            if counter > 150:
                break

        if(running_error < tol):
            angles_limit = 2 * math.pi /3 # rotation limit on angles
            
            solved = True

            if (current_guess[1] > angles_limit and current_guess[1] < math.pi * 2 - angles_limit):
                solved = False
                current_guess = np.array([random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi])

            if (current_guess[2] > angles_limit and current_guess[2] < math.pi * 2 - angles_limit):
                solved = False   
                current_guess = np.array([random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi])
         
            if (current_guess[3] > angles_limit and current_guess[3] < math.pi * 2 - angles_limit):
                solved = False              
                current_guess = np.array([random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi])
         
            if (current_guess[5] > angles_limit and current_guess[5] < math.pi * 2 - angles_limit):
                solved = False
                current_guess = np.array([random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi])

        else:
            #print(running_error)
            current_guess = np.array([random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi,random() * 2 * math.pi, random() * 2 * math.pi])
        
    print(current_guess)


    return current_guess, runFKin(ScrewList, HomeMatrix, current_guess)

if __name__ == "__main__":
    Screwlist, home = defineArm()
    g, p = runIKin(Screwlist, home, [math.pi,0,0,5,10,5], np.array([.1,.2,.3,.5,.4,.1]))
    print(p)


import os
from threading import Thread
from ament_index_python.packages import get_package_share_directory
from time import sleep

def launchGazebo():
    #creates Thread to run gazebo
    gazebo_thread = Thread(target=babysitGazebo, name="gazebo_thread")
    gazebo_thread.start()

def babysitGazebo():
    #runs gazebo
    WORLD_PATH = os.path.join(get_package_share_directory('arm_sim'), 'world.sdf')
    os.system(f'gz sim {WORLD_PATH}')

    while (True):
        sleep(10)

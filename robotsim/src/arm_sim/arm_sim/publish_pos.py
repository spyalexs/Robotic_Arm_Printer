import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.time import Time

from ament_index_python.packages import get_package_share_directory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import os
import time
import math

class posePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.posPub = self.create_publisher(JointTrajectory, '/model/printerArm/joint_trajectory', qos_profile_system_default)
        self.startTime = 0
        time.sleep(1)
        self.followPoints()

    def followPoints(self):
        points = []
        f = open(os.path.join(get_package_share_directory('arm_sim'), 'Test_Part_1.hcode'))
        out_msg = JointTrajectory()
        out_msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        for line in f:
            jointPos = JointTrajectoryPoint()
            jointPos.positions = [float(i) % (2 * math.pi) for i in line[0:line.index('#')].split()]
            timeToPos = float(line[line.index('#time#') + 6:])
            jointPos.time_from_start.sec = int(timeToPos)
            jointPos.time_from_start.nanosec = int(100000000 * (timeToPos % 1))
            points.append(jointPos)
        self.get_logger().info("Sending points")
        out_msg.points = points
        self.posPub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = posePublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
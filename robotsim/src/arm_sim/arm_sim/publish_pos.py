import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_system_default
from rclpy.time import Time

from ament_index_python.packages import get_package_share_directory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

import os
import time

class posePublisher(Node):
    def __init__(self):
        super().__init__('pose_publisher')
        self.posPub = self.create_publisher(JointTrajectory, '/model/printerArm/joint_trajectory', qos_profile_system_default)
        self.startTime = 0
        time.sleep(1)
        # self.startGzBridge()
        self.sendGoal(self.HCodeToJointPoints())

    def startGzBridge(self):
        topic = '/model/printerArm/joint_trajectory'
        gz_type = 'gz.msgs.JointTrajectory'
        ros_type = 'trajectory_msgs/msg/JointTrajectory'
        self.get_logger().info(f'Running \'ros2 run ros_gz_bridge parameter_bridge {topic}@{ros_type}]{gz_type}\'')
        os.system(f'ros2 run ros_gz_bridge parameter_bridge {topic}@{ros_type}]{gz_type}')

    def HCodeToJointPoints(self):
        points = []
        f = open(os.path.join(get_package_share_directory('arm_sim'), 'Test_Part_1.hcode'))
        curNs = 0
        curS = 0
        for line in f:
            jointPos = JointTrajectoryPoint()
            jointPos.positions = [float(i) for i in line[0:line.index('#')].split()]
            jointPos.time_from_start.sec = curS
            jointPos.time_from_start.nanosec = curNs
            points.append(jointPos)
            if curNs + 100000000 >= 1e9:
                curS += 1
                curNs = 0
            else:
                curNs += 100000000
        return points

    def sendGoal(self, points):
        self.get_logger().info(str(len(points)))
        out_msg = JointTrajectory()
        out_msg.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        out_msg.points = points
        self.posPub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = posePublisher()
    rclpy.spin(node)

if __name__ == '__main__':
    main()
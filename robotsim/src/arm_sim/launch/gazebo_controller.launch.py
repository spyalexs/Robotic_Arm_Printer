import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

world_file_name = 'my_empty_world.world'
world = os.path.join(get_package_share_directory('arm_sim'), world_file_name)


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    urdf_file_name = 'arm.urdf'
    urdf = os.path.join(
        get_package_share_directory('arm_sim'),
        urdf_file_name)
    with open(urdf, 'r') as infp:
        robot_desc = infp.read()

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use simulation (Gazebo) clock if true'),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time,
                         'robot_description': robot_desc}],
            arguments=[urdf]),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory(
                    'arm_sim'), 'gz_sim.launch.py')
            ),
            launch_arguments={'gz_args': '-r empty.sdf'}.items(),
        ),

        # ExecuteProcess(cmd=['gazebo', '--verbose', world,
        #                '-s', 'libgazebo_ros_factory.so'], output='screen'),

        # ExecuteProcess(
        #     cmd=['ros2', 'control', 'load_controller',
        #          '--set-state', 'start', 'joint_state_broadcaster'],
        #     output='screen'),


        # ExecuteProcess(
        #     cmd=['ros2', 'control', 'load_controller', '--set-state',
        #          'start', 'joint_trajectory_controller'],
        #     output='screen')

        # Node(
        #     name='state_publisher',
        #     package='arm_sim',
        #     executable='state_publisher',
        #     output='screen'),
    ])

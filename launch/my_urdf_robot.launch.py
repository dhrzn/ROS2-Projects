import os 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node

def generate_launch_description():
    urdf_file = os.path.join(
        get_package_share_directory('my_robot_pkg'),
        'urdf_practice',
        'my_robot.urdf'
    )

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    return LaunchDescription([
        #publishing robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
        ExecuteProcess(
            cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'],
            output='screen'

        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=['-topic', 'robot_description', '-entity', 'my_robot', '-z', '0.1'],
            output='screen'
        ),

        #Node(
            #package='joint_state_publisher',
           # executable='joint_state_publisher',
            #arguments=[urdf_file],
            #output='screen'
        #),
    ])

#note joint publisher was removed because gazebo actually reads and changes the value for joint positioning, and in rviz, we need a dummy value for it to actually show case the robot
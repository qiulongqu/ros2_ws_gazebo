from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from pathlib import Path


def generate_launch_description():
    description_share = Path(get_package_share_directory('simple_arm_description'))
    urdf_path = description_share / 'urdf' / 'simple_6dof_arm.urdf'
    rviz_config_path = description_share / 'rviz' / 'arm_display.rviz'

    with open(urdf_path, 'r') as infp:
        robot_description_content = infp.read()

    robot_description = {'robot_description': robot_description_content}

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[robot_description]
        ),
        Node(
            package='arm_trajectory_planner',
            executable='planned_to_joint_state',
            output='screen'
        ),
        Node(
            package='arm_trajectory_planner',
            executable='joint_trajectory_planner',
            output='screen'
        ),
        Node(
            package='arm_trajectory_planner',
            executable='auto_demo_publisher',
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d', str(rviz_config_path)],
            output='screen'
        )
    ])

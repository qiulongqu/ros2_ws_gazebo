# Exection单次目标运动

## 第一步

先在第一个终端里运行:
source /opt/ros/jazzy/setup.bash
cd /home/yunhao/ros2_ws_practise
colcon build --packages-select arm_trajectory_planner simple_arm_description
source install/setup.bash
export ROS_LOG_DIR=/tmp/ros_logs
ros2 launch simple_arm_description display.launch.py

## 第二步

在第二个终端里发布目标角度:
source /opt/ros/jazzy/setup.bash
cd /home/yunhao/ros2_ws_practise
source install/setup.bash
ros2 topic pub /target_joint_positions std_msgs/msg/Float64MultiArray "{data: [0.5, -0.3, 0.8, 0.2, -0.5, 0.1]}" --once

也可以发布其他角度：
ros2 topic pub /target_joint_positions std_msgs/msg/Float64MultiArray "{data: [-0.4, 0.6, -0.5, 0.3, 0.2, -0.2]}" --once

# Exection循环运动演示

## 在终端里运行：
source /opt/ros/jazzy/setup.bash
cd /home/yunhao/ros2_ws_practise
colcon build --packages-select arm_trajectory_planner simple_arm_description
source install/setup.bash
export ROS_LOG_DIR=/tmp/ros_logs
ros2 launch simple_arm_description display.launch.py

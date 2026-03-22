# 初始化和启动命令：

## 1：在每个终端打开之前必须运行的
    目的是：设置环境变量，使得ROS2可以正常运行。
    source ~/ros2_ws_gazebo/install/setup.bash

## 2：创建运行包体：
    作用是：创建一个ROS2运行包。
    ros2 run package_name executable_name

    例如：
    ros2 pkg create --build-type ament_python simple_arm_description
    (以上代码的作用是创建一个机械臂描述包)

## 3：编译运行包：
    作用是：编译运行包，可以使得ROS2可以识别到该包。
    cd ~/ros2_ws_gazebo
    colcon build

    例如：
    cd ~/ros2_ws_gazebo/src/simple_arm_description
    colcon build --packages-select simple_arm_description
    > (编译指定的包，加上--packages-select参数，可以只编译指定的包。)

## 4：运行节点：
    (每个节点都在需要在一个新的终端中运行，并且必须先运行source ~/ros2_ws/install/setup.bash
    注意：节点是在install中运行的，而不是在build中运行的。)
    ros2 run package_name executable_name

    例如：
    ros2 run arm_trajectory_planner joint_trajectory_planner
    > (启动轨迹规划节点)

    例如：
    ros2 run arm_trajectory_planner planned_to_joint_state
    > (启动桥接节点)

## 5：向话题发布消息：
    (在ros2中，节点之间互不关联，只通过话题topic进行通信。)
    ros2 topic pub /topic_name message_type message_content

    例如：
    ros2 topic pub -r 10 /joint_states sensor_msgs/msg/JointState "{name: ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6'], position: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}"
    (发布初始关节状态，-r参数表示每秒发布一次)

    例如：
    ros2 topic pub /target_joint_positions std_msgs/msg/Float64MultiArray "{data: [0.5, -0.3, 0.8, 0.2, -0.5, 0.1]}" --once
    (发布目标关节位置，--once参数表示只发布一次)

    注意：
    发布的消息类型必须与发布的topic类型一致。
    以上例子按顺序依次执行，再在所有的例子的最前面开启RViz仿真器，可以开启仿真机械臂。

## 6：启动RViz仿真器：
    作用是：启动RViz仿真器，可以查看节点发布的消息。
    ros2 run rviz2 rviz2

    具体操作：
    打开一个新的终端，输入以下命令：
    source ~/ros2_ws_practise/install/setup.bash
    ros2 launch simple_arm_description display.launch.py

    ros2 topic echo /tf
    (查看tf变换,这条命令能够解决tf变换的发布问题)

# ROS2工作项目的创建：

## 1：创建工作空间：
    作用是：创建一个ROS2工作空间。
    mkdir -p ~/ros2_ws_practise/src
    cd ~/ros2_ws_practise
    colcon build

## 2：创建ROS2包：
    作用是：创建一个ROS2运行包。
    ros2 pkg create --build-type ament_python package_name

    例如：
    ros2 pkg create --build-type ament_python arm_trajectory_planner

## 3：编译运行包：
    作用是：编译运行包，可以使得ROS2可以识别到该包。
    cd ~/ros2_ws_practise
    colcon build

## 4：创建节点：
    暂定

## 5：创建依赖关系：
    (在package.xml文件中添加依赖关系)
    
    例如：
    <exec_depend>rclpy</exec_depend>
    <exec_depend>std_msgs</exec_depend>
    <exec_depend>sensor_msgs</exec_depend>

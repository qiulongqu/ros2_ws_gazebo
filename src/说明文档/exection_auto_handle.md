# 机械臂仿真运行说明

本文档将项目的运行方式分为两种：

1. 自动模式：启动后机械臂会自动在两组目标姿态之间循环运动
2. 手动模式：启动后机械臂保持等待状态，由用户在第二个终端手动发送一次目标角度

这两种模式使用的启动文件不同，请不要混用。

## 一、自动模式

自动模式使用的启动文件是：

```bash
ros2 launch simple_arm_description display.launch_auto.py
```

这个启动文件会同时启动：

1. `robot_state_publisher`：根据 URDF 机械臂模型和 `/joint_states` 计算每个连杆的 TF 变换
2. `planned_to_joint_state`：把规划后的关节角转换成 `/joint_states`
3. `joint_trajectory_planner`：接收目标关节角并生成平滑轨迹
4. `auto_demo_publisher`：自动周期性发布目标角度
5. `rviz2`：打开 RViz 显示机械臂模型和运动过程

### 运行步骤

在第一个终端中依次执行：

```bash
# 加载系统中安装的 ROS2 Jazzy 环境。
# 作用：让当前终端可以使用 ros2、rviz2、colcon 等命令。
source /opt/ros/jazzy/setup.bash

# 进入当前 ROS2 工作空间根目录。
# 作用：后续编译和加载 install 环境都需要在这个目录下完成。
cd /home/yunhao/ros2_ws_gazebo

# 编译当前项目中的两个功能包。
# arm_trajectory_planner 负责轨迹规划与话题转换；
# simple_arm_description 负责机械臂模型、URDF 和启动文件。
colcon build --packages-select arm_trajectory_planner simple_arm_description

# 加载当前工作空间编译后的 install 环境。
# 作用：让 ROS2 能识别你自己写的功能包与节点。
source install/setup.bash

# 设置 ROS2 的日志输出目录。
# 作用：运行日志会写入 /tmp/ros_logs，方便排查问题，也能避免默认日志目录权限问题。
export ROS_LOG_DIR=/tmp/ros_logs

# 启动自动演示模式。
# 作用：打开 RViz，并自动让机械臂在两组姿态之间循环运动。
ros2 launch simple_arm_description display.launch_auto.py
```

### 自动模式特点

1. 启动后不需要第二个终端发送命令
2. 机械臂会自动循环往返运动
3. 适合做演示和快速检查可视化是否正常

## 二、手动模式

手动模式使用的启动文件是：

```bash
ros2 launch simple_arm_description display_static.launch.py
```

这个启动文件会启动：

1. `robot_state_publisher`：根据 URDF 和 `/joint_states` 计算机械臂 TF
2. `planned_to_joint_state`：把规划后的关节角转换成 `/joint_states`
3. `joint_trajectory_planner`：接收手动发布的目标角度并生成平滑轨迹
4. `rviz2`：显示机械臂运动过程

注意：
这个模式不会启动 `auto_demo_publisher`，因此不会自动发送目标角度，也不会干扰你的手动控制。

### 第一步：启动手动模式

先在第一个终端中依次执行：

```bash
# 加载系统中安装的 ROS2 Jazzy 环境。
# 作用：让当前终端可以使用 ros2、rviz2、colcon 等 ROS2 命令。
source /opt/ros/jazzy/setup.bash

# 进入当前 ROS2 工作空间根目录。
# 作用：后续编译和加载工作空间环境都依赖这个目录。
cd /home/yunhao/ros2_ws_gazebo

# 编译当前项目中的两个核心功能包。
# 作用：把源码安装到 install 目录中，供 launch 和 run 使用。
colcon build --packages-select arm_trajectory_planner simple_arm_description

# 加载当前工作空间编译后的 install 环境。
# 作用：让 ROS2 能找到你自己写的节点、启动文件和包。
source install/setup.bash

# 设置 ROS2 日志目录到 /tmp/ros_logs。
# 作用：保存运行日志，方便查看报错与节点输出。
export ROS_LOG_DIR=/tmp/ros_logs

# 启动手动模式。
# 作用：打开 RViz，并启动轨迹规划链路，但不会自动发送目标角度。
ros2 launch simple_arm_description display_static.launch.py
```

### 第二步：手动发送一次目标角度

再打开第二个终端，依次执行：

```bash
# 加载系统中安装的 ROS2 Jazzy 环境。
source /opt/ros/jazzy/setup.bash

# 进入当前 ROS2 工作空间根目录。
cd /home/yunhao/ros2_ws_gazebo

# 加载当前工作空间 install 环境。
# 作用：确保当前终端能够正确识别当前项目中的 ROS2 运行环境。
source install/setup.bash

# 向 /target_joint_positions 话题发送一条目标关节角指令。
# 消息类型是 std_msgs/msg/Float64MultiArray。
# data 中的 6 个数值分别对应 joint1 到 joint6 的目标角度。
# --once 表示只发送一次，不循环重复发送。
ros2 topic pub /target_joint_positions std_msgs/msg/Float64MultiArray "{data: [0.5, -0.3, 0.8, 0.2, -0.5, 0.1]}" --once
```

### 另一组可选的目标角度

如果你想让机械臂运动到另一组姿态，也可以发送：

```bash
# 向 /target_joint_positions 发布另一组 6 关节目标角度。
# 作用：让机械臂从当前姿态平滑运动到新的目标姿态。
ros2 topic pub /target_joint_positions std_msgs/msg/Float64MultiArray "{data: [-0.4, 0.6, -0.5, 0.3, 0.2, -0.2]}" --once
```

### 这条手动控制命令的实际意义

命令中的：

```bash
{data: [0.5, -0.3, 0.8, 0.2, -0.5, 0.1]}
```

表示：

1. `joint1 = 0.5`
2. `joint2 = -0.3`
3. `joint3 = 0.8`
4. `joint4 = 0.2`
5. `joint5 = -0.5`
6. `joint6 = 0.1`

也就是说，你是在一次性给 6 个关节分别设置一个目标角度。

## 三、两种模式的区别

### 自动模式

启动命令：

```bash
ros2 launch simple_arm_description display.launch.py
```

特点：

1. 启动后自动运动
2. 不需要第二个终端
3. 适合做演示

### 手动模式

启动命令：

```bash
ros2 launch simple_arm_description display_static.launch.py
```

特点：

1. 启动后不会自动运动
2. 需要第二个终端手动发送目标角度
3. 适合测试指定姿态和单次目标运动

## 四、整个机械臂仿真的运行链路

手动模式下，命令执行后的数据流如下：

```text
ros2 topic pub /target_joint_positions
        ->
joint_trajectory_planner 生成平滑轨迹
        ->
planned_to_joint_state 转换成 /joint_states
        ->
robot_state_publisher 计算各个连杆的 TF
        ->
rviz2 显示机械臂运动
```

自动模式下，上面的第一步不是由用户手动输入，而是由 `auto_demo_publisher` 自动定时发布。

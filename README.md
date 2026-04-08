# ROS2 6自由度机械臂仿真项目

基于 ROS2 Jazzy + RViz 的 6 自由度机械臂关节空间轨迹规划与可视化项目。
使用的机械臂是自制的简单几何体组成的示意图，并使用 RViz 进行可视化。
工程中使用时推荐到官方的仓库克隆对应的机械臂配置包，并进行修改。
本项目仅作为本人学习 ROS2 轨迹规划和机械臂仿真的练习，代码质量和功能完整性可能不够完善，请勿用于生产环境。

## 项目结构

```
ros2_ws_gazebo_ST/
├── src/
│   ├── arm_trajectory_planner/      # 轨迹规划包
│   │   ├── arm_trajectory_planner/
│   │   │   ├── auto_demo_publisher.py    # 自动演示节点
│   │   │   └── joint_trajectory_planner.py  # 轨迹规划节点
│   │   └── package.xml
│   │
│   ├── simple_arm_description/       # 机械臂描述包
│   │   ├── urdf/
│   │   │   └── simple_6dof_arm.urdf     # 6DOF机械臂URDF模型
│   │   ├── launch/
│   │   │   └── display.launch.py          # RViz显示启动文件
│   │   └── package.xml
│   │
│   └── 说明文档/                    # 项目文档
│
├── build/                           # 编译目录 (已忽略)
├── install/                         # 安装目录 (已忽略)
└── log/                             # 日志目录 (已忽略)
```

## 包说明

### 1. simple_arm_description

机械臂模型与 RViz 显示包。

**包含内容：**
- `simple_6dof_arm.urdf` - 6 自由度机械臂 URDF 模型
- `display.launch.py` - RViz 显示启动文件

**URDF 模型结构：**
- base_link（基座）
- link1 ~ link6（6个连杆）
- joint1 ~ joint6（6个旋转关节）

### 2. arm_trajectory_planner

轨迹规划与桥接包。

**包含节点：**
- `joint_trajectory_planner.py` - 订阅 `/target_joint_positions`，生成五次多项式平滑轨迹，发布 `/planned_joint_positions`
- `planned_to_joint_state.py` - 将规划结果转换为 `/joint_states` 供 RViz 显示
- `auto_demo_publisher.py` - 自动演示节点，发布两个预设目标实现往复运动

## 数据流

```
/target_joint_positions
        ↓
joint_trajectory_planner
        ↓
/planned_joint_positions
        ↓
planned_to_joint_state
        ↓
/joint_states
        ↓
robot_state_publisher
        ↓
RViz 显示机械臂运动
```

## 依赖

- ROS2 Jazzy
- rclpy
- std_msgs
- sensor_msgs
- robot_state_publisher
- rviz2

## 编译

```bash
cd ~/ros2jazzy_wsl/ros2_ws_gazebo_ST
source /opt/ros/jazzy/setup.bash
colcon build
source install/setup.bash
```

## 运行

### 方式一：使用自动演示（推荐）

```bash
# 终端1：启动显示
ros2 launch simple_arm_description display.launch.py

# 终端2：启动自动演示
ros2 run arm_trajectory_planner auto_demo_publisher
```

### 方式二：手动发布目标

```bash
# 终端1：启动显示
ros2 launch simple_arm_description display.launch.py

# 终端2：手动发布目标关节角
ros2 topic pub /target_joint_positions std_msgs/Float64MultiArray "{data: [0.5, -0.3, 0.8, 0.2, -0.5, 0.1]}"
```

## 关节角说明

机械臂有 6 个关节，关节角单位为弧度：

| 关节 | 范围 (rad) | 轴 |
|------|-----------|-----|
| joint1 | [-3.14, 3.14] | Z |
| joint2 | [-1.57, 1.57] | Y |
| joint3 | [-1.57, 1.57] | Y |
| joint4 | [-3.14, 3.14] | X |
| joint5 | [-3.14, 3.14] | Y |
| joint6 | [-3.14, 3.14] | X |

## Topic 说明

| Topic | 类型 | 方向 | 说明 |
|-------|------|------|------|
| `/target_joint_positions` | std_msgs/Float64MultiArray | 订阅 | 目标关节角输入 |
| `/planned_joint_positions` | std_msgs/Float64MultiArray | 发布 | 规划后的轨迹点 |
| `/joint_states` | sensor_msgs/JointState | 发布 | 机械臂当前状态 |

## License

TODO

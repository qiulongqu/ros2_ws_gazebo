import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
import time
import math


class JointTrajectoryPlanner(Node):
    def __init__(self):
        super().__init__('joint_trajectory_planner')

        # 6自由度机械臂
        self.num_joints = 6

        # 当前关节状态
        self.current_positions = [0.0] * self.num_joints
        self.joint_state_received = False

        # 轨迹参数
        self.start_positions = [0.0] * self.num_joints
        self.goal_positions = [0.0] * self.num_joints
        self.motion_duration = 3.0   # 轨迹总时间 3 秒
        self.start_time = None
        self.executing = False

        # 订阅目标关节角
        self.target_sub = self.create_subscription(
            Float64MultiArray,
            '/target_joint_positions',
            self.target_callback,
            10
        )

        # 订阅当前关节角（通常来自仿真器/机器人状态）
        self.joint_state_sub = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )

        # 发布规划后的关节参考位置
        self.command_pub = self.create_publisher(
            Float64MultiArray,
            '/planned_joint_positions',
            10
        )

        # 定时器：100Hz 发布轨迹点
        self.timer = self.create_timer(0.01, self.timer_callback)

        self.get_logger().info('Joint trajectory planner node started.')

    def joint_state_callback(self, msg: JointState):
        if len(msg.position) >= self.num_joints:
            self.current_positions = list(msg.position[:self.num_joints])
            self.joint_state_received = True

    def target_callback(self, msg: Float64MultiArray):
        if len(msg.data) != self.num_joints:
            self.get_logger().warn(f'目标关节角数量错误，应为 {self.num_joints} 个')
            return

        if not self.joint_state_received:
            self.get_logger().warn('尚未接收到 /joint_states，无法规划轨迹')
            return

        self.start_positions = self.current_positions.copy()
        self.goal_positions = list(msg.data)
        self.start_time = time.time()
        self.executing = True

        self.get_logger().info(f'Received target: {self.goal_positions}')
        self.get_logger().info(f'Start from: {self.start_positions}')

    def quintic_interpolation(self, q0, qf, t, T):
        """
        五次多项式插值:
        q(t) = q0 + dq * (10*s^3 - 15*s^4 + 6*s^5)
        其中 s = t/T
        """
        if T <= 0.0:
            return qf

        s = max(0.0, min(1.0, t / T))
        dq = qf - q0
        q = q0 + dq * (10 * s**3 - 15 * s**4 + 6 * s**5)
        return q

    def timer_callback(self):
        if not self.executing:
            return

        if self.start_time is None:
            self.get_logger().warn('start_time is None, cannot execute trajectory.')
            return
        
        elapsed = time.time() - self.start_time

        if elapsed >= self.motion_duration:
            cmd = Float64MultiArray()
            cmd.data = self.goal_positions
            self.command_pub.publish(cmd)

            self.executing = False
            self.get_logger().info('Trajectory execution completed.')
            return

        planned_positions = []
        for i in range(self.num_joints):
            q = self.quintic_interpolation(
                self.start_positions[i],
                self.goal_positions[i],
                elapsed,
                self.motion_duration
            )
            planned_positions.append(q)

        cmd = Float64MultiArray()
        cmd.data = planned_positions
        self.command_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = JointTrajectoryPlanner()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
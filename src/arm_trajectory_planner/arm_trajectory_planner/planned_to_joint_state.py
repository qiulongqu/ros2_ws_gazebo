import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


# 桥接节点（依附于轨迹规划节点）
class PlannedToJointState(Node):
    def __init__(self):
        super().__init__('planned_to_joint_state')

        self.joint_names = [
            'joint1',
            'joint2',
            'joint3',
            'joint4',
            'joint5',
            'joint6'
        ]

        self.sub = self.create_subscription(
            Float64MultiArray,
            '/planned_joint_positions',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            JointState,
            '/joint_states',
            10
        )

        self.initial_positions = [0.0] * len(self.joint_names)
        self.received_planned_positions = False
        self.initial_publish_count = 0
        self.initial_timer = self.create_timer(0.2, self.publish_initial_state)

        self.get_logger().info('planned_to_joint_state node started.')

    def publish_joint_state(self, positions):
        joint_state_msg = JointState()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        joint_state_msg.name = self.joint_names
        joint_state_msg.position = list(positions)

        self.pub.publish(joint_state_msg)

    def publish_initial_state(self):
        if self.received_planned_positions:
            self.initial_timer.cancel()
            return

        self.publish_joint_state(self.initial_positions)
        self.initial_publish_count += 1

        # Publish a few times so downstream subscribers are very likely to see it.
        if self.initial_publish_count >= 10:
            self.initial_timer.cancel()

    def callback(self, msg):
        if len(msg.data) != 6:
            self.get_logger().warn('Expected 6 joint values.')
            return

        self.received_planned_positions = True
        self.publish_joint_state(msg.data)


def main(args=None):
    rclpy.init(args=args)
    node = PlannedToJointState()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

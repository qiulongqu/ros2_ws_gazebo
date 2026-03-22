import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray


class AutoDemoPublisher(Node):
    def __init__(self):
        super().__init__('auto_demo_publisher')

        self.target_pub = self.create_publisher(
            Float64MultiArray,
            '/target_joint_positions',
            10
        )

        self.demo_targets = [
            [0.5, -0.3, 0.8, 0.2, -0.5, 0.1],
            [-0.4, 0.6, -0.5, 0.3, 0.2, -0.2],
        ]
        self.current_target_index = 0

        # Give the planner a moment to receive the initial joint state first.
        self.initial_timer = self.create_timer(1.5, self.start_demo)
        self.loop_timer = None

        self.get_logger().info('auto_demo_publisher node started.')

    def publish_target(self):
        msg = Float64MultiArray()
        msg.data = list(self.demo_targets[self.current_target_index])
        self.target_pub.publish(msg)

        self.get_logger().info(
            f'Published demo target {self.current_target_index + 1}: {msg.data}'
        )

        self.current_target_index = (self.current_target_index + 1) % len(self.demo_targets)

    def start_demo(self):
        self.initial_timer.cancel()
        self.publish_target()

        # Slightly longer than the planner motion duration, so commands don't overlap.
        self.loop_timer = self.create_timer(4.0, self.publish_target)


def main(args=None):
    rclpy.init(args=args)
    node = AutoDemoPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time.time
import threading

class RotateWheel(Node):
    def __init__(self,name):
        self.pub_rate = self.create_rate(5)
        super().__init__(name)
        self.get_logger().info(f'node{name}init..')
        self.joint_pub = self.create_publisher(JointState,'/joint_states',10)
        self.thread = threading.Thread(target=self._thread_pub)
        self.thread.start()

    def joint_state_msg(self):
        self.joint_speeds = [0.0,0.0]
        self.joint_states = JointState()
        self.joint_states.header.stamp = self.get_clock().now().to_msg()
        self.joint_states.header.frame_id = ''
        self.joint_states.name = ['left_wheel_joint','right_wheel_joint']
        self.joint_states.position = [0.0,0.0]
        self.joint_states.velocity = self.joint_speeds
        self.joint_states.effort = []
    def update_speed(self,speeds):
        self.joint_speeds = speeds    
   
        
    def _thread_pub(self):
        last_update_time = time.time()
        while rclpy.ok():
            delta_time = time.time() - last_update_time
            last_update_time = time.time()
            self.joint_states.position[0] += self.joint_speeds[0] * delta_time
            self.joint_states.position[1] += self.joint_speeds[1] * delta_time
            self.joint_states.velocity = self.joint_speeds
            self.joint_states.header.stamp = self.get_clock().now().to_msg()
            self.joint_pub.publish(self.joint_states)
            self.pub_rate.sleep()
          
def main(args=None):
    rclpy.init(args=args)
    node = RotateWheel('rotate_yezibot_wheel')
    node.update_speed([15.0,-15.0])  # 设置轮子旋转速度
    rclpy.spin(node)
    rclpy.shutdown()        
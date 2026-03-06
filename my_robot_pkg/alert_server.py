import rclpy
from rclpy.node import Node
from my_robot_interfaces.srv import TriggerAlert
from std_msgs.msg import String
threshold = 30

class AlertServerNode(Node):
    def __init__(self):
        super().__init__('alert_server')
        self.server = self.create_service(TriggerAlert, 'trigger_alert', self.alert_callback) #referencinng its objecting by going through the trigger alert interfaces and communicating with client with 'trigger_alert' and defining what we want to do with the request we recieve from client
        self.get_logger().info('Alert server is ready!') #making our server announce that its aline and ready to recieve requests (useful for debugging because you never know if the server fully started)
        self.command_pub = self.create_publisher(String, '/alert_command', 10)

    def alert_callback(self,request,response):

        if request.distance < threshold:
            self.get_logger().warn(f'Alert triggered! distance: {request.distance:.2f}')
            message = f'ALERT:{request.distance:.2f}' #this is us defining what message we want to send back to the ardunio board
        else:
            self.get_logger().info('All clear!')
            message = 'CLEAR'

        msg = String()
        msg.data = message
        self.command_pub.publish(msg)
        response.success = True #sending a response back to monitor node
        return response #sending the true response letting the mintor node everything went smoothly



def main(args=None):
    rclpy.init(args=args)
    node = AlertServerNode()
    rclpy.spin(node)
    node.destroy(node) #after we hit ctr c it cleans up the que and basically logs out of node so when we run it it starts fresh without any left over data
    rclpy.shutdown()

if __name__ == '__main__':
    main()


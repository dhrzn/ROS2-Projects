import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32 #need this because this is the type of data we are recieveing from the topic
from my_robot_interfaces.srv import TriggerAlert #importing so we can com with server


class MonitorNode(Node):
    def __init__(self):
        super().__init__('monitor_node') #name
        self.declare_parameter('threshold', 30.0) #defining default parameter (name, default value)
        self.subscription = self.create_subscription(Float32, '/distance', self.distance_callback, 10) #creating subscription (data expected to recieve, subbing to topic, what we want to do with that data, que size)
        #Note: we add the distance_call back because while we are subscribed we want to hear and see the data is coming in and now we want to do something with that said data and thats why we create a function.
        #this function would help us to compare to the threshold we set and check it if passes or not which depending if it passes it would send a signal back to the ardunio board
        #if below the threshold we want to call the alert service and if over we want to keep still listening thats what our distance_callback will do 
        self.client = self.create_client(TriggerAlert, 'trigger_alert') #defining the client
        #Note: Triggeralert tells the client what format to use for request and response (basically just inherits and sees what we defined in our trigger_alert interface)
        #Note: 'trigger_alert' is the shared name both client and server uses to find eachother

    def distance_callback(self,msg):
        distance = msg.data #the type of data that was published but we are unpacking it the same way just like how we did when it was published
        threshold = self.get_parameter('threshold').value #just defining threshold and based off of a parameter we may change or set it would know else it goes to default value

        request = TriggerAlert.Request() #requesting service
        request.distance = distance #helping us fill the field when we defined 'float32 distance' in the trigger_alert parameter and this lets us send the distance value as context to the service
        self.client.call_async(request) #this means "call the service but dont wait for a response" (async part means the node keeps running and checking distance while the service call happens in the background)
        #Note: if we just use the regular 'call' it would freeze and wait for the response every time

        if distance < threshold:
            self.get_logger().warn(f'Object too close! Distance: {distance:.2f} cm') #ros version of print but we do .warn to it prints out our text in yellow as a warning
            


def main(args = None):
    rclpy.init(args=args)
    node = MonitorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
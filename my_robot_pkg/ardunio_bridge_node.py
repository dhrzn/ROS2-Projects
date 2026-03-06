import rclpy #accessing ros2 python library 
from rclpy.node import Node #importing our Node class so we can inherit from it 
#(Note: added string because thats what we will recieve from alert_server so we can send back to ardunio):
from std_msgs.msg import Float32, String #accessing our message type for pubishinh distance
import serial #allows python to open and read from USB port

class ArdunioBridgeNode(Node):
    def __init__(self):
        super().__init__('ardunio_bridge_node') #naming our node
        self.publisher_ = self.create_publisher(Float32, '/distance',10) #(data type, name of topic, que size)
        self.serial_connection = serial.Serial('/dev/ttyACM0', 9600, timeout = 1) #(the serial name for ardunio board, standard time data comes in and matching the serial.begin(9600) from ardunio board...)
        # note that the timeout = 1 waits for data and if nothing comes out for 1 second, dont wait forever and move on
        self.timer = self.create_timer(.01, self.read_serial) #for every 0.1s it reads off read_serial (or for every 0.1s call this function)
        self.alert_sub = self.create_subscription(String, '/alert_command', self.send_command,10)
    def read_serial(self):
        if self.serial_connection.in_waiting > 0:  #in_waiting tells how many bytes are currently sitting in seiral buffer waiting to be read (basically if there is at leas soemething waiting, go read it)
            line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip() #grabs one full line of text "decode(utf-8)" and convert it from raw bytes into a python string
            # was having issues when runnnnnning it the first time because ardunio_bridge_nodeee was finding bytes but couldnt decode bytes so we added error = ignore to keep moving if it has this issue
            msg = Float32() #creaing a float32 message object
            try:
                msg.data = float(line) #taling the string of txt like "66.82" and converting it to an actual float
                self.publisher_.publish(msg) # publishing message (already defined where publisher publishes)
                self.get_logger().info(f'publishing distance: {msg.data} cm')  #ros2 version of print
            except ValueError:
                pass #pass just means if line cant be converted to a float, skip it and move on
            #added the try and except because we were getting garbled data like '24ij' instead of clean numbers due to the serial buffer getting bixed up betweem distance data going out and alert signals coming in
    
    
    #what we are sending back to ardunio
    def send_command(self,msg):
        command = msg.data + '\n' #each message gets their own line
        self.serial_connection.write(command.encode()) #transfering the string we get into bytes for ardunio (what we are sending back)
        self.get_logger().info(f'Sent to Ardunio: {command.strip()}')


def main(args=None):
    rclpy.init(args=args)
    node = ArdunioBridgeNode()
    rclpy.spin(node)
    node.destory(node) #after we hit ctr c it cleans up the que and basically logs out of node so when we run it it starts fresh without any left over data
    rclpy.shutdown()

if __name__ == '__main__':
    main()
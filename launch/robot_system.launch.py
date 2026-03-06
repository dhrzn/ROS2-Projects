from launch import LaunchDescription #this just gives deails about nodes
#says this argyment exists and if user doesnt pass value just use default val
from launch.actions import DeclareLaunchArgument
#recognizes user input when user tries to pass an argument
from launch.substitutions import LaunchConfiguration 
#lets us just use Node
from launch_ros.actions import Node

def generate_launch_description():
	return LaunchDescription([
#lets ros know default value so when it finishes passing argument it can come back to this value when done
		DeclareLaunchArgument(
			'battery_level',
			default_value = '75.0',
			description = 'Simulated battery percentage',
		),


	
		#defining our publisher
		Node(
			package = 'my_robot_pkg',
			executable = 'publisher_node',
			name = 'publisher_node'
		),
		#defining our subscriber
		Node(
			package = 'my_robot_pkg',
			executable = 'subscriber_node',
			name = 'subscriber_node'
		),

		#defining our server 
		Node(
			package = 'my_robot_pkg',
			executable = 'battery_server',
			name = 'battery_server',
		#setting up parameters so we can run arugments for simulation
			parameters=[{
				'battery_level': LaunchConfiguration('battery_level')
			}]
		),

		


	]) 
#Notes for parameter:
#parameter field is how you pass values into a node from launch file.
#"give the battery_server a parameter called battery_level and its value comes
#from whatever launchContuguration('battery_level') reads else its default
#reads either the user's input or just sets as default

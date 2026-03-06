from setuptools import find_packages, setup
import os #tools to work with operating system file like building file paths
from glob import glob #tools to find every tile in launch folder
#needed becayse if you add more launch files it automatucally picks them
# all up without havig to list each one manually
#'launch/*.launch.py' finds every file in launch folder that ends with launch.py

package_name = 'my_robot_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
	(os.path.join('share', package_name, 'launch'),glob('launch/*.launch.py')),
#basically grabs anything that ends in launch.py and
# super useful when creating another launch file (dont need to change anything here when created) 
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dhrn',
    maintainer_email='dhrn@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
		'publisher_node = my_robot_pkg.publisher_node:main',
		'subscriber_node = my_robot_pkg.subscriber_node:main',
		'battery_server = my_robot_pkg.battery_server:main',
		'battery_client = my_robot_pkg.battery_client:main',
        'ardunio_bridge_node = my_robot_pkg.ardunio_bridge_node:main',
        'monitor_node = my_robot_pkg.monitor_node:main',
        'alert_server = my_robot_pkg.alert_server:main',
        ],
    },
)

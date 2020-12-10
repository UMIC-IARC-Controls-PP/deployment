#!/usr/bin/env python
# ROS python API
import rospy
import time

# 3D point & Stamped Pose msgs
from geometry_msgs.msg import *
# import all mavros messages and services
from mavros_msgs.msg import *
from mavros_msgs.srv import * 
from sensor_msgs.msg import Imu

def setarm(x): # input: 1=arm, 0=disarm
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
		response = arming(x)
		response.success
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

def setmode(x):
	rospy.wait_for_service('/mavros/set_mode')
	try:
		mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
		response = mode(0,x)
		response.mode_sent
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

def imu_call(val):
	global z
	z = val.linear_acceleration.z
	print(z)

def man_pub(man_msg):
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(man_msg)
        rate.sleep()


if __name__ == '__main__':
	rospy.init_node('drop_node', anonymous=True)
	print("drop_node initialised...")
	pub = rospy.Publisher('mavros/manual_control/send', ManualControl, queue_size=10)
	rospy.Subscriber("/mavros/imu/data", Imu, imu_call)
	man_msg = ManualControl()
	setarm(1)
	time.sleep(4)
	while True:
		if(0<z<0.2):
			setmode('MANUAL')
			man_msg.x = 0
			man_msg.y = 0
			man_msg.z = 0
			man_msg.r = 0
			man_pub(man_msg)

			print('Its stable baby')




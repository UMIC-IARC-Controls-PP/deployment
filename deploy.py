#!/usr/bin/env python
# ROS python API
import rospy
import time

# 3D point & Stamped Pose msgs
from geometry_msgs.msg import *
# import all mavros messages and services
from mavros_msgs.msg import *
from mavros_msgs.srv import * 


def setArm():
        rospy.wait_for_service('mavros/cmd/arming')
        try:
            armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
            armService(True)
        except rospy.ServiceException, e:
            print "Service arming call failed: %s"%e


def setPositionMode():
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='POSCTL')
        except rospy.ServiceException, e:
            print "service set_mode call failed: %s. Position Mode could not be set."%e

def setManualMode():
        rospy.wait_for_service('mavros/set_mode')
        try:
            flightModeService = rospy.ServiceProxy('mavros/set_mode', mavros_msgs.srv.SetMode)
            flightModeService(custom_mode='MANUAL')
        except rospy.ServiceException, e:
            print "service set_mode call failed: %s. Manual Mode could not be set."%e



rospy.init_node('setpoint_node', anonymous=True)
print("node initialised...")
pub = rospy.Publisher('mavros/manual_control/send', ManualControl, queue_size=10)
sp_pub = rospy.Publisher('mavros/setpoint_raw/local', PositionTarget, queue_size=1)
msg = ManualControl()

armService = rospy.ServiceProxy('mavros/cmd/arming', mavros_msgs.srv.CommandBool)
armService(True)
setManualMode()
msg.x = 0
msg.y = 0
msg.z = 0
msg.r = 0

i = 0
while i < 100:
    pub.publish(msg)
    rospy.sleep(1)
    i = i + 1



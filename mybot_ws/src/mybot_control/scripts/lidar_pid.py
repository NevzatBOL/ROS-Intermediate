#!/usr/bin/env python
#-*-coding: utf-8 -*-

import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

integral2 =0
e2 = 0

def scancallback(scan):
    """
    Lidar sagdan sola dogru lazer atıyor.
    Robotun pozitif angular.z degerleri robotu sola negatif degerleri robotu saga donduruyor.
    """
    leftwallDistance = np.min(np.array(scan.ranges[420:]))
    print "left wall distance : ", leftwallDistance
    
    angle = PID(0.7, leftwallDistance)
    print "Angle : ", angle

    move_cmd.linear.x = 0.2
    move_cmd.angular.z = angle
    cmd_vel_pub.publish(move_cmd)

def PID(desiredDistance, wallDistance):
    global integral2
    global e2
    t = 1
    kp=2.0 
    ki=0.0 
    kd=0.0
    
    e1 = wallDistance - desiredDistance
    
    integral1 = e1*t+integral2
    turev=(e1-e2)/t
    e2=e1
    integral2=integral1
    
    print "oransal : ", kp*e1
    print "integral : ", ki*integral1
    print "turev : ", kd*turev
    
    u = (kp*e1)+(ki*integral1)+(kd*turev)
    
    return u


def shutdown():
    rospy.loginfo("Stop Mybot")
    cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
    rospy.init_node('pycode', anonymous=True)
    rospy.Subscriber('/mybot/laser/scan',LaserScan,scancallback)
    
    rospy.loginfo("To Stop Mybot CTRL + C")
    rospy.on_shutdown(shutdown)
    
    cmd_vel_pub = rospy.Publisher('cmd_vel',Twist,queue_size=1)
    move_cmd = Twist()
    rospy.spin()

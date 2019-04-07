#!/usr/bin/env python
#-*-coding: utf-8 -*-

import numpy as np
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist


def scancallback(scan):
    #Lidar sagdan sola dogru lazer atıyor.
    data = [] #Data 180 derece 720 ornek
    for i in range(18):
        data.append(np.min(np.array(scan.ranges[i*40:(i+1)*40]))) # 40'ar adımlık aralık ile 18 deger aldık.

    #print "data : ", data

    mybot_control(np.array(data))

def mybot_control(data):
    if data[8:10].min() > 1.0 and data[8:10].min() < 2.0 : # Robotun onunden 80-100 derece arasına bakıyoruz.
        speed = 0.2
        if data[5:7].min() - data[11:13].min() < 0.5: # Robotun 50-70 ile 110-130 derece arasındaki farka gore robotu yonlendiriyoruz.
            print "sol"
            angle = 0.3 # Posif deger sol
        else :
            print "sag"
            angle = -0.3 # Negatif deger sag
    
    elif data[8:10].min() < 1.0: #robotun engele 1.0 den daha az mesafede ise robotu durdur.
        print "dur"
        speed = 0.0
        angle = 0.0
    
    else :
        print "duz"
        speed = 0.2
        angle = 0.0

    move_cmd.linear.x = speed
    move_cmd.angular.z = angle
    cmd_vel_pub.publish(move_cmd)

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

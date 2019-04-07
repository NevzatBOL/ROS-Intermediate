#!/usr/bin/env python
#-*-coding: utf-8 -*-

import cv2
import numpy as np
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from geometry_msgs.msg import Twist

class objectTracking():
    def __init__(self):
        rospy.init_node('objectTracking', anonymous=False)
        rospy.Subscriber('/mybot/camera1/image_raw',Image ,self.callback)

        rospy.loginfo("To stop Mytbot CTRL + C")
        rospy.on_shutdown(self.shutdown)

        self.redLower = np.array([0, 100, 100])
        self.redUpper = np.array([10, 255, 255])

        self.cmd_vel_pub= rospy.Publisher('cmd_vel', Twist, queue_size=1)
        self.move_cmd = Twist() #move_cmd objesini olusturduk.

    def callback(self, image_msg):
        bridge = CvBridge()
        image_cv = bridge.imgmsg_to_cv2(image_msg)
        self.frame = cv2.cvtColor(image_cv,cv2.COLOR_RGB2BGR)
        self.renk_filtresi()

    def renk_filtresi(self):
        hsv=cv2.cvtColor(self.frame,cv2.COLOR_BGR2HSV)

        mask=cv2.inRange(hsv,self.redLower,self.redUpper)
        mask=cv2.erode(mask,None,iterations=2)
        mask=cv2.dilate(mask,None,iterations=2)

        self.status = False

        _,cnts,_=cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts)>0:
            c=max(cnts,key=cv2.contourArea)
            ((x,y),self.radius)=cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            self.center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            if self.radius >10:
                cv2.circle(self.frame,(int(x),int(y)),int(self.radius),(0,255,255),5)
                cv2.circle(self.frame,self.center,10,(255,0,0),-1)
                self.status = True

        cv2.imshow("frame",self.frame)
        cv2.waitKey(1)
        self.mybot_control()


    def mybot_control(self):
        speed = 0
        angle = 0

        if self.status:
            if self.radius < 300:
                speed = 0.2
                angle = (400 - self.center[0]) /266.6

        self.move_cmd.linear.x = speed
        self.move_cmd.angular.z = angle
        self.cmd_vel_pub.publish(self.move_cmd)

    def shutdown(self):
        rospy.loginfo("Stop Mybot")
        self.cmd_vel_pub.publish(Twist())

if __name__ == '__main__':
    try:
        objectTracking()
        rospy.spin()
    except:
        rospy.loginfo("objetcTracking node terminated.")


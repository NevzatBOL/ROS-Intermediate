#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
from geometry_msgs.msg import Twist

class GoForward():
    def __init__(self):
        rospy.init_node('GoForward', anonymous=False)

        rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)

        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        rate = rospy.Rate(10);

        move_cmd = Twist() #move_cmd objesini olusrutduk.
        move_cmd.linear.x = 0.2 # ileri dogru git. hız: 0.2 m/s
        move_cmd.angular.z = 0 # Robotun kendi ekseni etrafında donusu. rotation: 0 radians/s

        while not rospy.is_shutdown():
            self.cmd_vel.publish(move_cmd)
            rate.sleep()

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        GoForward()
    except:
        rospy.loginfo("GoForward node terminated.")


#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *

class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)

        rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)

        #ActionClient olusturuldu
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        rospy.loginfo("wait for the action server to come up")
        #action server'in calısması icin 5sn bekleyin
        self.move_base.wait_for_server(rospy.Duration(5))

        #Robot a 3 metre ileriye dogru gitme gorevi verildi.
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'base_link'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 3.0 #3 meters
        goal.target_pose.pose.orientation.w = 1.0 #go forward

        #Robot Hedefe gonderildi.
        self.move_base.send_goal(goal)

        #gorev tamamlanana kadar 60sn bekle ve gorevin sonucunu dondur.
        success = self.move_base.wait_for_result(rospy.Duration(60)) 


        if not success:
                self.move_base.cancel_goal() #gorev basarısız olursa gorevi iptal et.
                rospy.loginfo("The base failed to move forward 3 meters for some reason")
        else:
            state = self.move_base.get_state()
            if state == GoalStatus.SUCCEEDED:
                rospy.loginfo("Hooray, the base moved 3 meters forward")


    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")

if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")


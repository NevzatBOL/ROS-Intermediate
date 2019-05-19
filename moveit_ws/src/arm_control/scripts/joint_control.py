#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import copy
import rospy
from math import pi
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
import time

class MoveGroup (object):

    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node("move_group_python")
        
        self.robot = moveit_commander.RobotCommander()
        
        scene = moveit_commander.PlanningSceneInterface()
        
        group_name = "panda_arm"
        self.group = moveit_commander.MoveGroupCommander(group_name)
        
        self.display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)
        
        planning_frame = self.group.get_planning_frame()
        print "========= Reference frame: ", planning_frame
        
        eef_link = self.group.get_end_effector_link()
        print "========= End effector: ", eef_link
        
        group_names = self.robot.get_group_names()
        print "========= Robot Groups: ",group_names
        
        print "========= Printing robot state"
        print self.robot.get_current_state()
        print ""
        
    def go_to_joint_state(self):
        joint_goal = self.group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -pi/4
        joint_goal[2] = 0
        joint_goal[3] = -pi/2
        joint_goal[4] = 0
        joint_goal[5] = pi/3
        joint_goal[6] = 0
        
        self.group.go(joint_goal, wait=True)
        
        self.group.stop()
    
    
if __name__ == "__main__":
    tutorial = MoveGroup()
    tutorial.go_to_joint_state()
    



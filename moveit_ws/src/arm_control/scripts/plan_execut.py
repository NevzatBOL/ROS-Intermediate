#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import copy
import rospy
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
        
    def plan_cartesian_path(self,scale=1):
        waypoints = []
        
        wpose = self.group.get_current_pose().pose
        wpose.position.z -= scale * 0.1
        wpose.position.y += scale * 0.2
        waypoints.append(copy.deepcopy(wpose))
        
        wpose.position.x += scale * 0.1
        waypoints.append(copy.deepcopy(wpose))
        
        wpose.position.y -= scale * 0.1
        waypoints.append(copy.deepcopy(wpose))
        
        (plan, fraction) = self.group.compute_cartesian_path(waypoints, 0.01, 0.0)
        
        return plan, fraction
        
    def display_trajectory(self, plan):
        display_trajectory = moveit_msgs.msg.DisplayTrajectory()
        display_trajectory.trajectory_start = self.robot.get_current_state()
        display_trajectory.trajectory.append(plan)
        
        self.display_trajectory_publisher.publish(display_trajectory)
    
    def execute_plan(self, plan):
        self.group.execute(plan, wait=True)
    
if __name__ == "__main__":
    tutorial = MoveGroup()
    
    rospy.loginfo("CartesianPlan")
    cartesian_plan, fraction = tutorial.plan_cartesian_path()
    time.sleep(5)
    rospy.loginfo("DisplayTrajectory")
    tutorial.display_trajectory(cartesian_plan)
    time.sleep(5)
    rospy.loginfo("Executing")
    tutorial.execute_plan(cartesian_plan)
    
    
    
    
    


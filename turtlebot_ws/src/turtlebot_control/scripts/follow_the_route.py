#!/usr/bin/env python
#-*-coding: utf-8 -*-

import rospy
import yaml
from take_photo import TakePhoto
from go_to_specific_point_on_map import GoToPose

if __name__ == '__main__':
    path = "turtlebot_ws/src/turtlebot_control/scripts/"

    # yaml dosyasını okuduk.
    with open(path+"route.yaml", 'r') as stream:
        dataMap = yaml.load(stream)

    try:
        rospy.init_node('follow_route', anonymous=False)
        navigator = GoToPose()
        camera = TakePhoto()

        for obj in dataMap:
            if rospy.is_shutdown():
                break

            name = obj['filename']

            # Navigation
            rospy.loginfo("Go to %s pose", name[:-4])
            success = navigator.goto(obj['position'], obj['quaternion'])
            if not success:
                rospy.loginfo("Failed to reach %s pose", name[:-4])
                continue
            rospy.loginfo("Reached %s pose", name[:-4])

            # Take a photo
            if camera.take_picture(path+name):
                rospy.loginfo("Saved image " + name)
            else:
                rospy.loginfo("No images received")

            rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

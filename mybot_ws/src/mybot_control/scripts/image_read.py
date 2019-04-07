#!/usr/bin/env python
import cv2
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def callback(image_msg):
    bridge = CvBridge()
    image_cv = bridge.imgmsg_to_cv2(image_msg)
    image_cv = cv2.cvtColor(image_cv,cv2.COLOR_RGB2BGR)

    #print image_cv.shape #800x800x3
    cv2.imshow("frame",image_cv)
    cv2.waitKey(1)

if __name__ == '__main__':
    rospy.init_node('cv_camera',anonymous=True)
    rospy.Subscriber('/mybot/camera1/image_raw',Image ,callback)
    rospy.spin()


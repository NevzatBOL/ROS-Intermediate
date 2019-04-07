#!/usr/bin/env python
import numpy as np
import math
import rospy
from sensor_msgs.msg import LaserScan

def scancallback(scan):
    #print "Lidar Data : ", scan

    rangesCount = len(scan.ranges)
    #print "Ranges Count : ", rangesCount
    
    #print "Scan Ranges : ", scan.ranges
    
    data = np.array(scan.ranges[:60])
    
    #print "Data : ", data
    
    #print [math.isinf(i) for i in data]
    #print np.isinf(data)
    
    print "Max Data : ", data.max()
    print "Max Index : ", data.argmax()
    
    print "Min Data : ", data.min()
    print "Min Index : ", data.argmin() 
    

if __name__ == '__main__':
    rospy.init_node('Lidar_read', anonymous=True)
    rospy.Subscriber('/mybot/laser/scan',LaserScan,scancallback)
    rospy.spin()

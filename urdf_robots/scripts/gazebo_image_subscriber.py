#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

bridge = CvBridge()

def image_callback(msg):
    try:
        cv2_img = bridge.imgmsg_to_cv2(msg, "bgr8")
    except CvBridgeError, e:
        print(e)
    else:
        arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
        arucoParams = cv2.aruco.DetectorParameters_create()
        (corners, ids, rejected) = cv2.aruco.detectMarkers(cv2_img, arucoDict, parameters=arucoParams)
        if np.all(ids is not None):
            cv2.aruco.drawDetectedMarkers(cv2_img, corners, ids)
        cv2.imshow('gazebo_show', cv2_img)
        cv2.waitKey(10)


def listener():
    rospy.init_node('gazebo_img', anonymous = False)
    sub = rospy.Subscriber('/gazebo_cam1/gazebo_image1', Image, image_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

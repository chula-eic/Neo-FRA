#!/usr/bin/env python3
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import rospy
from std_msgs.msg import String
import numpy as np

camera = PiCamera()
camera.resolution = (320, 240)
rawCapture = PiRGBArray(camera)


def color_checker():
    pub = rospy.Publisher('color', String, queue_size=10)
    rospy.init_node('color_checker', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    while not rospy.is_shutdown():
        color = check_color()
        pub.publish(color)
        rate.sleep()


def check_color():
    global camera
    global rawCapture
    frame = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(frame, format="bgr")
    channel = frame[119,159,:]
    b = channel[0]
    g = channel[1]
    r = channel[2]
    color = "red"
    return color
    
if __name__ == '__main__' :
    try :
        color_checker()
    except rospy.ROSInterruptException:
        pass

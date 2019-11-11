
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import rospy
from std_msgs.msg import String
from cru_robot.msg import Float


camera = PiCamera()
rawCapture = PiRGBArray(camera)

def color_checker():
    pub = rospy.Publisher('color', String, queue_size=10)
    rospy.init_node('color_checker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        color = check_color()
        pub.publish(color)
        rate.sleep()


def check_color():
    global camera
    global rawCapture
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    channel = rawCapture.array[x,y,:]
    b = channel[0]
    g = channel[0]
    r = channel[0]
    return [r,g,b]
    
if __name__ == '__main__' :
    try :
        color_checker()
    except rospy.ROSInterruptException:
        pass
        
    

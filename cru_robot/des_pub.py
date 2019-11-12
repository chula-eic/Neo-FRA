#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from cru_robot.msg import FloatList


pub = rospy.Publisher('destination', FloatList, queue_size=10)
servo_pub = rospy.Publisher('servo', String, queue_size=10)
queue = [];  #DECLARE QUEUE/FLOATLIST QUEUE HERE
state = 0
def callback(data):
	global pub
	global queue
	global state
	if state == 0 :
		if data.data == "red":
			queue = [[0,0],[1,1],[2,2]] #INSERT RED HERE
		elif data.data == "blue":
			queue = [[3,3]] #INSERT POS HERE
		elif data.data == "green":
			queue = [[4,4]] #INSERT POS HERE
		elif data.data == "yellow":
			queue = [[5,5]] #INSERT POS HERE
		state = 1
	if state == 1:
            pub.publish(queue[-1])


def feedback(data):
    global pub
    global queue
    if data.data == "1":
        if len(queue) > 0 : 
	    pub.publish(queue.pop())
        else:
	    servo_pub.publish("1")
            print("Destinatoin Reached")
    else:
        print("FAILED")
        
def des_pub():
    rospy.init_node('des_pub', anonymous=True)
    rospy.Subscriber("color", String, callback)
    rospy.Subscriber("Feedback", String, feedback)

    rospy.spin()

if __name__ == '__main__':
    try:
        des_pub()
    except rospy.ROSInterruptException:
        pass

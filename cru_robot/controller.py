#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from cru_robot.msg import FloatList

pub = rospy.Publisher('desfeedback', String, queue_size = 10)
destination = []
def callback(data):
	global pub
	global destination
	print("read ",data.data)
	destination = data.data
	while(not reached):
		#calculate velocity
		#send serial
	pub.publish('1')

def controller():
	rospy.init_node('controller',anonymous = True)
	rospy.Subscriber('destination',FloatList,callback)
	rospy.spin()

if __name__ == '__main__':
	try:
		controller()
	except rospy.ROSInterruptException:
		pass

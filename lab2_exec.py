#!/usr/bin/env python

import copy
import time
import rospy
import numpy as np
from lab2_header import *
import sys

# 20Hz
SPIN_RATE = 20 

# UR3 home location
home = np.radians([175.25, -82.18, 82.86, -91.67, -90.04, 79.68])

# UR3 current position, using home position for initialization
current_position = copy.deepcopy(home)


############## Your Code Starts Here ##############


Q11 = np.radians([160.03,-43.95,87.38,-127.45,-92.30,64.85])
Q12 = np.radians([158.35, -49.89, 90.96, -127.41, -87.01, 65.22])
Q13 = np.radians([159.09, -54.0, 89.4, -123.86, -88.54, 63.39])
Q21 = np.radians([176.24, -43.49, 93.49, -141.65, -88.79, 84.1])
Q22 = np.radians([175.23, -48.97, 89.96, -128.71, -87.63, 77.02])
Q23 = np.radians([175.27, -54.4, 92.1, -128.8, -87.58, 79.42])
Q31 = np.radians([190.48, -38.58, 82.64, -135.88, -88.48, 86.08])
Q32 = np.radians([190.46, -44.03, 85.19, -135.67, -88.53, 86.08])
Q33 = np.radians([190.47, -47.15, 76.33, -117.9, -88.53, 86.08])

### Hint: How can you map this array to the towers?
Q = [ [Q11, Q12, Q13], \
      [Q21, Q22, Q23], \
      [Q31, Q32, Q33] ]

















############### Your Code Ends Here ###############


thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

digital_in_0 = 0
analog_in_0 = 0

suction_on = True
suction_off = False

current_io_0 = False
current_position_set = False

current_digin = False ###


############## Your Code Starts Here ##############

"""
TODO: define a ROS topic callback funtion for getting the state of suction cup
Whenever ur3/gripper_input publishes info this callback function is called.
"""
def succ_callback(msg):
	global current_digin

	current_digin= msg.DIGIN

















############### Your Code Ends Here ###############


"""
Whenever ur3/position publishes info, this callback function is called.
"""
def position_callback(msg):

	global thetas
	global current_position
	global current_position_set

	thetas[0] = msg.position[0]
	thetas[1] = msg.position[1]
	thetas[2] = msg.position[2]
	thetas[3] = msg.position[3]
	thetas[4] = msg.position[4]
	thetas[5] = msg.position[5]

	current_position[0] = thetas[0]
	current_position[1] = thetas[1]
	current_position[2] = thetas[2]
	current_position[3] = thetas[3]
	current_position[4] = thetas[4]
	current_position[5] = thetas[5]

	current_position_set = True


def gripper(pub_cmd, loop_rate, io_0):

	global SPIN_RATE
	global thetas
	global current_io_0
	global current_position

	error = 0
	spin_count = 0
	at_goal = 0

	current_io_0 = io_0

	driver_msg = command()
	driver_msg.destination = current_position
	driver_msg.v = 1.0
	driver_msg.a = 1.0
	driver_msg.io_0 = io_0   
	pub_cmd.publish(driver_msg)

	while(at_goal == 0):

		if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
			abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
			abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
			abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
			abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
			abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

			at_goal = 1
		
		loop_rate.sleep()


		if(spin_count >  SPIN_RATE*5):

			pub_cmd.publish(driver_msg)
			rospy.loginfo("Just published again driver_msg")
			spin_count = 0

		spin_count = spin_count + 1

	return error


def move_arm(pub_cmd, loop_rate, dest, vel, accel):

	global thetas
	global SPIN_RATE

	error = 0
	spin_count = 0
	at_goal = 0

	driver_msg = command()
	driver_msg.destination = dest
	driver_msg.v = vel
	driver_msg.a = accel
	driver_msg.io_0 = current_io_0
	pub_cmd.publish(driver_msg)

	loop_rate.sleep()

	while(at_goal == 0):

		if( abs(thetas[0]-driver_msg.destination[0]) < 0.0005 and \
			abs(thetas[1]-driver_msg.destination[1]) < 0.0005 and \
			abs(thetas[2]-driver_msg.destination[2]) < 0.0005 and \
			abs(thetas[3]-driver_msg.destination[3]) < 0.0005 and \
			abs(thetas[4]-driver_msg.destination[4]) < 0.0005 and \
			abs(thetas[5]-driver_msg.destination[5]) < 0.0005 ):

			at_goal = 1
			#rospy.loginfo("Goal is reached!")
		
		loop_rate.sleep()

		if(spin_count >  SPIN_RATE*5):

			pub_cmd.publish(driver_msg)
			rospy.loginfo("Just published again driver_msg")
			spin_count = 0

		spin_count = spin_count + 1

	return error


############## Your Code Starts Here ##############

def move_block(pub_cmd, loop_rate, start_loc, start_height, \
	           end_loc, end_height):
	global Q
	global home	
	print(end_loc, end_height)
	print(Q[end_loc][end_height])
	### Hint: Use the Q array to map out your towers by location and height.
	
	error = 0

	#move_arm(pub_cmd, loop_rate, dest, vel, accel):
	move_arm(pub_cmd, loop_rate, home, 4, 4)
	move_arm(pub_cmd, loop_rate, Q[start_loc][start_height], 4, 4)
	gripper(pub_cmd, loop_rate, 1)
	loop_rate.sleep()
	loop_rate.sleep()
	loop_rate.sleep()
	if current_digin != 1:
		gripper(pub_cmd, loop_rate, 0)
		move_arm(pub_cmd, loop_rate, home, 4, 4)
		error = 1
		return error	
	move_arm(pub_cmd, loop_rate, home, 4, 4)
	move_arm(pub_cmd, loop_rate, Q[end_loc][end_height], 4, 4)
	gripper(pub_cmd, loop_rate, 0)
	move_arm(pub_cmd, loop_rate, home, 4, 4)
	
	return error


def solveHanoiTower(start, intermediate, end, pub_cmd, loop_rate):
	if move_block(pub_cmd, loop_rate, start, 2, end, 0) == 1:
		return
	if move_block(pub_cmd, loop_rate, start, 1, intermediate, 0) == 1:
		return
	if move_block(pub_cmd, loop_rate, end, 0, intermediate, 1) == 1:
		return
	if move_block(pub_cmd, loop_rate, start, 0, end, 0) == 1:
		return
	if move_block(pub_cmd, loop_rate, intermediate, 1, start, 0) == 1:
		return
	if move_block(pub_cmd, loop_rate, intermediate, 0, end, 1) == 1:
		return
	if move_block(pub_cmd, loop_rate, start, 0, end, 2) == 1:
		return

	
















############### Your Code Ends Here ###############


def main():

	global home
	global Q
	global SPIN_RATE

	# Initialize ROS node
	rospy.init_node('lab2node')

    # Initialize publisher for ur3/command with buffer size of 10
	pub_command = rospy.Publisher('ur3/command', command, queue_size=10)

	# Initialize subscriber to ur3/position and callback fuction
	# each time data is published
	sub_position = rospy.Subscriber('ur3/position', position, position_callback)

	############## Your Code Starts Here ##############
	# TODO: define a ROS subscriber for ur3/gripper_input message and corresponding callback function

	sub_gripper_input = rospy.Subscriber('ur3/gripper_input', gripper_input, succ_callback)




	loop_rate = rospy.Rate(SPIN_RATE)




	############### Your Code Ends Here ###############


	############## Your Code Starts Here ##############
	# TODO: modify the code below so that program can get user input

	input_done = 0
	loop_count = 0

	while(not input_done):
		start = raw_input("Enter the start (between 0 and 2, 3 to quit) ")
		if (int(start) == 3):
			print("Quitting... ")
			sys.exit()
		if((int(start) != 0 and int(start) != 1 and int(start) != 2)):
			print("enter valid start")
			input_done = 0
			continue
		
		print("you entered " + start + "\n")
		
		end = raw_input("Enter the end ")
		if(int(end) == 3 ):
			print("Quitting... ")
			sys.exit()	
		if((int(end) != 0 and int(end) != 1 and int(end) != 2)):
			print("enter valid end")
			input_done = 0
			continue
	        
		print("You entered " + end + "\n")	
		

		if (start == end):
			print("start and end have to be different")
			input_done = 0
			continue

		input_done =1
	













	############### Your Code Ends Here ###############

	# Check if ROS is ready for operation
	while(rospy.is_shutdown()):
		print("ROS is shutdown!")

	rospy.loginfo("Sending Goals ...")

	loop_rate = rospy.Rate(SPIN_RATE)

	############## Your Code Starts Here ##############
	# TODO: modify the code so that UR3 can move a tower to a new location according to user input

	choice = [0, 1, 2]
	choice.remove(int(start))
	choice.remove(int(end))
	intermediate = choice[0]
	solveHanoiTower(int(start), intermediate, int(end), pub_command, loop_rate)
#	print(move_block(pub_command, loop_rate, 0, 2, 1, 0))


	############### Your Code Ends Here ###############



if __name__ == '__main__':
	
	try:
		main()
    # When Ctrl+C is executed, it catches the exception
	except rospy.ROSInterruptException:
		pass


	







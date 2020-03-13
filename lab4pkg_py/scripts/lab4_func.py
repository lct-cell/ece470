#!/usr/bin/env python
import numpy as np
from scipy.linalg import expm
from lab4_header import *

"""
Use 'expm' for matrix exponential.
Angles are in radian, distance are in meters.
"""

def Get_MS():
	# =================== Your code starts here ====================#
	# Fill in the correct values for S1~6, as well as the M matrix
	M = np.eye(4)
	S = np.zeros((6,6))
	M = np.array([[0, -1, 0, 0.55], [0, 0, -1, 0.27], [1, 0, 0, 0.21], [0, 0, 0, 1]])
	S = np.array([[0, 0, 0, 0, 1, 0], [0, 1, -1, 1, 0, 1], [1, 0, 0, 0, 0, 0], [0, -0.16, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, -0.25, 0.45, -0.12, 0.55]])




	
	# ==============================================================#
	return M, S


"""
Function that calculates encoder numbers for each motor
"""
def s_to_S(s):
	S = np.array([[0, -s[2], s[1], s[3]], [s[2], 0, -s[0], s[4]], [-s[1], s[0], 0, s[5]], [0, 0, 0, 0]])
	return S

def lab_fk(theta1, theta2, theta3, theta4, theta5, theta6):

	# Initialize the return_value 
	return_value = [None, None, None, None, None, None]

	# =========== Implement joint angle to encoder expressions here ===========
	print("Foward kinematics calculated:\n")

	# =================== Your code starts here ====================#
	theta = np.array([theta1,theta2,theta3,theta4,theta5,theta6])
	T = np.eye(4)

	M, S = Get_MS()

	S1 = s_to_S(S[:,0])
	S2 = s_to_S(S[:,1])
	S3 = s_to_S(S[:,2])
	S4 = s_to_S(S[:,3])
	S5 = s_to_S(S[:,4])
	S6 = s_to_S(S[:,5])
	T = M*expm(S1*theta1)*expm(S2*theta2)*expm(S3*theta3)*expm(S4*theta4)*expm(S5*theta5)*expm(S6*theta6)






	# ==============================================================#
	
	print(str(T) + "\n")

	return_value[0] = theta1 + PI
	return_value[1] = theta2
	return_value[2] = theta3
	return_value[3] = theta4 - (0.5*PI)
	return_value[4] = theta5
	return_value[5] = theta6

	return return_value




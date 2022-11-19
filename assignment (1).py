from __future__ import print_function

import time
from sr.robot import *

R = Robot()
a_th = 1.5 # The threshold for controlling the linear distance
d_th = 0.4 # The threshold for controlling the orientation

def drive(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

def turn(speed, seconds):
	R.motors[0].m0.power = speed
	R.motors[0].m1.power = -speed
	time.sleep(seconds)
	R.motors[0].m0.power = 0
	R.motors[0].m1.power = 0

Silver_Codes = [] # list of silver tokens codes that are grabbed.
Golden_Codes = [] # list of golden tokens codes that are paired.

#The following function searches for silver tokens and checks if the token code is already stored in the Silver_Codes list, Which means that the token is already grabbed, so it doesn't grab it and look for another token.
def find_ungrabbed_silver_token(): 
	dist=100
	for token in R.see(): 
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and token.info.code not in Silver_Codes:
			dist=token.dist
			rot_y=token.rot_y
			Token_Codes=token.info.code
	if dist==100:
		return -1, -1 ,-1
	else:    
		return dist, rot_y, Token_Codes

#The following function searches for golden tokens and checks if the token code is already paired in the Golden_Codes list, which means that the token is already paired, so it looks for another golden token.
def find_unpaired_golden_token():

	dist=100
	for token in R.see(): 
		if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and token.info.code not in Golden_Codes:
			dist=token.dist
			rot_y=token.rot_y
			Token_Codes=token.info.code
	if dist==100:
		return -1, -1, -1
	else:
		
		return dist, rot_y, Token_Codes

#This function simply returns +1 or -1 depending on the sign of (a).
def sign(a):
	if a < 0:
		return -1
	else:
		return 1

#This function takes the checked silver box to the checked golden box.
def put_silver_with_golden():
	while (len(Golden_Codes)<7):
		dist, rot_y, Token_Codes = find_ungrabbed_silver_token() #Searching for ungrabbed silver tokens first.
		if dist==-1:
		    turn(10,0.1)
		    continue
		while(dist<0):   #If the robot doesn't find any token, we make it turn until it does.
			turn(-5,0.01)
			dist, rot_y, Token_Codes = find_ungrabbed_silver_token()
		#allign orientation of the robot.
		while (rot_y >= a_th or rot_y<=-a_th) : 
			turn(sign(rot_y-a_th) * 10,0.001) #I used the sign to make the robot turn with the right orientation
			dist, rot_y,Token_Codes = find_ungrabbed_silver_token()
		#The following while loop drives the robot to the desired ungrabbed silver box
		while (dist >= d_th) : 
			drive(30,0.01)
			dist, rot_y, Token_Codes = find_ungrabbed_silver_token()
	    	Silver_Codes.append(Token_Codes)
	    	print("Found you silver box number:",len(Silver_Codes))
	    	R.grab()
	    	turn(20,0.1)
		print("Let's pair you with an unpaired golden box!")
		#Now, The robot tries to find the closest unpaired golden box by calling the previously declared function
		dist, rot_y, Token_Codes = find_unpaired_golden_token()
		#The following loop takes every ungrabbed silver box to the closest unpaired golden box until no pairs left.
		while(dist<0):
			turn(-5,0.01)
			dist, rot_y, Token_Codes = find_unpaired_golden_token()
	    	while (rot_y >= a_th or rot_y<=-a_th) :
			turn(sign(rot_y-a_th) * 10,0.001)
			dist, rot_y, Token_Codes= find_unpaired_golden_token()
	    	while (dist >= 1.5*d_th) :
			drive(40,0.01)
			dist, rot_y, Token_Codes= find_unpaired_golden_token()
	    	R.release()
	    	Golden_Codes.append(Token_Codes)
	    	print("Gotcha golden box number:",len(Golden_Codes))
	    	drive(-50,0.8)
		#The following if loop checks whether the golden boxes codes reached the limit (6).
		if (len(Golden_Codes)==6):
			print("Task completed")
			exit() 
			
put_silver_with_golden()

   	
  
	


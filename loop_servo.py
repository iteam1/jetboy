from adafruit_servokit import ServoKit
import time 

# initializ the your servo kit 
kit = ServoKit(channels = 16)

while True:
	for i in range(0,160,1):
		kit.servo[0].angle = i # set the angle for servo kit
		time.sleep(0.1)

	for i in range(160,0,-1):
		kit.servo[0].angle = i 
		time.sleep(0.1)
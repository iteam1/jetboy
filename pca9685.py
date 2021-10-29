import time 
from adafruit_servokit import ServoKit

kit = ServoKit(channels = 16)

while True:
	print(" PCA9685 is running!")
	for i in range(0,180):
		kit.servo[0].angle = i
		kit.servo[1].angle = i
		kit.servo[2].angle = i
		kit.servo[3].angle = i
		time.sleep(0.05)

	for i in range(180,0,-1):
		kit.servo[0].angle = i
		kit.servo[1].angle = i
		kit.servo[2].angle = i
		kit.servo[3].angle = i
		time.sleep(0.5)

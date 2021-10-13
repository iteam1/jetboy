# control PCA9685 board
# pip3 install adafruit-circuitpython-servokit
import time 
from adafruit_servokit import ServoKit

kit = ServoKit(channels = 16)

kit.servo[0].angle = 90
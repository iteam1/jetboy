import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15,GPIO.IN)

while True:
	x = GPIO.input(15) # 3.3v = 1; 0v = 0
	print(x)
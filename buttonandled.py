import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15,GPIO.IN)
GPIO.setup(23,GPIO.OUT)

while True:
	x= GPIO.input(15)
	if x == 1:
		print("LED ON")
		GPIO.output(23,1)
	else:
		print("LED OFF")
		GPIO.output(23,0)
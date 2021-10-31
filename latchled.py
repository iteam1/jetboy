import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15,GPIO.IN)
GPIO.setup(23,GPIO.OUT)

old_state = 1
led_state = 0

while True:
	
	new_state = GPIO.input(15)
	GPIO.output(23,led_state)

	if new_state != old_state:
		led_state  = not(led_state)
		old_state = new_state


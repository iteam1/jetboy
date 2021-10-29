# confguring the 40-pin expand header
# sudo /opt/nvidia/jetson-io/jetson-io.py
# full duty = 3.3

import RPi.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BOARD)

GPIO.setup(33,GPIO.OUT)

my_pwm = GPIO.PWM(33,100) # can not change the setup while running

my_pwm.start(0)


while True:
	print('Runing')
	for i in range(100):
		my_pwm.ChangeDutyCycle(i) #my_pwm.ChangeFrequency(100)
		print(i)
		time.sleep(0.5)

	for i in range(100,0,-1):
		my_pwm.ChangeDutyCycle(i)
		print(i)
		time.sleep(0.5)

#GPIO.cleanup()








'''
Author: locchuong
Updated: 27/12/21
Description:
	This python program read GPIO pins connected to the ultra sensor signal and print it out
'''
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

GPIO.setup(15,GPIO.IN)
GPIO.setup(16,GPIO.IN)
GPIO.setup(18,GPIO.IN)
GPIO.setup(19,GPIO.IN)

while True:

	f= GPIO.input(15)
	b= GPIO.input(16)
	l= GPIO.input(18)
	r= GPIO.input(19)

	print(f"f = {f},b = {b},l = {l},r = {r}")
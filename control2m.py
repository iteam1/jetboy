import RPi.GPIO as gpio
import time

L_lpwm = 31
L_rpwm = 33

R_lpwm = 35
R_rpwm = 37

def begin():
	gpio.setmode(gpio.BOARD)
	
	gpio.setup(L_lpwm,gpio.OUT)
	gpio.setup(L_rpwm,gpio.OUT)
	gpio.setup(R_lpwm,gpio.OUT)
	gpio.setup(R_rpwm,gpio.OUT)
	
	gpio.output(L_lpwm,1)
	gpio.output(L_rpwm,1)
	gpio.output(R_lpwm,1)
	gpio.output(R_rpwm,1)

def stop():
	gpio.output(L_lpwm,1)
	gpio.output(L_rpwm,1)
	gpio.output(R_lpwm,1)
	gpio.output(R_rpwm,1)

def forward():
	gpio.output(L_lpwm,1)
	gpio.output(L_rpwm,0)
	gpio.output(R_lpwm,1)
	gpio.output(R_rpwm,0)

def backward():
	gpio.output(L_lpwm,0)
	gpio.output(L_rpwm,1)
	gpio.output(R_lpwm,0)
	gpio.output(R_rpwm,1)

def left():
	gpio.output(L_lpwm,1)
	gpio.output(L_rpwm,0)
	gpio.output(R_lpwm,0)
	gpio.output(R_rpwm,1)

def right():
	gpio.output(L_lpwm,0)
	gpio.output(L_rpwm,1)
	gpio.output(R_lpwm,1)
	gpio.output(R_rpwm,0)

def loop():
	while True:
		mode = input("x=exit,f=go,b=back,l=left,r=right,t=stop: ")
		if mode == "x":
			print("Clean up and exit.")
			gpio.cleanup()
			break
		elif mode == "t":
			print("Stop.")
			stop()
		elif mode == "f":
			print("Go forward.")
			forward()
		elif mode == "b":
			print("Go backward.")
			backward()
		elif mode == "l":
			print("Turn left.")
			left()
		elif mode == "r":
			print("Turn right.")
			right()
		else:
			pass

if __name__ == "__main__":
	begin()
	loop()
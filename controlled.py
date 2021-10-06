import RPi.GPIO as GPIO

def main():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(11,GPIO.OUT)

def loop():
	while True:
		mode = int(input("Control LED (0 = OFF, 1 = ON): "))
		if mode == 0 :
			GPIO.output(11,0)
		elif mode == 1 :
			GPIO.output(11,1)
		else:
			pass

if __name__ == "__main__":
  main()
  loop()


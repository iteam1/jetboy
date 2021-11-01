from controller import MotorController
import RPi.GPIO 
import time 

if __name__ == "__main__":

	controller = MotorController()

	print("Control Robot via Command Line!")

	while True:

		command = input("Enter your command: ")

		if command == "x":
			print("Stop motor & Clean up")
			controller.stop()
			RPi.GPIO.cleanup()
			break

		elif command == "w":
			print("Forward")
			controller.forward()

		elif command == "s":
			print("Backward")
			controller.backward()

		elif command == "a":
			print("Turn left")
			controller.turnleft()

		elif command == "d":
			print("Turn Right")
			controller.turnright()

		else:
			print("Command does not Exist!")
			pass

	print("Exit cml")













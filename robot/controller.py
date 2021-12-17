'''
Contain a class to interface with robot's hardware
cml_l.py import this module
'''
import RPi.GPIO  

# name control pins
ML_DIR = 24 # motor left direction
ML_RUN = 23 # motor left run
MR_DIR = 22 # motor right direction
MR_RUN = 21 # motor right run

class MotorController():
	
	def __init__(self,ML_DIR = ML_DIR,ML_RUN = ML_RUN
						,MR_DIR = MR_DIR,MR_RUN = MR_RUN,GPIO=RPi.GPIO):
		
		self.ML_DIR = ML_DIR
		self.ML_RUN = ML_RUN
		self.MR_DIR = MR_DIR
		self.MR_RUN = MR_RUN
		self.GPIO = GPIO

		#initialize gpio
		self.GPIO.setmode(GPIO.BOARD)

		self.GPIO.setup(self.ML_DIR,GPIO.OUT)
		self.GPIO.setup(self.ML_RUN,GPIO.OUT)
		self.GPIO.setup(self.MR_DIR,GPIO.OUT)
		self.GPIO.setup(self.MR_RUN,GPIO.OUT)

		# block motors run by EN pins
		self.GPIO.output(self.MR_RUN,0)
		self.GPIO.output(self.ML_RUN,0)

		# set dir to equal
		# block motors run by EN pins
		self.GPIO.output(self.MR_DIR,0)
		self.GPIO.output(self.ML_DIR,0)

	def stop(self):
		self.GPIO.output(self.MR_RUN,0)
		self.GPIO.output(self.ML_RUN,0)

	def forward(self):
		self.stop()
		self.GPIO.output(self.MR_RUN,1)
		self.GPIO.output(self.ML_RUN,1)
		self.GPIO.output(self.MR_DIR,1)
		self.GPIO.output(self.ML_DIR,1)

	def backward(self):
		self.stop()
		self.GPIO.output(self.MR_RUN,1)
		self.GPIO.output(self.ML_RUN,1)
		self.GPIO.output(self.MR_DIR,0)
		self.GPIO.output(self.ML_DIR,0)

	def turnleft(self):
		self.stop()
		self.GPIO.output(self.MR_RUN,1)
		self.GPIO.output(self.ML_RUN,1)
		self.GPIO.output(self.MR_DIR,1)
		self.GPIO.output(self.ML_DIR,0)

	def turnright(self):
		self.stop()
		self.GPIO.output(self.MR_RUN,1)
		self.GPIO.output(self.ML_RUN,1)
		self.GPIO.output(self.MR_DIR,0)
		self.GPIO.output(self.ML_DIR,1)

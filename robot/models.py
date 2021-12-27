'''
Author: locchuong
Updated: 27/12/21
Description:
	Models for flask server containt Robot class for create a object add to database
'''
from robot import db

class Robot(db.Model):
	
	# For moving
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')

	# Estop and sensors
	estop = db.Column(db.Boolean,default = False,nullable = False)
	obs_f = db.Column(db.Boolean,default = False,nullable = False)
	obs_b = db.Column(db.Boolean,default = False,nullable = False)
	obs_l = db.Column(db.Boolean,default = False,nullable = False)
	obs_r = db.Column(db.Boolean,default = False,nullable = False)

	# For display
	content = db.Column(db.String(),nullable = False, default = 'Good days') # The sentece will display on robot window
	emotion = db.Column(db.String(),nullable = False,default = 'happyblink') # The emotion will display on robot window
	image = db.Column(db.String(),nullable = False,default = 'simplesmileblink') # The emotion will display on robot window
	itype = db.Column(db.String(),nullable = False, default = 'emo') # emo = gif,img, info

	def __repr__(self):
		return f"{self.name}: {self.command}"


from robot import db

class Robot(db.Model):
	
	# for moving
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')

	#for display
	content = db.Column(db.String(),nullable = False, default = 'Good days') # The sentece will display on robot window
	emotion = db.Column(db.String(),nullable = False,default = 'happyblink') # The emotion will display on robot window
	image = db.Column(db.String(),nullable = False,default = 'simplesmile') # The emotion will display on robot window
	itype = db.Column(db.String(),nullable = False, default = 'emo') # emo = gif,img, info

	def __repr__(self):
		return f"{self.name}: {self.command}"


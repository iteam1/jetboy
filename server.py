from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Robot(db.Model):
	
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')

	def __repr__(self):
		return f"{self.name}: {self.command}"

@app.route("/",methods = ['GET'])
def base():
	return render_template('base.html')

@app.route("/command/1",methods = ['POST'])
def move():
	command = request.form.get('command')
	robot = Robot.query.get(1)
	robot.command = command 
	db.session.commit()
	print(robot)
	return render_template('base.html')


if __name__ == "__main__":
	app.run(debug = True,host= '192.168.1.12',port ='5000')

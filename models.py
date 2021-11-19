from flask import Flask,render_template,request,Response,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b9fed3b85a77047fc95896683ee6713'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Robot(db.Model):
	
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(30),nullable = False,unique = True)
	command = db.Column(db.String(30),nullable = False,default = 'stop')
	face = db.Column(db.Integer,nullable = False,default =0)

	def __repr__(self):
		return f"{self.name}: {self.command}"


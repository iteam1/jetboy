'''
Initialize 
	Database
	App
Connect camera d455
'''
from flask import Flask   
from flask_sqlalchemy import SQLAlchemy  
import robot.realsense_depth as rd

app = Flask(__name__)
app.config['SECRET_KEY'] = '3b9fed3b85a77047fc95896683ee6713'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

# Can not detect camera after server on
d455 = rd.DepthCamera() 

from robot import routes
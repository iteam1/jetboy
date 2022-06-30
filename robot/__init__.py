'''
Author: locchuong
Updated: 27/12/21
Description:
	- Initialize: 
		+ Database
		+ App
	- Connect camera d455
'''
from flask import Flask   
from flask_sqlalchemy import SQLAlchemy  
import robot.realsense_depth as rd
from robot.pyrealsense2 import pyrealsense2 as rs # run from path "./"

# flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '3b9fed3b85a77047fc95896683ee6713'    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# connect to database
db = SQLAlchemy(app)

# Can not detect camera after server on
d455 = rd.DepthCamera() 

# declare pointcloud object
pc = rs.pointcloud()
# declare points object
points = rs.points()
# declare colorizer to generate texture for our ply
colorizer = rs.colorizer()

# run route
from robot import routes
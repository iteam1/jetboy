### generate database

- step1: `gendata.py` (if there is no database)
- step2: create data

		python3
		from robot import db
		from robot.models import Robot
		robot = Robot()
		db.create_all()
		db.session.add(robot)
		db.session.commit()
		exit()
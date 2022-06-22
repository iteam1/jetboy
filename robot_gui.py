'''
Author: locchuong
Updated: 27/12/21
Description:
	This python program display robot's GUI by tkinter
	These ones in the robot database will be use:

	1/ id: is the robot id (primary key)
	2/ name: robot's name

	# Control robot's GUI display on the screen

	4/ content: the sentence content will display on the robot screen for TEXT,WORDS DISPLAY
	5/ emotion: the name of gif image will display on the robot screen for GIF,EMOTION DISPLAY
	6/ image: the name of the image will display on the robot screen for IMAGE DISPLAY
	7/ itype: the content's type will display on the robot
		value:
			- info: display content on the screen
			- emo: display emotion or gif on the screen
			- img: display the image on the screen

	This program continously read the database and display it
'''
import tkinter 
from PIL import Image,ImageTk,ImageSequence
import os 
import sqlite3 

class App:
	'''
	Create App class 
	'''
	def __init__(self,parent,width = 1024,height = 600,path = './robot/static/face/huma/'):
		self.parent = parent # This is root window
		self.path = path # the path lead to gif, images,... of the robot
		self.width = width  # Screen's width
		self.height = height # Screen's height
		self.canvas = tkinter.Canvas(parent,width = self.width,height = self.height) # Create a canvas object for drawing
		self.sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(self.path + 'happyblink' +'.gif'))] # Split the gif and turn it into sequence object
		self.canvas.pack() # Pack the canvas into tkinter window
		
		self.animate(1) # Start the animate function with the index = 1 

	def dbconnect(self):
		'''
		Read into database, find out what kind of message we want to display then read the corresponding content
		'''
		self.conn = sqlite3.connect("./robot/site.db")
		c = self.conn.cursor()
		c.execute(f"SELECT *FROM robot WHERE id = 1") # fetch the robot id = 1
		itype = c.fetchone()[6] # read the kind of message first
		# find out the corresponding content
		if itype == 'emo':
			c.execute(f"SELECT *FROM robot WHERE id = 1")
			content = c.fetchone()[4] # read column emotion in the database
			self.conn.commit()
			return itype, content # return the inforamtion type and content is the name of the gif
		elif itype == 'info':
			c.execute(f"SELECT *FROM robot WHERE id = 1")
			content = c.fetchone()[3] # read column content in the database
			self.conn.commit()
			return itype,content # return the itype and content is the content of the sentence
		elif itype == 'img':
			c.execute(f"SELECT *FROM robot WHERE id = 1")
			content = c.fetchone()[5] # read the image's name in the database
			self.conn.commit()
			return itype,content # return the itype and content si the image's name  
		else:
			return None

	def animate(self,counter,stime = 50):
		'''
		Display on screen the content of massage
		'''
		itype,item = self.dbconnect()

		if itype == 'info':
			self.canvas.delete("all") # clear canvas before draw something new
			content = tkinter.Label(self.parent,text = item,fg = 'black',font= ('Arial',30))
			self.canvas.create_window(312,250,anchor = 'nw',window = content)
			self.parent.after(stime, lambda: self.animate(0))

		elif itype == 'emo':
			self.canvas.delete("all")
			self.sequence = [ImageTk.PhotoImage(img.resize(((self.width),(self.height)))) for img in ImageSequence.Iterator(Image.open(self.path + item +'.gif'))]
			self.image = self.canvas.create_image(512,300,image= self.sequence[0])
			try:
				self.canvas.itemconfig(self.image, image = self.sequence[counter])
			except:
				pass
			self.parent.after(stime,lambda: self.animate((counter+1)%len(self.sequence)))

		elif itype == 'img':
			self.canvas.delete("all")
			img = Image.open(self.path + item +'.png')
			img = img.resize(((self.width),(self.height)))
			self.image = ImageTk.PhotoImage(img)
			self.canvas.create_image(0,0,anchor = 'nw',image = self.image)
			self.parent.after(stime, lambda: self.animate(0))

if __name__ == '__main__':

	root = tkinter.Tk() # Create a tkinter window 

	app = App(root) # Create a app object by app class

	print("robot GUI created!")

	root.mainloop() # continously run the  program

	print("robot GUI closed!")
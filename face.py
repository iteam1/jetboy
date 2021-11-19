# Display a gif image by tkinter for robot's GUI
import tkinter
from PIL import Image, ImageTk, ImageSequence
import os
import sqlite3   

gif_dir = './static/face/huma/' # directory of the gifs
# Get the list of gif image
gif_list = []
for i in os.listdir(gif_dir):
	if i[-3:] == 'gif':
		gif_list.append(i)

# Create a class inheritate from  root tkinter
class App:
	def __init__(self,parent):
		self.parent =parent
		
		# Create a canvas for tkinter app
		self.canvas = tkinter.Canvas(parent,width = 1024,height = 600)
		self.canvas.pack() # pack this canvas into your tkinter

		self.animate(1) # Function to display frame by frame, without this after can not loop

	def animate(self,counter,time_inter =100):

		# Create the connection to database
		conn = sqlite3.connect("site.db")
		c = conn.cursor()
		c.execute(f"SELECT *FROM robot WHERE id = 1")
		self.face = c.fetchone()[-1]
		conn.commit()

		# Create a list of tkinter image for display it frame by frame
		self.sequence = [ImageTk.PhotoImage(img)
							for img in ImageSequence.Iterator(Image.open(gif_dir+gif_list[self.face]))]
		
		# Create a image for display on canvas, start with the frame zero of sequence
		self.image = self.canvas.create_image(512,300,image=self.sequence[0])
		
		# Maybe crash a bit in this function if you change face number This animate function will run continously
		try:
			self.canvas.itemconfig(self.image,image= self.sequence[counter])
		except:
			pass
		
		# increate the counter frame after time_inter, this function after make 
		self.parent.after(time_inter,lambda:self.animate((counter+1)%len(self.sequence)))

root = tkinter.Tk()
app = App(root)
root.mainloop()
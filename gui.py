# Display a gif image by tkinter for robot's GUI
import tkinter
from PIL import Image, ImageTk, ImageSequence 

file = './static/face/huma/happyblink.gif'

# Create a class inheritate from  root tkinter
class App:
	def __init__(self,parent):
		self.parent =parent
		# Create a canvas for tkinter app
		self.canvas = tkinter.Canvas(parent,width = 1024,height = 600)
		self.canvas.pack() # pack this canvas into your tkinter
		# Create a list of tkinter image for display it frame by frame
		self.sequence = [ImageTk.PhotoImage(img)
							for img in ImageSequence.Iterator(Image.open(file))]
		# Create a image for display on canvas, start with the frame zero of sequence
		self.image = self.canvas.create_image(512,300,image=self.sequence[0])
		self.animate(1) # Function to display  frame by frame

	def animate(self,counter,time_inter =100):
		# This animate function will run continously
		self.canvas.itemconfig(self.image,image= self.sequence[counter])
		# increate the counter frame after time_inter
		self.parent.after(time_inter,lambda:self.animate((counter+1)%len(self.sequence)))

root = tkinter.Tk()
app = App(root)
root.mainloop()
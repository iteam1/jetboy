import pygame
import os

class Amy_3(pygame.sprite.Sprite):

	def __init__(self,path_sprite):

		super(Amy_3,self).__init__()

		# Create var for class
		self.images = []
		self.path = path_sprite
		self.emotion = list(os.listdir(self.path))
		self.rect = pygame.Rect(0,0,300,300)
		
		#Emotion bit
		self.bit_anger 		 = False
		self.bit_fear 		 = False
		self.bit_happy 		 = False
		self.bit_neutral     = False
		self.bit_sad	     = False
		self.bit_shame		 = False
		self.bit_silly		 = False
		self.bit_sleep		 = False
		self.bit_smile	     = False
		self.bit_surprise	 = False
		self.bit_talk        = False 
		self.bit_list        = [False,False,False,False,False,False,False,False,False,False,False]
		self.tick_count      = 0
		# Start to read all images of sprite
		for e in self.emotion:

			image_list = []

			for img in list(os.listdir(self.path + e)):
				#print(self.path + e + "/" + img)
				image_list.append(pygame.image.load(self.path + e + "/" + img))

			self.images.append(image_list)

		self.id_emotion = 0
		self.index = 0 
		self.image = self.images[self.id_emotion][self.index]

		# Command for Amy
		self.command = "None"

	def update(self):

		# With a list

		self.bit_anger,self.bit_fear,self.bit_happy,self.bit_neutral,self.bit_sad,\
		self.bit_shame,self.bit_silly,self.bit_sleep,self.bit_smile,self.bit_surprise,\
		self.bit_talk = self.bit_list 

		# Update sprite image follow emotion bit

		if self.bit_anger == True:
			self.id_emotion = 0
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_fear == True:
			self.id_emotion = 1
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_happy == True:
			self.id_emotion = 2
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_neutral == True:
			self.id_emotion = 3
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_sad == True:
			self.id_emotion = 4
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_shame == True:
			self.id_emotion = 5
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_silly == True:
			self.id_emotion = 6
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_sleep == True:
			self.id_emotion = 7
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_smile == True:
			self.id_emotion = 8
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_surprise == True:
			self.id_emotion = 9
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		elif self.bit_talk == True:
			self.id_emotion = 10
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		else:
			self.id_emotion = 3
			self.index += 1
			if self.index >= len(self.images[self.id_emotion]): self.index = 0

		# Set the image of sprite
		self.image = self.images[self.id_emotion][self.index]
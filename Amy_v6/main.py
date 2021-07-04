import threading
import os 
# Custom library
from Amy_root import Amy
import thread_funct

#GLOBAL variable
path_sprite = "./Amy_root/Amy_png/"
my_Amy = Amy.Amy_3(path_sprite)

if __name__ == "__main__":

	Amy_communicate = threading.Thread(target = thread_funct.communicate2, args = (my_Amy,))
	Amy_externalize = threading.Thread(target = thread_funct.externalize2, args = (my_Amy,))
	Amy_sprite      = threading.Thread(target = thread_funct.sprite, args = (my_Amy,))

	Amy_communicate.start()
	Amy_externalize.start()
	Amy_sprite.start()

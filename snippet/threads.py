'''
Author: locchuong
Updated: 28/12/21
Description:
    This python program for testing 2  thread,
        - a continously thread  printout something 
        - a event thread wait for a specific input, if correct then terminate both thread
'''

import logging
import time 
import threading

c = "no"

def f_cont(name):
    global c
    while True:
        logging.info("Thread %s: running",name)
        logging.info("c = %s",c)
        time.sleep(2)
        if c == "yes":
            break

def f_trig(name):
    global c
    while True:
        logging.info("Thread %s : running",name)
        c = input("What is your c: ")
        if c == "yes":
            break


if __name__ == "__main__":

    format = "%(asctime)s: %(message)s" 
    logging.basicConfig(format = format, level = logging.INFO, datefmt = "%H:%M:%S")
    
    logging.info("Main: before creating thread")
    
    x1 = threading.Thread(target = f_cont,args = ("cf",),daemon = False)
    x2 = threading.Thread(target = f_trig,args = ("tf",),daemon = False)
    #x2 = threading.Thread(target = f_cont,args = ("cf2",),daemon = False)
    
    logging.info("Main: before running thread")
    
    x1.start()
    x2.start()
    
    logging.info("Main: wait for the thread to finish")
    logging.info("Main: all done")

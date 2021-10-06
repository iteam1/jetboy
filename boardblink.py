import RPi.GPIO as GPIO 
import time 

def main():
  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(23,GPIO.OUT)

def loop():
  GPIO.output(23,1)
  time.sleep(1)
  GPIO.output(23,0)
  time.sleep(1)

if __name__ == "__main__":
  main()
  loop()


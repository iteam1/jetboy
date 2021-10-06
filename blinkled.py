import RPi.GPIO as GPIO
import time 

def main():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(11,GPIO.OUT)

def loop():
  while True:
    GPIO.output(11,1)
    time.sleep(1)
    GPIO.output(11,0)
    time.sleep(1)

if __name__ == "__main__":
  main()
  loop()  

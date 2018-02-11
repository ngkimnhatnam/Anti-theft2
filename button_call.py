import RPi.GPIO as GPIO
import time
import os

#adjust for where your switch is connected
buttonPin = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP) 
print("Waiting for button click")

while True:
  #assuming the script to call is long enough we can ignore bouncing
  if not(GPIO.input(buttonPin)):
    #this is the script that will be called (as root)
    os.system("python position0.py")
#if GPIO.input(buttonPin)==1:
 # print("Its on")
#else:
 # print("Its off")

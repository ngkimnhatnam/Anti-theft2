import RPi.GPIO as GPIO
import time

buzzer=11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setwarnings(False)

def beep():
    while True:
        GPIO.output(11, GPIO.HIGH)
        time.sleep(.05)
        GPIO.output(11, GPIO.LOW)
        time.sleep(.05)
        
def buzzer():
    try:
        beep()
    except KeyboardInterrupt:
        GPIO.output(11, GPIO.LOW)
buzzer()    


        
             

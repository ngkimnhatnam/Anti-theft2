import serial
import pynmea2
import math
import time
import RPi.GPIO as GPIO

serialStream= serial.Serial("/dev/ttyS0",9600,timeout=0.5)
coord2=[]
collected_dist=[]
#margin_error=[](Taking error margin from GPS data) 
buzzer=40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.OUT)
GPIO.setwarnings(False)
buzzer_parameter=[]

def guarding_mode(): #Calculate total distance travelled so far
        
        while True:

                if len(coord2)<4:
                        current_location()
                
                elif len(coord2)==4:
                        haversine_frompos0(coord2[0],coord2[1],coord2[2],coord2[3])
                        if buzzer_parameter[0]>5:
                            buzzer()                         
                        del buzzer_parameter[:]
                        del coord2[2:4]
                        buzzer_off()
                        
                        #print("Highest margin of error: ",max(margin_error)," m")
                        
                

def current_location(): #Get current location and append to list
        sentence=serialStream.readline()
        if sentence.find('GGA')>0:
                data=pynmea2.parse(sentence)
                lati=data.latitude
                longi=data.longitude
                la=round(lati,7)
                lo=round(longi,7)
                coord2.append(lo)
                coord2.append(la)
                print ("ON GUARDING MODE! Current location: {lat} North,{lon} East".format(lat=data.latitude, lon=data.longitude))
                print (coord2)
                time.sleep(.5)
                
                


def haversine_frompos0(lon1,lat1,lon2,lat2): #Haversine formula to calculate distance from original position between two points
    
    
    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    #lon1, lat1 = coord1
    #lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 3)
    km = round(km, 3)

    #margin_error.append(meters)
    buzzer_parameter.append(meters)
    print("Distance from original position: ",meters," m")
    
    #print("Distance:",km," km")

def beep(): #Calling the buzzer to raise beeping alarm
    
    for n in range(0,5):
        GPIO.output(40, GPIO.HIGH)
        time.sleep(.05)
        GPIO.output(40, GPIO.LOW)
        time.sleep(.05)
    
def buzzer_off():
        GPIO.output(40, GPIO.LOW)
def buzzer():#Turn on buzzer with keyboard interrupt
    n=0
    for n in range(0,5):
        try:
            beep()
        except KeyboardInterrupt:
            GPIO.output(40, GPIO.LOW)

guarding_mode()


        
        
                


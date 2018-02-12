#!/usr/bin/python
import serial
import pynmea2
import math
import time
import RPi.GPIO as GPIO
import os

serialStream= serial.Serial("/dev/ttyS0",9600,timeout=0.5)
coord1=[]                       #Coordinate list of trailing mode
coord2=[]                       #Coordinate list of guarding mode
collected_dist=[]
buzzer=40                       #Position of buzzer signal pin on Pi
buttonPin = 11                  #Position of button signal pin on Pi
buttonPin2=37
buzzer_parameter=[]
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button status now ON
GPIO.setup(buttonPin2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(buttonPin,GPIO.FALLING)
GPIO.add_event_detect(buttonPin2,GPIO.FALLING)
GPIO.setwarnings(False)

def trailing_mode(): #Calculate total distance travelled so far
        f=open("BikingDistance2.txt", "w+")#Create a txt file to write data to
        while GPIO.input(buttonPin)==1:

                if len(coord1)<4:
                        current_location()
                
                elif len(coord1)==4:
                        haversine(coord1[0],coord1[1],coord1[2],coord1[3])
                        del coord1[:]
                        total_dist=round(sum(collected_dist),4)
                        f.writelines("Total distance is: "+str(total_dist)+" km\n")
                        print ("Total distance travelled is: ",total_dist," km")


def current_location(): #Get current location and append to list
        sentence=serialStream.readline()
        if sentence.find('GGA')>0:
                data=pynmea2.parse(sentence)
                lati=data.latitude
                longi=data.longitude
                la=round(lati,5)
                lo=round(longi,5)
                coord1.append(lo)
                coord1.append(la)
                print ("Current location: {lat} North,{lon} East".format(lat=data.latitude, lon=data.longitude))
                print (coord1)
                time.sleep(2)
                
                


def haversine(lon1,lat1,lon2,lat2): #Haversine formula to calculate distance between two points
    
    
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

    collected_dist.append(km)

    print("Distance:",km," m")
    
    
    #print("Distance:",km," km")

def guarding_mode(): #Calculate total distance travelled so far
        
        while GPIO.input(buttonPin2)==1:

                if len(coord2)<4:
                        current_location2()
                
                elif len(coord2)==4:
                        haversine_frompos0(coord2[0],coord2[1],coord2[2],coord2[3])
                        if buzzer_parameter[0]>20:
                            buzzer()                         
                        del buzzer_parameter[:]
                        del coord2[2:4]
                        buzzer_off()
                        
                        #print("Highest margin of error: ",max(margin_error)," m")
                        
                

def current_location2(): #Get current location and append to list
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
    print("Distance from original position: ",km," km")
    
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

def main():
        while True:
                if GPIO.event_detected(buttonPin2):
                        trailing_mode()
                        GPIO.remove_event_detect(buttonPin2)
                        GPIO.add_event_detect(buttonPin2, GPIO.RISING)
                elif GPIO.event_detected(buttonPin):
                        guarding_mode()
                        GPIO.remove_event_detect(buttonPin)
                        GPIO.add_event_detect(buttonPin, GPIO.RISING)


main()

        
        
                


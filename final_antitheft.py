#!/usr/bin/python
import serial
import pynmea2
import math
import time
import datetime
import RPi.GPIO as GPIO
import os
import sys



serialStream= serial.Serial("/dev/ttyS0",9600,timeout=0.5)
coord1=[]                       #Coordinate list of trailing mode
coord2=[]                       #Coordinate list of guarding mode
collected_dist=[]
buzzer_parameter=[]

buzzer=40                       #Position of buzzer signal pin on Pi
buttonPin = 11                  #Position of button1 signal pin on Pi
buttonPin2=37                   #Position of buzzer 2 on Pi
bluepin=29                      #Position of blue pin on Pi
redpin=31                       #Position of red pin on Pi
greenpin=33                     #Position of green pin on Pi


GPIO.setmode(GPIO.BOARD)

#Buzzer and button settings
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(buttonPin,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonPin2,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(buttonPin,GPIO.FALLING)
GPIO.add_event_detect(buttonPin2,GPIO.FALLING)

#LED settings
GPIO.setup(bluepin, GPIO.OUT)
GPIO.setup(redpin, GPIO.OUT)
GPIO.setup(greenpin, GPIO.OUT)
GPIO.output(bluepin, GPIO.LOW)
GPIO.output(redpin, GPIO.LOW)
GPIO.output(greenpin, GPIO.LOW)

GPIO.setwarnings(False)

ts=time.time()
st=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
#f=open("BikingDistance.txt", "w+")#Create a txt file to write data to
def trailing_mode(): #Calculate total distance travelled so far
        #Create a txt file to write data to
        
        greenOff()
        redOff()
        blue()
        while GPIO.input(buttonPin)==1:
                
                if len(coord1)<4:
                        current_location()
                
                elif len(coord1)==4:
                        f=open("BikingDistance.txt", "a+")
                        haversine(coord1[0],coord1[1],coord1[2],coord1[3])
                        del coord1[0:2]
                        total_dist=round(sum(collected_dist),4)
                        f.writelines(st+" Total distance is: "+str(total_dist)+" km\n")
                        print ("Total distance travelled is: ",total_dist," km")
                        f.close()

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
        green()
        blueOff()
        redOff()
        while GPIO.input(buttonPin2)==1:

                if len(coord2)<4:
                        current_location2()
                
                elif len(coord2)==4:
                        haversine_frompos0(coord2[0],coord2[1],coord2[2],coord2[3])
                        if buzzer_parameter[0]>10:
                            greenOff()
                            blueOff()
                            buzzer()
                            redOn()
                        del buzzer_parameter[:]
                        del coord2[2:4]
                        buzzer_off()
                        redOff()

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

def beep(): #Beeping sound
    
    for n in range(0,3):
        GPIO.output(40, GPIO.HIGH)
        time.sleep(.05)
        GPIO.output(40, GPIO.LOW)
        time.sleep(.05)
    
def buzzer_off():#Turn off buzzer
        GPIO.output(40, GPIO.LOW)
def buzzer():#Turn on buzzer with keyboard interrupt
    for n in range(0,1):
        try:
            beep()
        except KeyboardInterrupt:
            buzzer_off()
            
def blueOn():#Blue light on
    GPIO.output(bluepin, GPIO.HIGH)
     
def blue():
        try:
                blueOn()
        except KeyboardInterrupt:
                blueOff()
                
def blueOff():# Blue light off
    GPIO.output(bluepin, GPIO.LOW)
def redOn():#Red light on
    for i in range (0,1):
            GPIO.output(redpin, GPIO.HIGH)
            time.sleep(.05)
            GPIO.output(redpin, GPIO.LOW)
            time.sleep(.05)
def redOff():#Red light off
    GPIO.output(redpin, GPIO.LOW)
def red():
        for n in range(0,5):
                try:
                        redOn()
                except KeyboardInterrupt:
                        redOff()
def greenOn():#Green light on
    GPIO.output(greenpin, GPIO.HIGH)
def greenOff():#Green light off
    GPIO.output(greenpin, GPIO.LOW)
def green():
        try:
                greenOn()
        except KeyboardInterrupt:
                greenOff()

def main():
        while True:
                #trailing_mode()
                if GPIO.event_detected(buttonPin2):
                        trailing_mode()
                        GPIO.remove_event_detect(buttonPin2)
                        GPIO.add_event_detect(buttonPin2, GPIO.RISING)
                elif GPIO.event_detected(buttonPin):
                        guarding_mode()
                        GPIO.remove_event_detect(buttonPin)
                        GPIO.add_event_detect(buttonPin, GPIO.RISING)

if __name__ == '__main__':
        main()


        
        
                


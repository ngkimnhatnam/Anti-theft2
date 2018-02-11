import serial
import pynmea2
import math
import time

serialStream= serial.Serial("/dev/ttyS0",9600,timeout=0.5)

coord1=[]

def current_location():        
        counter=0
        while counter<=30:
                sentence=serialStream.readline()
                if sentence.find('GGA')>0:
                        data=pynmea2.parse(sentence)
                        lati=data.latitude
                        longi=data.longitude
                        la=round(lati,5)
                        lo=round(longi,5)
                        if len(coord1)<4:
                                coord1.append(lo)
                                coord1.append(la)
                                print ("Current location: {lat} North,{lon} East".format(lat=data.latitude, lon=data.longitude))
                                print (coord1)
                        elif len(coord1)==4:
                                
                                
                                haversine(coord1[0],coord1[1],coord1[2],coord1[3])
                                
                                
                                del coord1[:]
                        
                        time.sleep(1)
                        counter=counter+1
                
def haversine(lon1,lat1,lon2,lat2):
    
    distance=[]
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
    distance.append(meters)

    print("Distance:",meters," m")
    print("Distance in total: ",distance)
    
    #print("Distance:",km," km")

current_location()



        
        
                


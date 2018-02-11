#!/bin/bash
mosquitto_pub -h 192.168.1.145 -p 1883 -t bike -f BikingDistance2.txt


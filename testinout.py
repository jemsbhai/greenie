import serial
import json
import os
import random
##from twilio.rest import Client
import time
import requests
from pymongo import MongoClient
from pprint import pprint



# client = MongoClient("mongodb+srv://rootzero:fitx@teamzerocluster-mzyhk.mongodb.net/test?retryWrites=true&w=majority")
# db = client["pittchallenge-brushine"]


def getNFC(portname, baud):


    ##ser = serial.Serial('COM24', 115200)

    ser = serial.Serial(portname, baud)
    

    print ("connected to: " + str(ser.portstr))
    reading = {}
    ts1 = 0
    ts2 = 0

    while True:
        line = ser.readline()
        print("read a line")
        line = line.decode('utf8')
        ##line = line [2:13]
        line = line.replace(" ", "")
        line=line.rstrip()
        if "#" not in line:
            continue
        print(line)

        if "#" in line:
            print("NFC scanned")
            line = line.replace("#", "")
            line = line.replace("In dec:", "")
            line = line.replace(" ", "")
            return line
        
        if "$" in line:
            print("BPM read")
            return line

        

        



instatus = 0
instatus2 = 0

name2 = input(" what is your name?")     

while True:
    
    print ("test continue (any key)")
    
    any = input()
        
    line = getNFC('COM14', 115200)
    print(line)
    
    if "141" in line:
        if instatus == 0:
            print("welcome muntaser")
            instatus = 1
            continue
        if instatus == 1:
            print ("goodbye muntaser")
            instatus = 0
            continue

    if "189" in line:
        if instatus2 == 0:
            print("welcome " + name2)
            instatus2 = 1
            continue
        if instatus2 == 1:
            print ("goodbye " + name2)
            instatus2 = 0
            continue



        




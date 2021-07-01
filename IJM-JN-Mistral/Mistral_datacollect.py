# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:24:52 2020

@author: Ryan
"""
'''
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
    v6 structure: [(range,azimuth,elevation,doppler),......]

V7: Target Object List
    V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]

V8: Target Index
    V8 structure: [id1,id2....]

V9:Point Cloud Side Info
    v9 structure: [(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import lpdISK
from datetime import datetime
from mmWave import trafficMD
import csv


#Defined for Pi-board
#   port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

#Defined for Jetson Nano UART port
port = serial.Serial("/dev/ttyUSB1",baudrate = 921600, timeout = 0.5)

tmd = trafficMD.TrafficMD(port)

def uartGetdata(name):
    print("mmWaveRADAR@Petronas: {:} Raw-Point-Clouds:".format(name))
    port.flushInput()
    with open("count.txt", "r") as fopen:
        count = fopen.readline()

    print("Count: ", int(count))

    
    time_start = datetime.now()
    # i = int(input('Enter loop counter: '))
    i = int(count)
    i += 1
    with open("count.txt", "w") as fopen:
        fopen.write(str(i+1))


    while True:
        #hdr = tmd.getHeader()
        
        (dck,v6,v7,v8,v9)=tmd.tlvRead(False)
        
        time_end = datetime.now()
        time_diff = time_end - time_start
        total_seconds = time_diff.total_seconds()
        if  total_seconds > 900:
            time_start = datetime.now()
        
        if dck:
            print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
            
            # print(v6)

            time_stamp = datetime.now()
            timestr = time_stamp.strftime("%d %m %Y %H:%M:%S.%f")

          
            with open("v6 data {}.csv".format(i),"a") as p8_v6:
                writer_p8_v6 = csv.writer(p8_v6,delimiter=",",quoting=csv.QUOTE_ALL)
                writer_p8_v6.writerow([str(timestr), v6])
    
 
uartGetdata("Raw data collection for Petronas Dagangan Berhad using for BM-201 ISK (LPD)")

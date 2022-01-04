import serial
import time
import numpy as np
from lpdisk_mistral import LpdISK
import datetime as dt
import csv

# Change the configuration file name
configFileName = 'chirp_config_3d.cfg'

CLIport = {}
Dataport = {}
byteBuffer = np.zeros(2**15,dtype = 'uint8')
byteBufferLength = 0;


# ------------------------------------------------------------------

# Function to configure the serial ports and send the data from
# the configuration file to the radar
def serialConfig(configFileName):
    
    global CLIport
    global Dataport
    # Open the serial ports for the configuration and the data ports
    
    # Raspberry pi
    CLIport = serial.Serial('/dev/ttyUSB0', 115200)
    Dataport = serial.Serial('/dev/ttyUSB1', 921600)
    
    # Windows
    #CLIport = serial.Serial('COM3', 115200)
    #Dataport = serial.Serial('COM4', 921600)

    # Read the configuration file and send it to the board
    config = [line.rstrip('\r\n') for line in open(configFileName)]
    for i in config:
        CLIport.write((i+'\n').encode())
        print(i)
        time.sleep(0.01)
        
    return CLIport, Dataport
    

CLIport, port = serialConfig(configFileName)
tmd = LpdISK(port)

def uartGetdata(name):
    print("mmWaveRADAR@Petronas: {:} Raw-Point-Clouds:".format(name))
    port.flushInput()
        
    with open("count.txt", "r") as fopen:
        count = fopen.readline()

    print("Count: ", int(count))
    
    time_start = dt.datetime.now()
    i = int(count)
    i += 1
    with open("count.txt", "w") as fopen:
        fopen.write(str(i+1))
        
        

    while True:
        #hdr = tmd.getHeader()
        
        (dck,v6,v7,v8,v9)=tmd.tlvRead(False)
        
        time_end = dt.datetime.now()
        time_diff = time_end - time_start
        total_seconds = time_diff.total_seconds()
        if  total_seconds > 900:
            time_start = dt.datetime.now()
        
        if dck:
            print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
            
            # print(v6)

            time_stamp = dt.datetime.now()
            timestr = time_stamp.strftime("%d %m %Y %H:%M:%S.%f")

          
            with open("v6 data {}.csv".format(i),"a") as p8_v6:
                writer_p8_v6 = csv.writer(p8_v6,delimiter=",",quoting=csv.QUOTE_ALL)
                writer_p8_v6.writerow([str(timestr), v6])
 
uartGetdata("Raw data collection for mmWave Mistral IWR6843AoP")




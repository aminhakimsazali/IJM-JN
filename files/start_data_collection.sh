#!/bin/bash

sudo chmod +777 /dev/ttyS0
sudo chmod +777 /dev/ttyUSB1
sudo chmod +777 /dev/ttyUSB0

sudo python3 rawOutput.py

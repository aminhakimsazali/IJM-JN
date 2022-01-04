#!/bin/bash

#sudo chmod +777 /dev/ttyS0
sudo chmod +777 /dev/ttyUSB1
sudo chmod +777 /dev/ttyUSB0

sudo python3 /home/pi/Downloads/IJM-JN-Mistral/mistral_config_collect_data_20mins_cycle.py

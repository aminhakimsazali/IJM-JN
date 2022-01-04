#!/bin/bash
echo "Start Recoding video for ${filename}"
process=$( sudo fuser /dev/video0 | awk '{print $1}')
echo $process
kill -9 $process
# kill -9 $(ps aux | grep 'bash recordVid.sh' | awk '{print $2}')

sudo bash recordVid.sh	
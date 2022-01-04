#!/bin/bash

#11-10-2021_15-40-00.mp4 file format
#11-10-2021_15-40-00.mp4 file format

filename=$(date +"%d-%m-%Y_%H-%M-%S.mp4")
echo $filename

# echo "Start Recoding video for ${filename}"
# kill -9 $(ps aux | grep 'bash recordVid.sh' | awk '{print $2}')

# 1 minute =  60 seconds
# 2 minute =  120 seconds
# 3 minute =  180 seconds
# 4 minute =  340 seconds
# 18 minutes = 900 seconds
# 20 minutes = 1200 seconds
# Need to add 5 seconds for each minute

ffmpeg -f video4linux2 -i /dev/video0 -s 1280x720 -r 30  \
-framerate 25 -vcodec libx264 -vb 2000k -timelimit 1080  \
-vf "drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf: \
box=1: boxcolor=black@0.8: boxborderw=5 : \
fontsize=(h/30): x=(w-text_w)/2: y=50: text='%{localtime}': fontcolor=white:"  \
-preset ultrafast -f mp4 $filename

# ffmpeg -i output.mp4 -vf "transpose=2,transpose=2" output_rotated.mp4
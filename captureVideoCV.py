import cv2
import time


# import picamera
import datetime as dt
# import shlex
import subprocess
import os 

time_start = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
save_path= "/home/pi/Downloads"
filename = f"{time_start}.avi"
completed_video= os.path.join(save_path, filename)

# Creat an object to read
video = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
if (video.isOpened() == False): 
    print("Error reading video file")

# set dimensions
video.set(cv2.CAP_PROP_FRAME_WIDTH, 2560)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1440)

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))
size = (frame_width, frame_height)


result = cv2.VideoWriter(filename, 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

start = dt.datetime.now()
#10 minutes == 600  #20 minutes == 1200 #1 hour == 3600
while (dt.datetime.now() - start).seconds < 60: 
	print(dt.datetime.now())
    # camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # camera.wait_recording(0.2)
	ret, frame = video.read()    
	# cv2.rotate(frame, cv2.ROTATE_180)
	rotated=cv2.rotate(frame, cv2.ROTATE_180)

	if ret == True: 
		result.write(rotated)
		
	if cv2.waitKey(1) & 0xFF == ord('s'):
            break

# camera.stop_recording()


# When everything done, release 
# the video capture and video 
# write objects
video.release()
result.release()

print("The video was successfully saved")

import picamera
import datetime as dt
import shlex
import subprocess
import os 

time_start = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
save_path= "/home/pi/IJM-JN"
filename = f"{time_start}.h264"
completed_video= os.path.join(save_path, filename)

while True:
    time_start = dt.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    save_path= "/home/pi/IJM-JN"
    filename = f"{time_start}.h264"
    completed_video= os.path.join(save_path, filename)

    with picamera.PiCamera() as camera:
        camera.resolution = (1280, 720)
        camera.framerate = 24
        camera.start_preview()
        camera.vflip = True
        camera.hflip = True
        camera.annotate_background = picamera.Color('black')
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.start_recording(filename)
        start = dt.datetime.now()
        #10 minutes == 600  #20 minutes == 1200 #1 hour == 3600
        # while (dt.datetime.now() - start).seconds < 600:

        #Stop at 05, 25, 45 minutes
        while (dt.datetime.now().minute != 0) or (dt.datetime.now().minute != 25) or (dt.datetime.now().minute != 45):
            camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            camera.wait_recording(0.2)
        camera.stop_recording()
        
    #Conversion to usable file format
    print("Camera finished recording... Beginning Analysis")
    from subprocess import CalledProcessError

    command = shlex.split("MP4Box -add {} {}.mp4".format(completed_video, os.path.splitext(filename)[0]))

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except CalledProcessError as e:
        print('FAIL:\ncmd:{}\noutput:{}'.format(e.cmd, e.output))
        print(e.output)

    #starts detecting again after given time
    print("Ready for next sample")    
    os.remove(completed_video)



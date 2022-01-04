import picamera
import datetime as dt
time_start = dt.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 24
    camera.start_preview()
    camera.vflip = True
    camera.hflip = True
    camera.annotate_background = picamera.Color('black')
    camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.start_recording(f'{time_start}.h264')
    start = dt.datetime.now()
    while (dt.datetime.now() - start).seconds < 3600: #20 minutes == 1200
        camera.annotate_text = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)
    camera.stop_recording()

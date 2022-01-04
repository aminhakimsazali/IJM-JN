import numpy as np
import cv2 
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\AH\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

class ImageExtractor():
    def __init__(self, filename):
        self.fps = 5
        self.cap = cv2.VideoCapture(video_name)
        self.start_time = get_start_time(self.cap)[:-3]
        
    def get_start_time(self, index = 1):
        self.cap.set(1, index); # Where frame_no is the frame you want
        ret, frame = self.cap.read() # Read the frame

        start_frame = frame[20:50, 495:785]
        imgplot = plt.imshow(start_frame)
        custom_config = r'--oem 3 --psm 6'
        time_ = pytesseract.image_to_string(start_frame, config= custom_config)
        return time_

    def get_frame(self, index):
        self.cap.set(1, index); # Where frame_no is the frame you want
        ret, frame = self.cap.read() # Read the frame

        return frame
    def getFrameByTime(self, time_wanted):
        frame_index = (time_wanted - pd.Timestamp(self.start_time)).seconds * self.fps
        frame_ = get_frame(self.cap, int(frame_index))
        return frame_
    
    def plotImage(self, img, rgb = False):
        if rgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        figure(figsize=(10,6), dpi= 80)
        imgplot = plt.imshow(img)
        plt.show()


video_name =  r"C:\Users\AH\OneDrive - siswa.um.edu.my\FSKTM\Freelancer\2020\Freelancer - Adrian\IJM\IJM-Actual-Evaluation\11-10-2021_15-40-00.mp4"

ie = ImageExtractor(video_name)
ie.start_time = ie.get_start_time()
time_wanted = pd.to_datetime("2021-10-11 15:47:41", format = "%Y-%m-%d %H:%M:%S")
ie.plotImage(ie.getFrameByTime(time_wanted), rgb=True)
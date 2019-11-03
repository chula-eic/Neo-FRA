
import cv2
import socket
import struct
import pickle
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 24
rawCapture = PiRGBArray(camera)
print('initializing completed')
print('establishing connection')
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.2.38', 8554))
print('connected')
connection = client_socket.makefile('wb')


#image = rawCapture.array
#cam = cv2.VideoCapture(0)

#cam.set(3, 320);
#cam.set(4, 240);

img_counter = 0

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    
while True:
    #ret, frame = cam.read()
    frame = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(frame, 'bgr')
    print(frame.shape)
    result, frame = cv2.imencode('.jpg', frame, encode_param)
#    data = zlib.compress(pickle.dumps(frame, 0))
    data = pickle.dumps(frame, 0)
    size = len(data)


    print("{}: {}".format(img_counter, size))
    client_socket.sendall(struct.pack(">L", size) + data)
    img_counter += 1

cam.release()

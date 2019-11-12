import cv2
import socket
import struct
import pickle

from numba.pycc import CC
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np

class CamClient(object):
    def __init__(self, IP, PORT):
        self.camera = PiCamera()
        self.camera.resolution = (320, 240)
        self.camera.framerate = 24
        rawCapture = PiRGBArray(self.camera)
        #print('initializing completed')
        #print('establishing connection')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, PORT))
        #print('connected')
        self.connection = self.client_socket.makefile('wb')


        #image = rawCapture.array
        #cam = cv2.VideoCapture(0)

        #cam.set(3, 320);
        #cam.set(4, 240);

        #self.img_counter = 0

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def transmit(self, camera, encode_param, client_socket):
        while True:
            #ret, frame = cam.read()
            frame = np.empty((240, 320, 3), dtype=np.uint8)
            camera.capture(frame, 'bgr')
            #print(frame.shape)
            result, frame = cv2.imencode('.jpg', frame, encode_param)
            #data = zlib.compress(pickle.dumps(frame, 0))
            data = pickle.dumps(frame, 0)
            size = len(data)


            #print("{}: {}".format(img_counter, size))
            client_socket.sendall(struct.pack(">L", size) + data)
            #img_counter += 1

        cam.release()

def start(IP, PORT):
    CClient = CamClient(IP, PORT)
    CClient.transmit(CClient.camera, CClient.encode_param, CClient.client_socket)

if __name__ == '__main__':
    start('172.16.0.126', 8554)

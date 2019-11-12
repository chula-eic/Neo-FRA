import socket
import cv2
import pickle
import struct ## new

class CamServer(object):
    def __init__(self, port):
        self.HOST = '0.0.0.0'
        self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print('Socket created')

        self.s.bind((self.HOST, self.PORT))
        #print('Socket bind complete')
        self.s.listen(10)
        #print('Socket now listening')

        self.conn, self.addr = self.s.accept()

        self.data = b""
        self.payload_size = struct.calcsize(">L")
        #print("payload_size: {}".format(self.payload_size))
    def receive(self, data, conn, payload_size):
        while(1):
            while len(data) < payload_size:
                #print("Recv: {}".format(len(data)))
                data += conn.recv(4096)

            #print("Done Recv: {}".format(len(data)))
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            #print("msg_size: {}".format(msg_size))
            while len(data) < msg_size:
                data += conn.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (1280, 720))
            cv2.imshow('ImageWindow',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

def start(port):
    print('Cam server starting')
    CServer = CamServer(port)
    CServer.receive(CServer.data, CServer.conn, CServer.payload_size)

if __name__ == '__main__':
    start(8554)

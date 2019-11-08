import socket
import time
import Serial
import json


class Client(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):

        while True:

            
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.hostname,self.port))

            
            data = json.loads(sock.recv(1024).decode("utf-8"))

            moving = 1
            rotation = 1

            if data['hats'][0] == [0,0] and data['axes'][0] == 0 and data['axes'][1] == 0:
                moving = 0
            if data['button'][1] == 0 and data['button'][3] == 0 and data['axes'][2] == 0 and data['axes'][3] == 0:
                rotation = 0

            if moving:
                if data['hats'][0] != [0,0]:
                    #call func 2 func
                else:
                    #call func 2 func
                    #data['axes'][0] for x
                    #data['axes'][1] for y

            if rotation:
                if data['button'][1] != 0 or data['button'][3] != 0:
                    #call func rotate
                else:
                    #call func rotate
                        
            if data['button'][0]:
                #call lift up
            elif data['button'][2]:
                #call lift down

                    
            sock.close()


def init():
    
    pi = Client('localhost', 6969)
    pi.start()

init()

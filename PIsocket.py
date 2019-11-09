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
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.hostname,self.port))

                data = json.loads(sock.recv(1024).decode("utf-8"))

                moving = 1
                rotation = 1
                elevator = 1


                if data['hats']['0'] == [0,0] and data['axes']['0'] == 0 and data['axes']['1'] == 0:
                    moving = 0
                if data['button']['1'] == 0 and data['button']['3'] == 0 and data['axes']['2'] == 0 and data['axes']['3'] == 0:
                    rotation = 0
                if data['button']['0'] == 0 and data['button']['2'] == 0:
                    elevator = 0


                if moving:
                    if data['hats']['0'] != [0,0]:
                        Serial.translation_vx(data['hats']['0'][0])
                        Serial.translation_vy(data['hats']['0'][1])
                    else:
                        Serial.translation_vx(data['axes']['0'])
                        Serial.translation_vy(data['axes']['1'])

                else:
                    Serial.translation_vx(0)
                    Serial.translation_vy(0)


                if rotation:
                    if data['button']['1'] != 0 or data['button']['3'] != 0:
                        if data['button']['1'] != 0:
                            Serial.rotation_v(data['button']['1'])
                        else:
                            Serial.rotation_v((data['button']['3']*(-1)))
                    else:
                        Serial.rotation_v(data['axes']['2'])
                else:
                    Serial.rotation_v(0)


                if elevator:       
                    if data['button']['0']:
                        Serial.elevator(1)
                    else:
                        Serial.elevator(0)
            except:
                pass

            finally:
                sock.close()


def init():
    
    pi = Client('localhost', 6969)
    pi.start()

init()

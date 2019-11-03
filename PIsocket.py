import multiprocessing
import socket
import time
import Serial


def handle(connection, address):
    
    try:
        
        while True:
            
            data = connection.recv(1024)
            
            if data != b'':
                data = list(data)

                if len(data) == 2:
                    
                    speed = (data[1]-128)*9999/128
                    
                    if data[0] == 0:
                        Serial.translation_vx(speed)
                    elif data[0] == 1:
                        Serial.translation_vy(speed)
                    else:
                        Serial.rotation_v(speed)
                        
                elif data[0] == 0:
                    Serial.elevator(0)
                else:
                    Serial.elevator(1)
                
                break
    except:
        pass
    
    finally:
        connection.close()


class Server(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            process = multiprocessing.Process(
                target=handle(conn, address))
            process.daemon = True
            process.start()


def init():
    
    ser = Server('localhost', 6969)
    ser.start()

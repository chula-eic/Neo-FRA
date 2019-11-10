import socket, time, Serial, json

class Client(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):

        while True:
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("establishing connection")
                sock.connect((self.hostname,self.port))
                print('conected!')
                data = json.loads(sock.recv(1024).decode("utf-8"))
                
                moving = 1
                rotation = 1
                elevator = 1
                x = 0
                y = 0
                z = 0
                

                if data['hats']['0'] == [0,0] and data['axes']['0'] == 0 and data['axes']['1'] == 0:
                    moving = 0
                if data['button']['1'] == 0 and data['button']['3'] == 0 and data['axes']['2'] == 0 and data['axes']['3'] == 0:
                    rotation = 0
                if data['button']['0'] == 0 and data['button']['2'] == 0:
                    elevator = 0

                
                if moving:
                    if data['hats']['0'] != [0,0]:
                        x = data['hats']['0'][0]
                        y = data['hats']['0'][1]
                    else:
                        x = data['axes']['0']
                        y = data['axes']['1']

                else:
                    x = 0
                    y = 0


                if rotation:
                    if data['button']['1'] != 0 or data['button']['3'] != 0:
                        if data['button']['1'] != 0:
                            z = data['button']['1']
                        else:
                            z = data['button']['3']*(-1)
                    else:
                        z = data['axes']['2']
                else:
                    z = 0
                Serial.translation(x, y, z)
                if elevator:       
                    if data['button']['0']:
                        Serial.elevator(1)
                    elif data['button']['2']:
                        Serial.elevator(-1)
                    else:
                        Serial.elevator(0)
            except Exception as e:
                print(e)

            finally:
                sock.close()
            time.sleep(1)


def init():
    print('start')
    #Serial.setup()
    pi = Client('172.16.0.126', 6783)
    pi.start()
    
if __name__ == "__main__":
    init()

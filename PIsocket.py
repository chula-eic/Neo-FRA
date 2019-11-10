import socket, time, Serial, json


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
                elevator = 0
                gripper = 0
                x, y, z = 0


                if data['hats']['0'] == [0,0] and data['axes']['0'] == 0 and data['axes']['1'] == 0:
                    moving = 0
                if data['axes']['2'] == 0:
                    rotation = 0
                if data['button']['5'] == 0 and data['button']['7'] == 0:
                    elevator = 0
                if data['button']['4'] == 0:
                    gripper = 0
                if data['button']['6'] == 0:
                    gripper = 1


                if moving:
                    if data['hats']['0'] != [0,0]:
                        x = data['hats']['0'][0]
                        y = data['hats']['0'][1]
                    else:
                        x = data['axes']['0']
                        y = data['axes']['1']

                else:
                    x, y = 0


                if rotation:
                    if data['button']['1'] != 0 or data['button']['3'] != 0:
                        if data['button']['1'] != 0:
                            z = data['button']['1']
                        else:
                            z = data['button']['3']*(-1)
                    else:
                        z = data['axes']['2']
                else:
                    Serial.rotation_v(0)

                Serial.translation(x, y, z)
                if elevator:       
                    if data['button']['5']:
                        Serial.elevator(1)
                    elif data['button']['7']:
                        Serial.elevator(-1)
                    else:
                        Serial.elevator(0)
            except:
                pass

            finally:
                sock.close()


if __name__ == "__main__":
    #Serial.setup()
    client = Client('192.168.56.1', 6783)
    client.start()

import socket, Serial, json

class Client(object):

    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def start(self):

        while True:
            #time.sleep(0.5)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                #print("establishing connection")
                sock.connect((self.hostname,self.port))
                #print('conected!')
                data = json.loads(sock.recv(1024).decode("utf-8"))
                #print(data)
                moving = 1
                rotation = 1
                elevator = 1
                x = 0
                y = 0
                z = 0


                if data['hats']['0'] == [0,0] and data['axes']['0'] == 0 and data['axes']['1'] == 0:
                    moving = 0
                if data['axes']['2'] == 0:
                    rotation = 0
                if data['button']['5'] == 0 and data['button']['7'] == 0:
                    elevator = 0

                if data['button']['4'] == 1:
                    Serial.gripper(0)
                if data['button']['6'] == 1:
                    Serial.gripper(1)

                
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
                    z = data['axes']['2']
                else:
                    z = 0
                Serial.translation(int(-x/1.25), int(-y/1.25), -z//2)
                if elevator:       
                    if data['button']['5']:
                        Serial.elevator(1)
                    elif data['button']['7']:
                        Serial.elevator(-1)
                    else:
                        Serial.elevator(0)
            except Exception as e:
                print(e)
                #pass

            finally:
                sock.close()
    


def start(IP, PORT):
    print('start')
    Serial.setup()
    pi = Client(IP, PORT)
    pi.start()
    
if __name__ == "__main__":
    start('172.16.0.126', 6783)

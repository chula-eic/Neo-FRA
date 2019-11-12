import pygame, socket, json

# ----Define------
MAX_SPEED = 999
NOISE = 0.001


# ----------------

def handleCon(con, addr, joy):
    try:
        joy.handle_joy()

        data = bytes(json.dumps(joy.event), encoding='utf8')
        #print(data)
        con.send(data)


    except:
        pass

    finally:
        con.close()


class JoyHandler(object):

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.speed = MAX_SPEED
        self.event = {}
        self.count = 0
        self.joystick_count = pygame.joystick.get_count()

    def handle_joy(self):

        pygame.event.get()
        for joy_num in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(joy_num)
            joystick.init()

            axes = joystick.get_numaxes()
            self.event['axes'] = {}
            for j in range(axes):
                self.event['axes'][j] = joystick.get_axis(j)
                if self.event['axes'][j] ** 2 <= NOISE ** 2:
                    self.event['axes'][j] = 0
                self.event['axes'][j] = self.event['axes'][j] * self.speed
                if self.event['axes'][j] > MAX_SPEED:
                    self.event['axes'][j] = MAX_SPEED
                elif self.event['axes'][j] < -MAX_SPEED:
                    self.event['axes'][j] = -MAX_SPEED
                if j % 2 == 1:
                    self.event['axes'][j] *= -1
                self.event['axes'][j] = int(self.event['axes'][j])
            buttons = joystick.get_numbuttons()
            self.event['button'] = {}
            for but_num in range(buttons):
                if 4 <= but_num < 8:
                    self.event['button'][but_num] = joystick.get_button(but_num)

                #self.event['button'][but_num] = int(self.event['button'][but_num])

            hats = joystick.get_numhats()
            self.event['hats'] = {}
            for hat_num in range(hats):
                self.event['hats'][hat_num] = list(joystick.get_hat(hat_num))
                for hat in self.event['hats'][hat_num]:
                    self.event['hats'][hat_num][hat] *= self.speed
                    #self.event['hats'][hat_num][hat] = int(self.event['hats'][hat_num][hat])


class Server(object):

    def __init__(self, hostname, port, joy):
        self.hostname = hostname
        self.port = port
        self.joy = joy

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.hostname, self.port))
        self.socket.listen(1)

        while True:
            conn, address = self.socket.accept()
            handleCon(conn, address, self.joy)

def start(port):
    print("PC socket starting")
    Joy = JoyHandler()
    ser = Server('0.0.0.0', port, Joy)
    ser.start()


if __name__ == "__main__":
    start(6783)
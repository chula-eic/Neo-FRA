import pygame, socket, time, json

# ----Define------
MAX_SPEED = 999
NOISE = 0.001


# ----------------

def handleCon(con, addr, joy):
    try:

        joy.handle_joy()

        data = bytes(json.dumps(joy.event), encoding='utf8')
        con.send(data)


    except:
        pass

    finally:
        time.sleep(0.1)
        con.close()


class JoyHandler(object):

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.speed = MAX_SPEED // 2
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

            buttons = joystick.get_numbuttons()
            self.event['button'] = {}
            for but_num in range(buttons):
                if but_num < 4:
                    if but_num % 2 == 1:
                        self.event['button'][but_num] = joystick.get_button(but_num) * self.speed
                    else:
                        self.event['button'][but_num] = joystick.get_button(but_num)
                elif but_num % 2 == 1 and joystick.get_button(but_num) == 1:
                    self.speed -= 50
                    if self.speed < 0:
                        self.speed = 0
                elif but_num % 2 == 0 and joystick.get_button(but_num) == 1:
                    self.speed += 50
                    if self.speed > MAX_SPEED:
                        self.speed = MAX_SPEED

            hats = joystick.get_numhats()
            self.event['hats'] = {}
            for hat_num in range(hats):
                self.event['hats'][hat_num] = list(joystick.get_hat(hat_num))
                for hat in self.event['hats'][hat_num]:
                    self.event['hats'][hat_num][hat] *= self.speed


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


if __name__ == "__main__":
    JoyHandler = JoyHandler()
    ser = Server('0.0.0.0', 6783, JoyHandler)
    ser.start()

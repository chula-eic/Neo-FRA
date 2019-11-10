import pygame, socket, time, json, Serial

# ----Define------
MAX_SPEED = 999
NOISE = 0.001


# ----------------




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
                self.event['axes'][j] = int(self.event['axes'][j])
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
                #self.event['button'][but_num] = int(self.event['button'][but_num])

            hats = joystick.get_numhats()
            self.event['hats'] = {}
            for hat_num in range(hats):
                self.event['hats'][hat_num] = list(joystick.get_hat(hat_num))
                for hat in self.event['hats'][hat_num]:
                    self.event['hats'][hat_num][hat] *= self.speed
                    #self.event['hats'][hat_num][hat] = int(self.event['hats'][hat_num][hat])
            print(joystick.get_axis(2))
            Serial.translation(int(self.event['axes'][0]*1.5), int(self.event['axes'][1]*1.5), self.event['axes'][2])

if __name__ == "__main__":
    Serial.setup()
    JoyHandler = JoyHandler()
    while(1):
        JoyHandler.handle_joy()
        #time.sleep(0.1)

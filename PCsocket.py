import pygame, socket

#----Define------
LIFT_UP = [1]
LIFT_DOWN = [0]
MAX_SPEED = 9999
NOISE = 0.001

MOVE_X = [0,0]
MOVE_Y = [1,0]
ROTATE = [2,0]
#----------------

class JoyHandler(object):
    
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.speed = MAX_SPEED//2
        self.joystick_count = pygame.joystick.get_count()


    def send(self, comm):
        if len(comm) > 1:
            comm[1] = int(comm[1])
            if(comm[1] > 255):
                comm[1] -= 1
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 6969))
        sock.send(bytes(comm))
        sock.close()
        

    def handle_joy(self):
        
        pygame.event.get()
        
        for joy_num in range(self.joystick_count):
            joystick = pygame.joystick.Joystick(joy_num)
            joystick.init()
            
            axes = joystick.get_numaxes()
            for j in range(axes):
                axis = joystick.get_axis(j)
                self.callfunc('axis',j,axis)

            buttons = joystick.get_numbuttons()
            for but_num in range(buttons):
                button = joystick.get_button(but_num)
                self.callfunc('button',but_num,button)
                
            hats = joystick.get_numhats()
            for hat_num in range(hats):
                hat = joystick.get_hat(hat_num)
                self.callfunc('hat',hat_num,hat)


    def callfunc(self, action_type, key, value):
        
        if(value == 0 or value == (0,0)):
            return
        
        if(action_type == 'hat'):
            if value[0] == 1: #hat 2
                MOVE_X[1] = self.speed * 128 // MAX_SPEED + 128
                self.send(MOVE_X)
            elif value[0] == -1: #hat 4
                MOVE_X[1] = -self.speed * 128 // MAX_SPEED + 128
                self.send(MOVE_X)
            if value[1] == 1: #hat 1
                MOVE_Y[1] = self.speed * 128 // MAX_SPEED + 128
                self.send(MOVE_Y)
            elif value[1] == -1: #hat 3
                MOVE_Y[1] = -self.speed * 128 // MAX_SPEED + 128
                self.send(MOVE_Y)
                
        elif(action_type == 'button'):
            if (key < 4):
                if key == 0:
                    self.send(LIFT_UP)
                elif key == 2:
                    self.send(LIFT_DOWN)
                else:
                    if key == 1:
                        ROTATE[1] = self.speed * 128 // MAX_SPEED + 128
                        self.send(ROTATE)
                    elif key == 3:
                        ROTATE[1] = -self.speed * 128 // MAX_SPEED + 128
                        self.send(ROTATE)
            elif ( key % 2 == 1 ):
                self.speed += (key-1)*100
                if self.speed > MAX_SPEED:
                    self.speed = MAX_SPEED
            else:
                self.speed -= key*100
                if self.speed < 0:
                    self.speed = 0
                    
        elif(action_type == 'axis'):
            if value*value <= NOISE*NOISE:
                return
            value = value*self.speed
            if value > MAX_SPEED:
                value = MAX_SPEED
            elif value < -MAX_SPEED:
                value = -MAX_SPEED
            if key == 0:
                MOVE_X[1] = value * 128 // MAX_SPEED + 128
                self.send(MOVE_X)
            elif key == 1:
                MOVE_Y[1] = -value * 128 // MAX_SPEED + 128
                self.send(MOVE_Y)
            elif key == 2:
                ROTATE[1] = value * 128 // MAX_SPEED + 128
                self.send(ROTATE)


        
                

def init():
    global JoyHandler
    JoyHandler = JoyHandler()
    if(JoyHandler.joystick_count == 0):
        print("No joystick found!")
        exit(1)
        

def handle():
    global JoyHandler
    JoyHandler.handle_joy()


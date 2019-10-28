import pygame, Serial

#----Define------
LIFT_UP = 1
LIFT_DOWN = 0
MAX_SPEED = 9999
NOISE = 0.001
#----------------

class JoyHandler(object):
    
    
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.func = {}
        self.speed = MAX_SPEED//2
        self.joystick_count = pygame.joystick.get_count()
        self.func['move_y'] = Serial.translation_vy
        self.func['move_x'] = Serial.translation_vx
        self.func['rotate'] = Serial.rotation_v
        self.func['lift'] = Serial.elevator


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
                self.func['move_x'](self.speed)
            elif value[0] == -1: #hat 4
                self.func['move_x'](-self.speed)
            if value[1] == 1: #hat 1
                self.func['move_y'](self.speed)
            elif value[1] == -1: #hat 3
                self.func['move_y'](-self.speed)
                
        elif(action_type == 'button'):
            if (key < 4):
                if key == 0:
                    self.func['lift'](LIFT_UP)
                elif key == 2:
                    self.func['lift'](LIFT_DOWN)
                else:
                    if key == 1:
                        self.func['rotate'](self.speed)
                    elif key == 3:
                        self.func['rotate'](-self.speed)
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
                self.func['move_x'](value)
            elif key == 1:
                self.func['move_y'](-value)
            elif key == 2:
                self.func['rotate'](value)
                

def init():
    global JoyHandler
    JoyHandler = JoyHandler()
    if(JoyHandler.joystick_count == 0):
        print("No joystick found!")
        exit(1)
        

def handle():
    global JoyHandler
    JoyHandler.handle_joy()

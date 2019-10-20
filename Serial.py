#I'll be assuming that return value = 1 mean it's 'ready' for another command.
#and 0 for 'not ready'

import serial

PORT = '/dev/ttyACM0'
ser = None


def setup():
    global ser
    ser = serial.Serial(PORT, 115200, timeout=1)
    st = serial_read()
    if st[-1]=='\n':
        st = st[:-1]

    while not st == "1":
        st = serial_read()
    print("*" + st)


def serial_write(s):
    t = s
    global ser
    if ser is None:
        return "Error"
    ser.write(s.encode('utf-8'))
    return serial_read(t)

######## Driving Function Start Here ########

#There'll be function with speed as argument for manual control and function with unit(distance)
#as an argument for auto control, speed and distance have range from -9999 to 9999
def translation_vy(speed):
    #forward and backward
    #TODO

def translation_vx(speed):
    #left and right
    #TODO

def rotation_v(speed):
    #TODO

def translation_sy(distance):
    #TODO

def translation_sx(distance):
    #TODO

def rotation_s(distance):
    #TODO

def elevator(state):
    #only for manual bot
    if state == 0:
        #go down
    else:
        #go up

def grab(state):
    #for end eff control
    #state = 1 = grab, 0 = release


def grab():
    #legacy function
    print("Grabbing mango")
    if (serial_write("GRAB") == 'SUCCESS'):
        print('Grabbing success')
        return True
    else:
        print("Grabbing error")
        return False

######## End of Driving function ########

def serial_read(cmd=""):
    global ser

    while True:
        if ser.isOpen():
            rl = ser.readline()
        else:
            print("Serial is not available")
            continue
        try:
            rl = rl.decode('utf-8')
        except UnicodeDecodeError:
            rl = str(rl)
        if (rl == "DONE"):
            print('Done')
            setToDefault()
            return 'SUCCESS'
        elif (rl == "GOING FORWARD" or rl == "GOING BACKWARD" or rl == "STOPPED"):
            print('DONE')
            return ('SUCCESS')
        elif (rl == 'RELEASING'):
            setToReleasing()
        elif (rl == 'CUTTING'):
            setToCutting()
        elif (rl == 'GRABBING'):
            setToGrabbing()
        elif (rl == "SETUP DONE"):
            return rl
        elif (rl == ""):
            pass
        else:
            print('msg recieve=' + rl)
            setToDefault()
            return rl


if __name__ == '__main__':
    setup()
#I'll be assuming that return value = 1 mean it's 'ready' for another command.
#and 0 for 'not ready'

import serial


PORT = '/dev/ttyACM0'

ser = None


def setup():
    global ser
    ser = serial.Serial(PORT, 115200, timeout=1)
    #time.sleep(0.6)        #wait for arduino to setup, not really neccessary
    ser.close()
    #st = serial_read()
    #while not st == "1":
    #    st = serial_read()  #wait "1" from arduino to confirm connection
    print("Setup done")


def serial_write(s):
    ser = serial.Serial(PORT, 115200, timeout=1)
    if ser is None:
        return "Error"
    #print(s.encode())
    ser.write(s.encode())
    ser.close()
    #return serial_read()
#write data and returns the feedback msg from arduino

######## Driving Function Start Here ########


#There'll be function with speed as argument for manual control and function with unit(distance)
#as an argument for auto control, speed and distance have range from -9999 to 9999
def translation(x,y,z):
    data = [x,y,z]
    cmd = ""
    for d in data:
        if d>=0:
            d = str(d)
            d = "0"*(4-len(d))+d
        else:
            d = str(d)[1:]
            d = "1"+"0"*(3-len(d))+d
        cmd = cmd+d
    serial_write("!"+cmd)
    #print("!" + cmd)
#legacy translation function


def elevator(state):
    #only for manual bot
    if state == 1:
        serial_write("@u")
    elif state == -1:
        serial_write("@d")

def gripper(state):
    #for end eff control
    #state = 1 = grab, 0 = release"""
    if state == 1:
        serial_write("@g")
    elif state == 0:
        serial_write("@r")
        


if __name__ == '__main__':
    setup()

    while 1:
        x, y, z = [int(e) for e in input().strip().split()]
        translation(x,y,z)


#for arduino, use println(String) to communicate. Following codes is for echo

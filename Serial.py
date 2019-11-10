#I'll be assuming that return value = 1 mean it's 'ready' for another command.
#and 0 for 'not ready'

import serial
import time

PORT = '/dev/ttyACM0'
ser = None


def setup():
    global ser
    
    time.sleep(0.6)        #wait for arduino to setup, not really neccessary
    #st = serial_read()
    #while not st == "1":
    #    st = serial_read()  #wait "1" from arduino to confirm connection
    print("Setup done")


def serial_write(s):
    ser = serial.Serial(PORT, 115200, timeout=1)
    if ser is None:
        return "Error"
    print(s.encode())
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

'''def translation_vy(speed):
    if speed>0:
        serial_write(str([0,1,0,speed]))
    else:
        serial_write(str([0,0,0,speed]))
    #forward and backward
#
def translation_vx(speed):
    if speed>0:
        serial_write(str([1,1,0,speed]))
    else:
        serial_write(str([1,0,0,speed]))
    #right and left
def rotation_v(speed):
    if speed>0:
        serial_write(str([2,1,0,speed]))
    else:
        serial_write(str([2,0,0,speed]))
    #cw and ccw

def translation_sy(distance):
    if speed>0:
        serial_write(str([0,1,1,distance]))
    else:
        serial_write(str([0,0,1,distance]))

def translation_sx(distance):
    if speed>0:
        serial_write(str([1,1,1,distance]))
    else:
        serial_write(str([1,0,1,distance]))

def rotation_s(distance):
    if speed>0:
        serial_write(str([2,1,1,distance]))
    else:
        serial_write(str([2,0,1,distance]))'''

"""def elevator(state):
    #only for manual bot
    if state == 0:
        #go down
    else:
        #go up

def grab(state):
    #for end eff control
    #state = 1 = grab, 0 = release"""
#TODO

"""def grab():
    print("Grabbing mango")
    if (serial_write("GRAB") == 'SUCCESS'):
        print('Grabbing success')
        return True
    else:
        print("Grabbing error")
        return False"""
#legacy function

######## End of Driving function ########
'''
def serial_read():
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
            print("UDE")
        if len(rl)>0:
            rl = rl.strip()
        print("Recieved: "+rl)
        return rl'''
#reads line, returns the data after printing it on the console
    
if __name__ == '__main__':
    setup()
    x, y, z = [int(e) for e in input().strip().split()]
    translation(x,y,z)


#for arduino, use println(String) to communicate. Following codes is for echo
"""
char data;
char str[2];
void setup() {
  Serial.begin(115200);
  str[1] = '\0';
  pinMode(13,OUTPUT);
  digitalWrite(13,LOW);
  Serial.println("1"); //tell py set up is done
}

void loop() {
  if(Serial.available() > 0) {
    data = Serial.read();
    str[0] = data;
    Serial.print(str);
  }
  Serial.flush();
}
"""

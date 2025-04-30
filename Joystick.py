import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

import socket

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create ADS object
ads = ADS1115(i2c)
Lx = AnalogIn(ads, 0)
Ly = AnalogIn(ads, 1)
Ry = AnalogIn(ads, 2)
Rx = AnalogIn(ads, 3)

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to an address and port
ipAddr = "192.168.69.69"
port =  2222

PrevHoldingRDown = False
PrevHoldingRUp = False
PrevHoldingRLeft = False
PrevHoldingRRight = False

HoldingRDown = False
HoldingRUp = False
HoldingRLeft = False
HoldingRRight = False


while True:
    #Reset All Current Conditions of Right Joystick State
    
    HoldingRDown = False
    HoldingRUp = False
    HoldingRLeft = False
    HoldingRRight = False

    print(Ry.value)
    if Ry.value < 100: #check for when holding down
         HoldingRDown = True 
         if not PrevHoldingRDown:
                server.sendto(b"RDown", (ipAddr, port))
                print("Right Joystick: Down")

    elif Ry.value == 32767:
         HoldingRUp = True
         if not PrevHoldingRUp: 
               print("Right Joystick: Up")
               server.sendto(b"RUp", (ipAddr, port))
    else:
          if PrevHoldingRDown:
                HoldingRDown = False
                server.sendto(b"RDownNot", (ipAddr,port))
                print("Right Joystick: NOT Down")
          elif PrevHoldingRUp:
                HoldingRUp = False
                server.sendto(b"RUpNot", (ipAddr,port))
                print("Right Joystick: NOT Up")
    if Rx.value < 100:
        server.sendto(b"RLeft", (ipAddr, port))
#        print("Right Joystick: :Left")
    if Rx.value == 32767:
        server.sendto(b"RRight", (ipAddr, port))
#        print("Right Joystick: Right")
    if Rx.value >= 100  and Rx.value != 32767 and Ry.value >= 100 and Ry.value != 32767:
        server.sendto(b"RNone", (ipAddr, port))
#        print("Right Joystick: None")
    else:
        print("\n")
    
    if Ly.value < 100:
       server.sendto(b"LDown", (ipAddr, port))
#       print("Left Joystick: Down")
    if Ly.value == 32767:
       server.sendto(b"LUp", (ipAddr, port))
#       print("Left Joystick: Up")
    if Lx.value < 100:
       server.sendto(b"LLeft", (ipAddr, port))
#       print("Left Joystick: Left")

    if Lx.value == 32767:
       server.sendto(b"LRight", (ipAddr, port))
#       print("Left Joystick: Right")

    #Change Current States to Previous States
    PrevHoldingRDown = HoldingRDown
    PrevHoldingRUp = HoldingRUp

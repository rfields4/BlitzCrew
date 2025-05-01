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

PrevHoldingLDown = False
PrevHoldingLUp = False
PrevHoldingLLeft = False
PrevHoldingLRight = False

HoldingRDown = False
HoldingRUp = False
HoldingRLeft = False
HoldingRRight = False

HoldingLDown = False
HoldingLUp = False
HoldingLLeft = False
HoldingLRight = False

while True:
    #Reset All Current Conditions of Right Joystick State
    
    HoldingRDown = False
    HoldingRUp = False
    HoldingRLeft = False
    HoldingRRight = False
    
    HoldingLDown = False
    HoldingLUp = False
    HoldingLLeft = False
    HoldingLRight = False

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
         HoldingRLeft = True
         if not PrevHoldingRLeft:
               print("Right Joystick: Left")
               server.sendto(b"RLeft", (ipAddr, port))
    elif Rx.value = 32767:
         HoldingRRight = True
         if not PrevHoldingRRight:
               print("Right Joystick: Right")
               server.sendto(b"RRight", (ipAddr, port))
    else:
        if PrevHoldingRLeft:
                HoldingRLeft = False
                server.sendto(b"RLeftNot", (ipAddr, port))
                print("Right Joystick: NOT Left")
        elif PrevHoldingRRight:
                HoldingRRight = False
                server.sendto(b"RRightNot", (ipAddr, port))
                print("Right Joystick: NOT Right")
                    
    if Ly.value < 100: #check for when holding down
         HoldingLDown = True 
         if not PrevHoldingLDown:
                server.sendto(b"LDown", (ipAddr, port))
                print("Left Joystick: Down")
    elif Ly.value == 32767:
         HoldingLUp = True
         if not PrevHoldingLUp: 
               print("Left Joystick: Up")
               server.sendto(b"LUp", (ipAddr, port))
    else:
          if PrevHoldingLDown:
                HoldingLDown = False
                server.sendto(b"LDownNot", (ipAddr,port))
                print("Left Joystick: NOT Down")
          elif PrevHoldingLUp:
                HoldingLUp = False
                server.sendto(b"LUpNot", (ipAddr,port))
                print("Left Joystick: NOT Up")
    if Lx.value < 100:
         HoldingLLeft = True
         if not PrevHoldingLLeft:
               print("Left Joystick: Left")
               server.sendto(b"LLeft", (ipAddr, port))
    elif Lx.value = 32767:
         HoldingLRight = True
         if not PrevHoldingLRight:
               print("Left Joystick: Right")
               server.sendto(b"LRight", (ipAddr, port))
    else:
        if PrevHoldingLLeft:
                HoldingLLeft = False
                server.sendto(b"LLeftNot", (ipAddr, port))
                print("Left Joystick: NOT Left")
        elif PrevHoldingLRight:
                HoldingLRight = False
                server.sendto(b"LRightNot", (ipAddr, port))
                print("Left Joystick: NOT Right")

    #Change Current States to Previous States
    PrevHoldingRDown = HoldingRDown
    PrevHoldingRUp = HoldingRUp
    PrevHoldingRLeft = HoldingRLeft
    PrevHoldingRRight = HoldingRRight
    
    PrevHoldingLDown = HoldingLDown
    PrevHoldingLUp = HoldingLUp
    PrevHoldingLLeft = HoldingLLeft
    PrevHoldingLRight = HoldingLRight

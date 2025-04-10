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

while True:
    # Read from a single-ended input (A0)
    
   # print("Raw ADC Value:", chan.value)
    if Ry.value < 100:
        server.sendto(b"RDown", (ipAddr, port))
        print("Right Joystick: Down")
    if Ry.value == 32767:
        print("Right Joystick: Up")
        server.sendto(b"RUp", (ipAddr, port))
    if Rx.value < 100:
        server.sendto(b"RLeft", (ipAddr, port))
        print("Right Joystick: :Left")
    if Rx.value == 32767:
        server.sendto(b"RRight", (ipAddr, port))
        print("Right Joystick: Right")

    else:
       # print(Lx.value)
        print("\n")
    
    if Ly.value < 100:
       server.sendto(b"LDown", (ipAddr, port))
       print("Left Joystick: Down")
    if Ly.value == 32767:
       server.sendto(b"LUP", (ipAddr, port))
       print("Left Joystick: Up")
    if Lx.value < 100:
       server.sendto(b"LLeft", (ipAddr, port))
       print("Left Joystick: Left")

    if Lx.value == 32767:
       server.sendto(b"LRight", (ipAddr, port))
       print("Left Joystick: Right")


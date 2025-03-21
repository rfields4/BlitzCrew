import board
import busio
from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

import socket

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create ADS object
ads = ADS1115(i2c)
Lx = AnalogIn(ads, 3)
Ly = AnalogIn(ads, 2)
Rx = AnalogIn(ads, 1)
Ry = AnalogIn(ads, 0)

# Create a UDP socket
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to an address and port
ipAddr = "192.168.69.69"
port =  2222

while True:
    # Read from a single-ended input (A0)

   # print("Raw ADC Value:", chan.value)
    if Ry.value < 100:
        server.sendto(b"Up", (ipAddr, port))
        print("Right Joystick: Up")
    elif Ry.value == 32767:
        print("Right Joystick: Down")
        server.sendto(b"Down", (ipAddr, port))
    elif Rx.value < 100:
        server.sendto(b"Right", (ipAddr, port))
        print("Right Joystick: Right")
    elif Rx.value == 32767:
        server.sendto(b"Left", (ipAddr, port))
        print("Right Joystick: Left")

    else:
        #print(Lx.value)
        print("\n")

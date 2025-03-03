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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Set socket options
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind the socket to an address and port
server_address = ("10.127.19.68", 2222)
server_socket.bind(server_address)

# Listen for incoming connections (max 1 client in this case)
print(f"Listening on {server_address}")
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

while True:
    # Read from a single-ended input (A0)

   # print("Raw ADC Value:", chan.value)
    if Lx.value < 100:
        client_socket.sendall(b"Left")
        print("Left Joystick: Left")
    elif Lx.value == 32767:
        print("Left Joystick: Right")
        client_socket.sendall(b"Right")
   

    else:
        #print(Lx.value)
        print("\n")

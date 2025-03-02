import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio
def cameraAngleControl():
    commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    commsPort.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ipAddr = "127.0.0.1"
    server_address = (ipAddr, 2222)
    commsPort.bind(server_address)
    commsPort.setblocking(False)
    while True:
        try:
            data, address = commsPort.recvfrom(4096)  # Receive data (4096 is the buffer size)

            if data:
                print("dataReceived")
        except BlockingIOError:
            pass

    factory = PiGPIOFactory()
    servo = AngularServo(12, min_angle=0,
    max_angle=180, min_pulse_width=0.0005, 
    max_pulse_width=0.0024, pin_factory=factory)                   
    servo.angle = 0

    while True:
        key = 'w'
        if key == "w" and servo.angle != 180:
            servo.angle = servo.angle + 1
            sleep(0.000001)
        if key == "s" and servo.angle != 0:
            servo.angle = servo.angle - 1
            sleep(0.000001)

import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio

def cameraAngleControl():
    commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ipAddr = "192.168.69.69"
    commsPort.bind((ipAddr, 5005))    

    # servo setup
    factory = PiGPIOFactory()
    servoVertical = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)                   
    servoVertical.angle = 0
    
    while True:
        try:
            data = commsPort.recv(1024)  # Receive data (4096 is the buffer size)

            if data:
                print(data)
                if data == b"Left" and servoVertical.angle != 180:
                    servoVertical.angle = servoVertical.angle + 1
                    sleep(0.000001)
                if data == "Right" and servoVertical.angle != 0:
                    servoVertical.angle = servoVertical.angle - 1
                    sleep(0.000001)
        except BlockingIOError:
            pass
            
    

        

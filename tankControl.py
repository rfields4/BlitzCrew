import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio
import RPi.GPIO as GPIO

def cameraAngleControl():

    leftTreadPin = 39
    rightTreadPin = 40

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leftTreadPin, GPIO.OUT)
    GPIO.setup(rightTreadPin, GPIO.OUT)
    
    commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ipAddr = "192.168.69.69"
    commsPort.bind((ipAddr, 5005))    

    leftpwmPin = GPIO.PWM(leftTreadPin, 100)
    rightpwmPin = GPIO.PWM(rightTreadPin, 100)
    
    leftpwmPin.start(0)
    rightpwmPin.start(0)

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
                elif data == "Right" and servoVertical.angle != 0:
                    servoVertical.angle = servoVertical.angle - 1
                    sleep(0.000001)
                if data == "LRight":
                    leftpwmPin.ChangeDutyCycle(100)
                    sleep(0.01)
                if data == "LLeft":
                    leftpwmPin.ChangeDutyCycle(100)
                    sleep(.01)
                
                if data == b"Left" and servoHorizontal.angle < 297:
                    servoHorizontal.angle = servoHorizontal.angle + 2
                    sleep(0.000001)
                if data == b"Right" and servoHorizontal.angle > 3:
                    servoHorizontal.angle = servoHorizontal.angle - 2
                    sleep(0.000001)
        except BlockingIOError:
            pass
            
    

        

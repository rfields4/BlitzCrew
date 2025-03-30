import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio
import RPi.GPIO as GPIO

def cameraAngleControl():

    leftTreadPin = 21 #PIN 40
    rightTreadPin = 26 #PIN 37

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(leftTreadPin, GPIO.OUT)
    GPIO.setup(rightTreadPin, GPIO.OUT)
    
    commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ipAddr = "192.168.69.69"
    commsPort.bind((ipAddr, 2222))    

    leftpwmPin = GPIO.PWM(leftTreadPin, 100)
    rightpwmPin = GPIO.PWM(rightTreadPin, 100)
    
    leftpwmPin.start(0)
    rightpwmPin.start(0)

    # servo setup
    factory = PiGPIOFactory()
    
    servoHorizontal = AngularServo(13, min_angle=0, max_angle=300, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)
    servoVertical = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)                   
    servoVertical.angle = 90
    servoHorizontal.angle = 150
    
    while True:
        try:
            data, address = commsPort.recvfrom(1024)  # Receive data (4096 is the buffer size)
            print(data)
            if data:
                print(data)
                if data == b"RUp" and servoVertical.angle + 5 < 180:
                    servoVertical.angle = servoVertical.angle + 5
                    sleep(0.000001)
                    print(servoVertical.angle)
                elif data == b"RDown" and servoVertical.angle - 5  > 0:
                    servoVertical.angle = servoVertical.angle - 5
                    sleep(0.000001)
                    print(servoVertical.angle)
                if data == b"LRight":
                    rightpwmPin.ChangeDutyCycle(100)
                    sleep(0.01)
                if data == b"LLeft":
                    leftpwmPin.ChangeDutyCycle(100)
                    sleep(.01)
                if data == b"LUp":
                    leftTreadPin.ChangeDutyCycle(100)
                    leftTreadPin.ChangeDutyCycle(100)
                    sleep(.01)
                
                if data == b"RLeft" and servoHorizontal.angle + 7 < 300:
                    servoHorizontal.angle = servoHorizontal.angle + 7
                    sleep(0.000001)
                if data == b"RRight" and servoHorizontal.angle - 7 > 0:
                    servoHorizontal.angle = servoHorizontal.angle - 7
                    sleep(0.000001)
        except BlockingIOError:
            pass
            
    

        

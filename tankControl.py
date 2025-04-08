
import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio
import RPi.GPIO as GPIO

def cameraAngleControl():

    GPIO.setmode(GPIO.BCM)

    leftTreadPin1  = 27 #PIN 13 ForwardPin
    GPIO.setup(27, GPIO.OUT)
    leftTreadPin2  = 22 #PIN 15 BackPin
    GPIO.setup(22, GPIO.OUT)
    rightTreadPin1 = 23 #PIN 16 ForwardPin
    GPIO.setup(23, GPIO.OUT)
    rightTreadPin2 = 24 #Pin 18 BackPin
    GPIO.setup(24, GPIO.OUT)

    leftpwmPin = 5 #PIN 29
    GPIO.setup(leftpwmPin, GPIO.OUT)
    rightpwmPin= 6 #PIN 31
    GPIO.setup(rightpwmPin, GPIO.OUT)
    
    commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    ipAddr = "192.168.69.69"
    commsPort.bind((ipAddr, 2222))    

    leftpwmPin = GPIO.PWM(5, 100)
    rightpwmPin = GPIO.PWM(6, 100)
    
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
                    GPIO.output(27, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(23, GPIO.LOW)
                    GPIO.output(24, GPIO.HIGH)

                    rightpwmPin.ChangeDutyCycle(30)
                    leftpwmPin.ChangeDutyCycle(60)
                    sleep(0.01)
                if data == b"LLeft":
                    GPIO.output(27, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(23, GPIO.HIGH)
                    GPIO.output(24, GPIO.LOW)

                    rightpwmPin.ChangeDutyCycle(60)
                    leftpwmPin.ChangeDutyCycle(30)
                    sleep(.01)
                if data == b"LUp":
                    GPIO.output(27, GPIO.HIGH)
                    GPIO.output(22, GPIO.LOW)
                    GPIO.output(23, GPIO.HIGH)
                    GPIO.output(24, GPIO.LOW)

                    rightpwmPin.ChangeDutyCycle(80)
                    leftpwmPin.ChangeDutyCycle(80)
                    sleep(.1)
                    rightpwmPin.ChangeDutyCycle(0)
                    leftpwmPin.ChangeDutyCycle(0)
                if data == b'LDown':
                    GPIO.output(27, GPIO.LOW)
                    GPIO.output(22, GPIO.HIGH)
                    GPIO.output(23, GPIO.LOW)
                    GPIO.output(24, GPIO.HIGH)

                    rightpwmPin.ChangeDutyCycle(80)
                    leftpwmPin.ChangeDutyCycle(80)
                    sleep(.1)
                    rightpwmPin.ChangeDutyCycle(0)
                    leftpwmPin.ChangeDutyCycle(0)
                if data == b"RLeft" and servoHorizontal.angle + 7 < 300:
                    servoHorizontal.angle = servoHorizontal.angle + 7
                    sleep(0.000001)
                if data == b"RRight" and servoHorizontal.angle - 7 > 0:
                    servoHorizontal.angle = servoHorizontal.angle - 7
                    sleep(0.000001)
        except BlockingIOError:
            pass
            
    

        

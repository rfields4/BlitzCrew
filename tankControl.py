import RPi.GPIO as GPIO
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep

factory = PiGPIOFactory()
servo = AngularServo(12, min_angle=0,
 max_angle=180, min_pulse_width=0.0005, 
 max_pulse_width=0.0024, pin_factory=factory)                   

servo.angle = 0

while True:
    key = input()
    if key == "w" and servo.angle != 180:
        servo.angle = servo.angle + 1
        sleep(0.000001)
    if key == "s" and servo.angle != 0:
        servo.angle = servo.angle - 1
        sleep(0.000001)

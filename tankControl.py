import RPi.GPIO as GPIO
from gpiozero import Servo
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
#GPIO.setup(13, GPIO.OUT)

p = GPIO.PWM(12,50)
#q = GPIO.PWM(13,50)
#q.start(7)


p.start(2.5)

p.ChangeDutyCycle(2.5)
time.sleep(5)
p.ChangeDutyCycle(11.5)
time.sleep(5)

#servo = Servo(13)

#for i in range(-150,150):
#    servo.angle = i
#    sleep(0.1)
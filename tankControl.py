import pigpio
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import AngularServo
from time import sleep
import socket
import asyncio

class TankControl():

      def __init__(self):
          pi = pigpio.pi()
          self.leftTreadForwardPin  = 27 #PIN 13 ForwardPin
          self.leftTreadBackPin  = 22 #PIN 15 BackPin
 
          self.rightTreadForwardPin = 23 #PIN 16 ForwardPin
          self.rightTreadBackPin = 24 #Pin 18 BackPin

          self.leftPWM = 6 #PIN 29
          self.rightPWM= 5 #PIN 31

          #Setup Pins
          pi.set_mode(self.leftTreadForwardPin, pigpio.OUTPUT)
          pi.set_mode(self.leftTreadBackPin, pigpio.OUTPUT)
          pi.set_mode(self.rightTreadForwardPin, pigpio.OUTPUT)
          pi.set_mode(self.rightTreadBackPin, pigpio.OUTPUT)

          pi.set_mode(self.leftTreadForwardPin, pigpio.OUTPUT)
          pi.set_mode(self.rightTreadBackPin, pigpio.OUTPUT)

          #Configure PWM Signals
          pi.set_PWM_frequency(self.leftPWM, 10)
          pi.set_PWM_frequency(self.rightPWM, 10)
          pi.set_PWM_dutycycle(self.leftPWM, 0)
          pi.set_PWM_dutycycle(self.rightPWM, 0)

          #leftpwmPin = GPIO.PWM(6, 10)
          #rightpwmPin = GPIO.PWM(5, 10)    
          #leftpwmPin.start(0)
          #rightpwmPin.start(0)
    
          self.commsPort = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
          ipAddr = "192.168.69.69"
          self.commsPort.bind((ipAddr, 2222))    

          
          factory = PiGPIOFactory()
          # servo setup
          self.servoHorizontal = AngularServo(13, min_angle=0, max_angle=300, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)
          self.servoVertical = AngularServo(12, min_angle=0, max_angle=180, min_pulse_width=0.0005, max_pulse_width=0.0024, pin_factory=factory)                   
          self.servoVertical.angle = 90
          self.servoHorizontal.angle = 150
          self.pi = pi
      async def startTank(self):
            await asyncio.gather(
                 self.handleComms(),
                 self.changeVertCamera())
                 

      def handleComms(self):
            print("CommsStarted")
            servoVertical = self.servoVertical
            servoHorizontal = self.servoHorizontal
            LRight = False
            LLeft  = False
            LUp    = False
            LDown  = False
            while True:
                  try:
                     data, address = self.commsPort.recvfrom(1024)  # Receive data (4096 is the buffer size)
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
                        LRight = True
                        self.moveRight()
                     if data == b"LRightNot":
                        LRight = False 
                  
                     if data == b"LLeftNot":
                        LLeft = False
                    
                     if data == b"LLeft":
                        self.moveLeft()
                        LLeft = True   
             
                     if data == b"LUp":
                        LUp = True
                        self.moveUp()

                     if data == b"LUpNot":
                        LUp = False

                     if data == b"LDownNot":
                        LDown = False
 
           
                     if data == b'LDown':
                        LDown = True
                        self.moveDown()
                     if (not LLeft and not LRight) :
                        if LUp: #If still Holding Up, go back to moving up 
                             self.moveUp()
                        elif LDown: #If still Holding Down, go back to moving down                        
                             self.moveDown()
                        else:
                             self.pi.set_PWM_dutycycle(self.rightPWM,0)
                             self.pi.set_PWM_dutycycle(self.leftPWM, 0)
                            
                     if data == b"RLeft" and servoHorizontal.angle + 7 < 300:
                        servoHorizontal.angle = servoHorizontal.angle + 7
                        sleep(0.000001)
                     if data == b"RRight" and servoHorizontal.angle - 7 > 0:
                        servoHorizontal.angle = servoHorizontal.angle - 7
                        sleep(0.000001)
                  except BlockingIOError:
                     pass

      def moveRight(self):
               self.pi.write(27, 0)
               self.pi.write(22, 1)
               self.pi.write(23, 1)
               self.pi.write(24, 0)

               self.pi.set_PWM_dutycycle(self.rightPWM,255)
               self.pi.set_PWM_dutycycle(self.leftPWM,255)
      
      def moveUp(self):               
                        self.pi.write(27, 0)
                        self.pi.write(22, 1)
                        self.pi.write(23, 0)
                        self.pi.write(24, 1)

                        self.pi.set_PWM_dutycycle(self.rightPWM,255)
                        self.pi.set_PWM_dutycycle(self.leftPWM,255)

      def moveDown(self):
                 self.pi.write(27, 1)
                 self.pi.write(22, 0)
                 self.pi.write(23, 1)
                 self.pi.write(24, 0)

                 self.pi.set_PWM_dutycycle(self.rightPWM,255)
                 self.pi.set_PWM_dutycycle(self.leftPWM, 255)
                        
      def moveLeft(self):
                        self.pi.write(27, 1)
                        self.pi.write(22, 0)
                        self.pi.write(23, 0)
                        self.pi.write(24, 1)

                        self.pi.set_PWM_dutycycle(self.rightPWM,255)
                        self.pi.set_PWM_dutycycle(self.leftPWM,255)
                     
      def changeVertCamera(self):
           pass      
    
   
        

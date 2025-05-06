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
          self.leftTreadBackPin  = 22    #PIN 15 BackPin
 
          self.rightTreadForwardPin = 23 #PIN 16 ForwardPin
          self.rightTreadBackPin = 24    #Pin 18 BackPin

          self.leftPWM = 6               #PIN 29
          self.rightPWM= 5               #PIN 31

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

          self.RRight = False
          self.RLeft = False
          self.RUp =   asyncio.Event()
          self.RDown = asyncio.Event()


      async def startTank(self):
            await asyncio.gather(
                 self.handleComms(),
                 self.changeVertCamera(),
                 self.moveServoUp(),
                 self.moveServoDown())

      async def handleComms(self):
            print("CommsStarted")
            loop = asyncio.get_event_loop()
            servoVertical = self.servoVertical
            servoHorizontal = self.servoHorizontal
            LRight = False
            LLeft  = False
            LUp    = False
            LDown  = False


            while True:
                  try:
                     (data, address) = await loop.run_in_executor(None, self.commsPort.recvfrom, 1024)  # Receive data (4096 is the buffer size)
                     print(data)
                     if data == b"RUp":
                        self.RUp.set()
                        self.RDown.clear()
                     elif data == b"RUpNot":
                        self.RUp.clear()

                     elif data == b"RDown":
                        self.RDown.set()
                        self.RUp.clear()
                     elif data == b"RDownNot":
                        self.RDown.clear()
                     elif data == b"LRight":
                        LRight = True
                        self.moveRight()
                     elif data == b"LRightNot":
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

      async def moveRight(self):
               self.pi.write(27, 0)
               self.pi.write(22, 1)
               self.pi.write(23, 1)
               self.pi.write(24, 0)

               self.pi.set_PWM_dutycycle(self.rightPWM,255)
               self.pi.set_PWM_dutycycle(self.leftPWM,255)
      
      async def moveUp(self):               
                        self.pi.write(27, 0)
                        self.pi.write(22, 1)
                        self.pi.write(23, 0)
                        self.pi.write(24, 1)

                        self.pi.set_PWM_dutycycle(self.rightPWM,255)
                        self.pi.set_PWM_dutycycle(self.leftPWM,255)

      async def moveDown(self):
                 self.pi.write(27, 1)
                 self.pi.write(22, 0)
                 self.pi.write(23, 1)
                 self.pi.write(24, 0)

                 self.pi.set_PWM_dutycycle(self.rightPWM,255)
                 self.pi.set_PWM_dutycycle(self.leftPWM, 255)
                        
      async def moveLeft(self):
                        self.pi.write(27, 1)
                        self.pi.write(22, 0)
                        self.pi.write(23, 0)
                        self.pi.write(24, 1)

                        self.pi.set_PWM_dutycycle(self.rightPWM,255)
                        self.pi.set_PWM_dutycycle(self.leftPWM,255)
                     
      async def moveServoUp(self):
          while True: #keep Thread Alive
            await self.RUp.wait()
            while self.RUp.is_set() and self.servoVertical.angle + 1 < 180:   
                self.servoVertical.angle = self.servoVertical.angle +1
                await asyncio.sleep(.001)
            await asyncio.sleep(.001)
 
      async def moveServoDown(self):
         while True: #keep Thread Alive
           await self.RDown.wait()
           while self.RDown.is_set() and self.servoVertical.angle - 1 > 0:
               self.servoVertical.angle = self.servoVertical.angle -1
               await asyncio.sleep(.0001)
           await asyncio.sleep(.0001)
      async def moveServoLeft(self):
                 self.servoHorizontal.angle = self.servoHorizontal.angle +1

      async def moveServoRight(self):
                 servoHorizontal.angle = servoHorizontal.angle -1

      async def changeVertCamera(self):
           pass      
    
   
        

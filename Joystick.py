import board
import busio
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1115 import ADS1115

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Create ADS object
ads = ADS1115(i2c)
Lx = AnalogIn(ads, 3)
Ly = AnalogIn(ads, 2)
Rx = AnalogIn(ads, 1)
Ry = AnalogIn(ads, 0)

while True:
    # Read from a single-ended input (A0)

   # print("Raw ADC Value:", chan.value)
    if Lx.value < 100:
        print("Left Joystick: Left")
    elif Lx.value == 32767:
        print("Left Joystick: Right")

   

    else:
        #print(Lx.value)
        print("\n")
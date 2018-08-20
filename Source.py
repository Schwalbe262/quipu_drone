//Joystick_01_Debug_01

#-------------------------------------------------
#-------------------------------------------------
#-------------------------------------------------

print("\nRaspberryPi Debug Test 01\n")

while True:
    continue

//===================================================================================================================================
//Joystick_01_Debug_02
#-------------------------------------------------
import time

#-------------------------------------------------
i = 0
#-------------------------------------------------

print("\nRaspberryPi Debug Test 02\n")

while True:
    print(i)
    i += 1

    if i > 10:
        i = 0
        print("Console Test\n")

    time.sleep(0.3)


//===================================================================================================================================
//Joystick_02_Variable
#-------------------------------------------------
import time

#-------------------------------------------------
i = 0
#-------------------------------------------------

print("\nRaspberryPi Variable Test\n")

for i in range(100):
    print(i)
    time.sleep(0.1)

while True:
    continue


//===================================================================================================================================
//Joystick_03_String_01
#-------------------------------------------------
#-------------------------------------------------
testString = ""
#-------------------------------------------------

print("\nRaspberryPi String Test 01\n")

testString = "1234567890"
print(testString)

while True:
    continue


//===================================================================================================================================
//Joystick_03_String_02
#-------------------------------------------------
#-------------------------------------------------
testString = ""
#-------------------------------------------------

print("\nRaspberryPi String Test 02\n")

testString = "1234567890"
print(testString)

testString = "abc"
print(testString)

while True:
    continue


//===================================================================================================================================
//Joystick_04_Pio_01
#-------------------------------------------------
import time
import RPi.GPIO as GPIO

#-------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#-------------------------------------------------
pio_list = [22, 27, 17, 23, 24, 25]

for i in range(6):
    GPIO.setup(pio_list[i], GPIO.IN)

#-------------------------------------------------

print("\nRaspberryPi Pio Test 01\n")

while True:
    if GPIO.input(pio_list[4]) == 0:
        print("Press 4")
        time.sleep(0.1)



//===================================================================================================================================
//Joystick_04_Pio_02
#-------------------------------------------------
import time
import RPi.GPIO as GPIO

#-------------------------------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#-------------------------------------------------
pio_list = [22, 27, 17, 23, 24, 25]

for i in range(6):
    GPIO.setup(pio_list[i], GPIO.IN)

#-------------------------------------------------

print("\nRaspberryPi Pio Test 02\n")

while True:
    if GPIO.input(pio_list[0]) == 0:
        print("Press 0")
        time.sleep(0.1)
    if GPIO.input(pio_list[1]) == 0:
        print("Press 1")
        time.sleep(0.1)
    if GPIO.input(pio_list[2]) == 0:
        print("Press 2")
        time.sleep(0.1)
    if GPIO.input(pio_list[3]) == 0:
        print("Press 3")
        time.sleep(0.1)
    if GPIO.input(pio_list[4]) == 0:
        print("Press 4")
        time.sleep(0.1)
    if GPIO.input(pio_list[5]) == 0:
        print("Press 5")
        time.sleep(0.1)
        
        
        
//===================================================================================================================================
//Joystick_05_Spi_Adc_01      
#-------------------------------------------------
import time
import spidev

#-------------------------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

#-------------------------------------------------
#-------------------------------------------------

print("\nRaspberryPi SPI-Adc Test 01\n")

while True:
    data = spi.xfer2([1, (0x08 + 2) << 4, 0])
    adc_out = ((data[1] & 0x03) << 8) + data[2]
    time.sleep(0.01)
    
    print(adc_out)
    time.sleep(0.01)
    
    
//===================================================================================================================================
//Joystick_05_Spi_Adc_02
#-------------------------------------------------
import time
import spidev

#-------------------------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

#-------------------------------------------------
#-------------------------------------------------

print("\nRaspberryPi SPI-Adc Test 02\n")

while True:
    data = spi.xfer2([1, (0x08 + 2) << 4, 0])
    adc_out2 = ((data[1] & 0x03) << 8) + data[2]
    time.sleep(0.01)

    data = spi.xfer2([1, (0x08 + 3) << 4, 0])
    adc_out3 = ((data[1] & 0x03) << 8) + data[2]
    time.sleep(0.01)

    print("adc2 = %d   adc3 = %d" %(adc_out2, adc_out3))
    time.sleep(0.01)

    
//===================================================================================================================================
//Joystick_05_Spi_Adc_03
#-------------------------------------------------
import time
import spidev

#-------------------------------------------------
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

#-------------------------------------------------
def analog_read(channel):
    data = spi.xfer2([1, (0x08 + channel) << 4, 0])
    adc_out = ((data[1] & 0x03) << 8) + data[2]
    time.sleep(0.01)
    
    return adc_out

#-------------------------------------------------

print("\nRaspberryPi SPI-Adc Test 03\n")

while True:
    adc2 = analog_read(2)
    adc3 = analog_read(3)
    
    print("adc2 = %d   adc3 = %d" %(adc2, adc3))
    time.sleep(0.01)






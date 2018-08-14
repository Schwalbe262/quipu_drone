#-------------------------------------------------
import serial
import RPi.GPIO as GPIO
import time
import spidev

#-------------------------------------------------
ser = serial.Serial('/dev/ttyS0',9600,timeout=0.001)
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

currentStep = 1
oldStep = 0
uartString = ""
uartLength = 0

startBit = 0xf0
commandBit  = 0xa1
roll  = 100
pitch = 100
yaw = 100
throttle = 0
operationBit = 0x05
checkSum = 0

firstRoll = 0
firstPitch = 0

#-------------------------------------------------
def checkNextStep():
    global currentStep
    global oldStep
    global uartString

    time.sleep(0.3)
    uartString = ""
    oldStep = currentStep
    currentStep = 0

def checkCrLfProcess():
    global currentStep
    global oldStep
    global uartString
    global uartLength
    
    while ser.inWaiting():
        uartString += ser.read()
        uartLength = len(uartString)
        if uartLength > 4 and uartString.find("\r\n",0,2) == 0 \
        and uartString.find("\r\n",uartLength-2) == uartLength - 2:
            currentStep = oldStep
            currentStep += 1
            break


def analog_read(channel):
    data = spi.xfer2([1, (0x08 + channel) << 4, 0])
    adc_out = ((data[1] & 0x03) << 8) + data[2]
    time.sleep(0.04)
    
    return adc_out

def checkThrottle():
    global throttle
    
    if GPIO.input(switch_list[1]) == 0:
        if throttle > 59:
            throttle -= 20
        elif throttle > 3:
            throttle -= 4
    
    if GPIO.input(switch_list[0]) == 0:
        if throttle < 20:
           throttle = 20
        elif throttle < 181:
            throttle += 20

def checkPitch():
    global pitch
    global firstPitch

    secondPitch = analog_read(3)

    if secondPitch < firstPitch - 450:
        pitch = 75
    elif secondPitch < firstPitch - 350:
        pitch = 80
    elif secondPitch < firstPitch - 250:
        pitch = 85
    elif secondPitch < firstPitch - 150:
        pitch = 90
    elif secondPitch < firstPitch - 50:
        pitch = 95
    elif secondPitch < firstPitch + 50:
        pitch = 100
    elif secondPitch < firstPitch + 150:
        pitch = 105
    elif secondPitch < firstPitch + 250:
        pitch = 110
    elif secondPitch < firstPitch + 350:
        pitch = 115
    elif secondPitch < firstPitch + 450:
        pitch = 120
    else:
        pitch = 125

def checkRoll():
    global roll
    global firstRoll

    secondRoll = analog_read(2)
    
    if secondRoll < firstRoll - 450:
        roll = 75
    elif secondRoll < firstRoll - 350:
        roll = 80
    elif secondRoll < firstRoll - 250:
        roll = 85
    elif secondRoll < firstRoll - 150:
        roll = 90
    elif secondRoll < firstRoll - 50:
        roll = 95
    elif secondRoll < firstRoll + 50:
        roll = 100
    elif secondRoll < firstRoll + 150:
        roll = 105
    elif secondRoll < firstRoll + 250:
        roll = 110
    elif secondRoll < firstRoll + 350:
        roll = 115
    elif secondRoll < firstRoll + 450:
        roll = 120
    else:
        roll = 125

def checkYaw():
    global yaw

    if GPIO.input(switch_list[2]) == 0:
        yaw = 50
    elif GPIO.input(switch_list[3]) == 0:
        yaw = 150
    else:
        yaw = 100

def checkEmergency():
    global roll
    global pitch
    global yaw
    global throttle
    
    if GPIO.input(switch_list[4]) == 0:
        throttle = 0
        roll = 100
        pitch = 100
        yaw = 100

def sendDroneCommand():
    ser.write("at+writeh0006")

    ser.write(hex(startBit)[2:4])
    ser.write(hex(commandBit)[2:4])
    ser.write(hex(roll)[2:4])
    ser.write(hex(pitch)[2:4])
    ser.write(hex(yaw)[2:4])
    
    if throttle < 0x10:
        ser.write('0'+hex(throttle)[2:4])
    else:
        ser.write(hex(throttle)[2:4])
    
    ser.write('0'+hex(operationBit)[2:4])
    
    if checkSum < 0x10:
        ser.write('0'+hex(checkSum)[2:4])
    else:
        ser.write(hex(checkSum)[2:4])

    ser.write("\r")

def checkCRC():
    global commandBit
    global roll
    global pitch
    global yaw
    global throttle
    global operationBit
    global checkSum

    checkSum = commandBit + roll + pitch + yaw + throttle + operationBit
    checkSum = checkSum & 0x00ff

#-------------------------------------------------
switch_list = [22, 27, 17, 23, 24, 25]

for i in range(6):
    GPIO.setup(switch_list[i], GPIO.IN)

print("\nRaspberryPi Drone Joystick Shield Started!\n")

while True:
    if currentStep == 0:
        checkCrLfProcess()
    
    elif currentStep == 1:
        if GPIO.input(switch_list[4]) == 0:
            ser.flushOutput()
            ser.flushInput()
            uartString = ""
            firstRoll = analog_read(2)
            firstPitch = analog_read(3)
            ser.write("atd")
            ser.write("083a5c1f015b")
            ser.write("\r")
            checkNextStep()
    
    elif currentStep == 2:
        if uartString.find("\r\nOK\r\n",0,6) == 0:
            print("Wait Connect")
            checkNextStep()

        else:
            print("Connect 1 ERROR")
            uartString = ""
            currentStep = 100
    
    elif currentStep == 3:
        if uartString.find("\r\nCONNECT ",0,10) == 0:
            print("Connect OK")
            time.sleep(0.3)
            uartString = ""
            currentStep += 1

        else:
            print("Connect 2 ERROR")
            uartString = ""
            currentStep = 100
    
    elif currentStep == 4:
        checkThrottle()
        checkPitch()
        checkRoll()
        checkYaw()
        checkEmergency()
        checkCRC()
        sendDroneCommand()
        time.sleep(0.1)

        if GPIO.input(switch_list[5]) == 0:
            print("Request Disconnect")
            time.sleep(1)
            ser.flushInput()
            uartString = ""
            ser.write("ath")
            ser.write("\r")
            checkNextStep()
    
    elif currentStep == 5:
        if uartString.find("\r\nOK\r\n",0,6) == 0:
            print("Wait Disconnect")
            checkNextStep()

        else:
            print("Disconnect 1 ERROR")
            uartString = ""
            currentStep = 100
    
    elif currentStep == 6:
        if uartString.find("\r\nDISCONNECT",0,12) == 0:
            print("Disconnect 1 OK")
            checkNextStep()

        else:
            print("Disconnect 2 ERROR")
            uartString = ""
            currentStep = 100
    
    elif currentStep == 7:
        if uartString.find("\r\nREADY",0,7) == 0:
            print("Disconnect 2 OK")
            time.sleep(0.3)
            uartString = ""
            currentStep = 1

        else:
            print("Disconnect 3 ERROR")
            uartString = ""
            currentStep = 100
    
    else:
        if ser.inWaiting():
            uartString = ""
            time.sleep(0.5)
            while ser.inWaiting():
                uartString += ser.read()

            print(uartString)
            uartString = ""

        uartString = raw_input("Enter AT Command: ")
        ser.write(uartString)
        ser.write("\r")
        print("Wait Response Command for 3s...")
        time.sleep(3)

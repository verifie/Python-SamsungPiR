#!/usr/bin/python3


import sys
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

GPIO.setup(7, GPIO.OUT)

sleepon = 0.00000001
sleepoff = sleepon

# Pin Trigger (Not used)
#####################################################
def _checkUartDisabled():
    if self.CONST.UART_DISABLE_CHECK:
        self.l.mutter("[HARDWARE] UART DISABLED = True")
        return True
    else:
        self.l.mutter("[HARDWARE] UART DISABLED = False")
        return False    



# Generate pulses as quickly as possible., with prints on every cycle.
#####################################################
def printPulses():
    pulses = 25
    while pulses > 0 :
        print("pulse")
        GPIO.output(7, True)
        GPIO.output(7, False)  
        pulses = pulses - 1



# Generate pulses based on specified timing using time.sleep
#####################################################
sleepon = 0.00000001
sleepoff = sleepon

def timePulses():
    pulses = 25
    while pulses > 0 :
        GPIO.output(7, True)
        time.sleep(sleepon)
        GPIO.output(7, False)  
        time.sleep(sleepoff)  
        pulses = pulses - 1

# Generate pulses based on specified timing using RPi.GPIO PWM Frequency.
#####################################################

def pwmPulses():
    p = GPIO.PWM(7,50)
    p.start(1)
    input('Press Return to stop:')
    p.stop()
    GPIO.cleanup()


############################################################################################################################################################


# Generate pulses as quickly as possible.
#####################################################
def fastPulses():
    while True:
        onDuty = 4
        offDuty = 9
        while onDuty > 0:
                GPIO.output(7, True)
                onDuty = onDuty - 1
                x = 9000000000000 * 900000000000
        while offDuty > 0:
                GPIO.output(7, False)
                offDuty = offDuty - 1



fastPulses()
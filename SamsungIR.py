
#############################################################################################################################################
# irRemoteRaspberryPi
#
# Purpose :     Generate remote control signals from Python code.
# Detail :      Primarily intended to integrate with a Python Flask to allow web and IFTTT.com / Google Assistant control.
#
# Status :      40 In development.
#
#  Version:
#
#
# v0.07 27/01/2019 2218 PME : Construct CSV reading plan.
# v0.07 27/01/2019 2218 PME : Create a csv dictionary, interpret waveforms from entire remote: Samsung TV, LG Bluray, Maplin LED strip.
# v0.07 27/01/2019 0959 PME : Build converters.
# v0.07 27/01/2019 0959 PME : Execute a binary sequence, rather than the previous sequence of variables. Build converters.
# v0.05 26/01/2019 1613 PME : Testing an IR send! IT WORKED FIRST TIME :) Tv on and off every time.
# v0.04 23/01/2019 2520 PME : Length of message is too short, lengthening
# v0.04 23/01/2019 2250 PME : First trial of Power button sequence.
# v0.03 23/01/2019 2242 PME : Stop reliably for 580us to mimic packet bit sends.  One bit is 21 sub-carrier pulses (counted).
# v0.02 23/01/2019 2240 PME : Trial of different methods to get nearest to exact 38.7kHz PWM with correct duty cycle 
#



#############################################################################################################################################
# importLibraries
#
# Purpose :     Import python code libraries.
# Detail :      
#
# Status :      75 Working and coder tested.
# Version:      v0.01 23/01/2019 2240 PME : Setup to use GPIO pin 7 (4th down on the left.)
#

import time
import csv
#import RPi.GPIO as GPIO



#############################################################################################################################################
# setupGPIO
#
# Purpose :     Setup GPIO output.
# Detail :      Configure the GPIO access.
#
# Status :      75 Working and coder tested.
# Version:      v0.01 23/01/2019 2240 PME : Setup to use GPIO pin 7 (4th down on the left.)
#

#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
#GPIO.setup(7, GPIO.OUT)




#############################################################################################################################################
# gpioTriggerButton
#
# Purpose :     Does nothing. code reference only. Not setup in setupGPIO.
# Detail :      
#
# Status :      0
# Version:      v0.01 23/01/2019 2240 PME : Pasted.
#

def _checkUartDisabled():
    #if self.CONST.UART_DISABLE_CHECK:
        print("[HARDWARE] UART DISABLED = True")





##########################################################################################################################################################################
#
#              Everything below here is about generating the IR remote control signal.



#############################################################################################################################################
# irFrequency
#
# Purpose :     Generate the IR sub-carrier frequency.  This is used by the target device to identify that the signal is intended for it.
# Detail :      The duty cycle is also implemented. Note that the time(x) Python code does not time at the short periods required, so
#               alternative methods of creating a delay are used.  The first is to instruct the GPIO library to set the state of the pin
#               more than once.  The second is to make the CPU to undertake instructions.  In this case, we multiply two large numbers.
#               The multiple state sets cause the longest delay.  The maths cause the shorted and allow for fine tuning.
#               Of course, this is not a calibrated or in any way accurate method, but it generates a reasonably reliable result on my
#               Tektronic TDS3032 Oscilloscope.  There must be a better way of doing this!  (Next step is electronic oscillator, with output
#               controlled by GPIO.  This should be more reliable and require less work on the part of the Raspberry Pi.)
#
# Status :      50 - Tested and working independently at Oscilloscope, but not on a target device.
# Version:      v0.02 23/01/2019 2413 PME : Since this times really well, no point reinventing the wheel. We now accept a bit state (True / False)
#                                           which simply either turns on, or doesnt turn on on the initial state. Second off state remains the same.
# Version:      v0.01 23/01/2019 2240 PME : Tested a reasonably reliable PWM at the right frequency and duty cycle. 
#

def irFrequency(bit):
    # This function generates a single waveform used repeatedly

    # Determine the sub-carrier PWM Duty Cycle ratio
    onDuty = 4
    offDuty = 7

    # Onduty repeats the duty on timing process. onduty can be either on for a 1 bit, or 0 for an off bit.
    while onDuty > 0:
            
        # Set the GPIO hardware state.  This will either be a 0 or a 1 depending on the bit state required.
        #GPIO.output(7, bit)
        
        # Do some extra maths to waste some time to get accurate timing in the waveform.  We do this because
        # time.sleep doesn't get accurate enough.
        x = 9000000000000 * 900000000000

       # Decrease the counter.
        onDuty = onDuty - 1
    

    # Offduty repeats the duty off timing process. offduty is always off.
    while offDuty > 0:

        # Set the GPIO hardware state.  This will always be 0 (off).
        #GPIO.output(7, False)

        # Do some extra maths to waste some time to get accurate timing in the waveform.  We do this because
        # time.sleep doesn't get accurate enough.  Theres probably a better way, but this works for now on a RPi 3b Mark II. 
        y = 9000000000000 * 900000000000
        z = 9000000000000 * 900000000000

        # Decrease the counter.
        offDuty = offDuty - 1



#############################################################################################################################################
# StartBit
#
# Purpose :     The packet start bit.
# Detail :      The start bit is sent before the instruction data.
#
# Status :      40 - Testing and not functional.
# Version:      v0.02 23/01/2019 2418 PME : Oscilloscope reading shows 21 cycles within each data bit pulse length.  On an oscilloscope reading,
#                                           We seem to be more accurate than the remote control now(!), although not tested on a TV yet.
# Version:      v0.01 23/01/2019 2400 PME : Created.
#

def startBit():
    oneBit = 180
    while oneBit > 0:
        irFrequency(True)
        oneBit = oneBit - 1

    oneBit = 180
    while oneBit > 0:
        irFrequency(False)
        oneBit = oneBit - 1



#############################################################################################################################################
# dataBit
#
# Purpose :     Generate the IR pulses for one bit. Set the input variable as True or False for 0 or 1 bit state.
# Detail :      On measuring a remote control, the "1" data bit reliably consisted of 21 pulses.  This creeates reliable data bit pulse lengths
#               in theory.
#
# Status :      40 - Testing and not functional.
# Version:      v0.02 23/01/2019 2418 PME : Oscilloscope reading shows 21 cycles within each data bit pulse length.  On an oscilloscope reading,
#                                           We seem to be more accurate than the remote control now(!), although not tested on a TV yet.
# Version:      v0.01 23/01/2019 2400 PME : Created.
#

def dataBit(onOff):
    oneBit = 24
    while oneBit > 0:
        irFrequency(onOff)
        oneBit = oneBit - 1
    oneBit = 21
    while oneBit > 0:
        irFrequency(False)
        oneBit = oneBit - 1







#############################################################################################################################################
# signalPower
#
# Purpose :     The data signal required for a Power control signal.
# Detail :      The digital sequence.  Note the next stage will be to express this sequence as a decimal representation of a binary sequence.
#
# Status :      20 - Starting.
# Version:      v0.01 23/01/2019 2434 PME : Created.
#

bit1  = 1
bit2  = 0
bit3  = 1
bit4  = 0
bit5  = 1
bit6  = 0
bit7  = 1
bit8  = 1
bit9  = 1
bit10 = 1
bit11 = 1
bit12 = 1
bit13 = 0
bit14 = 1
bit15 = 0
bit16 = 1
bit17 = 0
bit18 = 1
bit19 = 1
bit20 = 1
bit21 = 1
bit22 = 1
bit23 = 1
bit24 = 1
bit25 = 0
bit26 = 1
bit27 = 1
bit28 = 1
bit29 = 1
bit30 = 1
bit31 = 1
bit32 = 1
bit33 = 0
bit34 = 1
bit35 = 1
bit36 = 0
bit37 = 1
bit38 = 0
bit39 = 1
bit40 = 0
bit41 = 1
bit42 = 0
bit43 = 1
bit44 = 0
bit45 = 1
bit46 = 0
bit47 = 1

# not yet used....
irFuncPowerOn = "10101011111101010111111101111111011010101010101"
#decemal 

#sendIR(273)
    



#############################################################################################################################################
# dataPacket
#
# Purpose :     Data packet formation.
# Detail :      Start bits follwed by 47 data bits.
#
# Status :      20 - Starting.
# Version:      v0.01 23/01/2019 2434 PME : Created.
#

def dataPacket():
    startBit()
    dataBit(bit1)
    dataBit(bit2)
    dataBit(bit3)
    dataBit(bit4)
    dataBit(bit5)
    dataBit(bit6)
    dataBit(bit7)
    dataBit(bit8)
    dataBit(bit9)
    dataBit(bit10)
    dataBit(bit11)
    dataBit(bit12)
    dataBit(bit13)
    dataBit(bit14)
    dataBit(bit15)
    dataBit(bit16)
    dataBit(bit17)
    dataBit(bit18)
    dataBit(bit19)
    dataBit(bit20)
    dataBit(bit21)
    dataBit(bit22)
    dataBit(bit23)
    dataBit(bit24)
    dataBit(bit25)
    dataBit(bit26)
    dataBit(bit27)
    dataBit(bit28)
    dataBit(bit29)
    dataBit(bit30)
    dataBit(bit31)
    dataBit(bit32)
    dataBit(bit33)
    dataBit(bit34)
    dataBit(bit35)
    dataBit(bit36)
    dataBit(bit37)
    dataBit(bit38)
    dataBit(bit39)
    dataBit(bit40)
    dataBit(bit41)
    dataBit(bit42)
    dataBit(bit43)
    dataBit(bit44)
    dataBit(bit45)
    dataBit(bit46)
    dataBit(bit47)




#############################################################################################################################################
# sendIR
#
# Purpose :     Send an IR signal.
# Detail :      Repeat the IR signal a few times with a small gap between.
#
# Status :      20 - Starting.
# Version:      v0.01 27/01/2019 1601 PME : Created.
#


def sendIR():

    # The time pause between each IR instruction send.
    pauseAtStart = 0.2

    # The time pause between each IR instruction send.
    pauseBetween = 0.1

    # The number of times each IR instruction is sent.
    repeats = 4

    # Since we are doing a lot of GPIO toggling, we want to avoid any legacy OS / CPU operation when we
    # start sending an IR instruction.  So we'll start by waiting.
    time.sleep(pauseAtStart)

    while repeats > 0:
            time.sleep(pauseBetween)
            dataPacket()
            repeats = repeats - 1




#############################################################################################################################################
# convertBinaryToInteger
#
# Purpose :     Used to work out the waveforms into a shorter, more readable data string. 
# Detail :      Not used in execution, just in reverse engineering IR remote signals and creating a number we can store
#               in a LUT dictionary. To avoid confusion, we call the resulting integer the IR Code (irCode)
#
# Status :      20 - Starting.
# Version:      v0.01 27/01/2019 0956 PME : Created.
#

def convertBinaryToInteger(binary):
        irCode = int(binary, 2)
        return irCode



#############################################################################################################################################
# convertIntegerToBinary
#
# Purpose :     Used to work out the waveforms into a shorter, more readable data string. 
# Detail :      Not used in execution, just in reverse engineering IR remote signals and creating a number we can store
#               in a LUT dictionary. 
#
# Status :      20 - Starting.
# Version:      v0.01 27/01/2019 1016 PME : Created.
#

def convertIntegerToBinary(irCode):
        binary = bin(irCode)
        return binary





#### Testing conversions and string reading.

# Get a data source
twofivefive = '11111111'

sourcebinary = irFuncPowerOn
print (sourcebinary)

# Convert the binary to an integer and print it.
irCode = convertBinaryToInteger(sourcebinary)
print (irCode)

# Convert the integer back to a binary and print it.
binary = convertIntegerToBinary(irCode)
print (binary)

# Convert an integer into hex and print it.
irAlt = hex(irCode)
print(irAlt)

# Convert the hex back to an integer and print it.
irCodeBack = int(irAlt, 16)
print(irCodeBack)

# Note the number of characters
test = '55fabfbfb555'
qwe = int(test, 16)
print(qwe)

# Get one character from a string based on its position number (index).
# Really useful guide! https://www.digitalocean.com/community/tutorials/how-to-index-and-slice-strings-in-python-3
stringExample = "Remote Control"
position = 4
print(stringExample[position])

# Work progressively through the string calling a function with the resulting character.  We'll use this to create the
# remote bit state on the fly from the binary string.

# Set IR transmission word length.  We'll use this to progressivelt work through the index.
wordLength = 47

# For loop.
# Reference https://wiki.python.org/moin/ForLoop
for x in range(0, 3):
    print ("We're on time %d" % (x))

# Now work through our binary string and print each bit sequentially.  
wordLengthOne = wordLength - 1
for x in range (0, wordLengthOne):
        print("Character : ", binary[x])

# In the next step we'll changeout the print command and instead pass the character to databit until
# all bits are processed.  This will be done on the fly.


########


with open('IOTRemoteLUT.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')


    line_count = 0
    for row in csv_reader:
        if line_count == 5:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        #else:
        #    print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')

# Read in a CSV.


# Pull a binary word from the csv dictionary. Get the device identifier word.


# Pull an instruction word for the same device


# Append the instruction word following the device identifier word to construct a complete IR word.


#########


# Use the resulting complete IR word to send a full IR signal to the TV.

# Try other devices.

# Create a lookup


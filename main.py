from machine import Pin, PWM, ADC
import time

# PWM outputs for fan control
cpuOutFanPWMPin = PWM(Pin(16))
gpuOutFanPWMPin = PWM(Pin(17))

#EC outputs -> raspberry inputs converted to DC with low pass filter using 10k and 100nF capacitor
cpuECInPin = ADC(26)
gpuECInPin = ADC(27)

# Set the PWM frequency to 23.73 kHz
cpuOutFanPWMPin.freq(22730)
gpuOutFanPWMPin.freq(22730)

# Duty cycle range is 0-65535 (16-bit)
defaultSpeedDutyCycle = int(65535 * 0.4)  # 40% of 65535

cpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)
gpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)

lowestProfileSpeedAllowed = 13107 #20% duty cycle or more

while 1:
    # 16-bit reading (0–65535)
    #read the dc outputs of our low pass filter from EC
    cpuECInValue = int(cpuECInPin.read_u16() / 1.65)
    gpuECInValue = int(gpuECInPin.read_u16() / 1.65)

    #if at least one of the 2 fans has a profile speed higher than the lowest allows, then use profile speed settings from EC
    #armoury crate or other software
    if cpuECInValue >= lowestProfileSpeedAllowed or gpuECInValue >= lowestProfileSpeedAllowed:
        cpuOutFanPWMPin.duty_u16(cpuECInValue)
        gpuOutFanPWMPin.duty_u16(gpuECInValue)
    else: #else use the default speed
        cpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)
        gpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)
        
    time.sleep(0.02)
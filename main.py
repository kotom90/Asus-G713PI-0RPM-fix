from machine import Pin, PWM 
import rp2
import time
from rp2 import StateMachine

# PWM outputs for fan control
cpuOutFanPWMPin = PWM(Pin(16))
gpuOutFanPWMPin = PWM(Pin(17))

# Set the PWM frequency to 22.73 kHz
ECPWMFreq = 22730
cpuOutFanPWMPin.freq(ECPWMFreq)
gpuOutFanPWMPin.freq(ECPWMFreq)

# Duty cycle range is 0-65535 (16-bit)
defaultSpeedDutyCycle = int(65535 * 0.3)  # 30% of 65535

cpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)
gpuOutFanPWMPin.duty_u16(defaultSpeedDutyCycle)

# Configure GP20 as input for EC PWM (CPU)
smFreq = 125_000_000
gp19CPUin = Pin(19, Pin.IN)
gp20GPUin = Pin(20, Pin.IN)

smCyclesInECCycle = smFreq / ECPWMFreq

#@asm_pio()
@rp2.asm_pio()
def pwm_reader():
    # Measure high time of PWM signal
    wrap_target()
    mov(x, invert(null))       # Initialize x to all 1s (maximum count)
    label('high_loop')
    jmp(pin, 'high_increment')  # While pin is high, keep counting
    mov(isr, x)                 # Move count to ISR
    push()                      # Send data to FIFO
    wait(0, pin, 0)             # Wait for pin to go low
    wait(1, pin, 0)             # Wait for pin to go high again
    wrap()

    label('high_increment')
    jmp(x_dec, 'high_loop')     # Decrement x (acts as counter)

# Initialize State Machine
smCPU = StateMachine(0, pwm_reader, freq=smFreq, in_base=Pin(19), jmp_pin=Pin(19))
smGPU = StateMachine(1, pwm_reader, freq=smFreq, in_base=Pin(20), jmp_pin=Pin(20))
smCPU.active(1)
smGPU.active(1)

def dutyCalc(highTime):
    dutyCycleIn = 0xFFFFFFFF - highTime
    dutyCycleOut = int((dutyCycleIn / smCyclesInECCycle) * 65535) * 2 # *2 (half cycle is used only)
    if dutyCycleOut > 65535:
        return 65535
    elif dutyCycleOut < defaultSpeedDutyCycle: #don't allow <30% RPM
        return defaultSpeedDutyCycle
    return dutyCycleOut

def saveToLog(msg):
    with open("log.log", "a") as logfile:
        logfile.write(msg)

while True:
    if (smCPU.rx_fifo()):
        highTimeCPU = smCPU.get()  # Get the count from FIFO (blocking)
        dutyCycleCPUOut = dutyCalc(highTimeCPU)
        cpuOutFanPWMPin.duty_u16(dutyCycleCPUOut)
        #print(f"High time CPU: {dutyCycleCPUOut:.12f}")
        #saveToLog(f"CPU: {dutyCycleCPUOut}\n")
    if (smGPU.rx_fifo()):
        highTimeGPU = smGPU.get()  # Get the count from FIFO (blocking)
        dutyCycleGPUOut = dutyCalc(highTimeGPU)
        gpuOutFanPWMPin.duty_u16(dutyCycleGPUOut)
        #print(f"High time GPU: {dutyCycleGPUOut:.12f}")
        #saveToLog(f"GPU: {dutyCycleGPUOut}\n")
    #print(f"{sm.rx_fifo()}")
    time.sleep(0.01)


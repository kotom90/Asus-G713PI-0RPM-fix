# Asus G713PI 0RPM fan speed fix
## Issue: 
In this particular model after shutting down and powering the laptop again, the fans don't keep the last profile loaded via armoury crate, so both CPU and GPU fans stay at 0 RPM, overheating the CPU while no OS has loaded and no fan profile exists. This issue may exist in other laptop models as well, but it's a generic solution that could be potentially used in most laptops.

The fans turn on only after entering the system diagnostics in bios and performing a fan test which passes or enabling a fan profile while the OS is loaded via the armoury crate or third party software. The fans also stay on after the test, but will go off to 0 RPM again as soon as the device shuts down and turns on again.

## Proposed solution: 
This is a hardware solution using a small microcontroller like a Raspberry Pico 2 with the RP2350 microcontroller chip which can fit inside our laptop and this is what will be used here. This is a difficult procedure because it requires expert soldering skills and possibly replacement of smd components. If you don't have the required equipment for the soldering, please don't attempt it because you will likely damage your device and possibly beyond repair.

## Process:
The idea is to use our controller as an intermediate and isolate the PWM output signals that control the fans from the embedded controller (EC) that's already installed in the laptop, and route those to the inputs of our Raspberry Pico GPIOs, reading the levels of the PWM signals the controller presents.

The fans will then be connected to the outputs of our Raspberry in PWM mode. In case the the duty cycle of the incoming signal indicates no fan rotation, or lower than a threshold we set via the **defaultSpeedDutyCycle** constant, we will instruct our raspberry to output that default minimum PWM signal instead.

The PWM signal is read using 2 state machines and run at the default 125Mhz which can precisely capture the PWM of the laptop's signals.

## Schematic diagram:
<img width="880" alt="circuit" src="https://github.com/user-attachments/assets/389f6d4e-6894-4fcc-93bf-1e49b0cc24fc" />

# Required electronics parts:
* 1x Rasperry pico (in our case raspberry pico 2, you can possibly use other versions too with slight or no modifications)  
* 1x 2.2Ω smd 0403 resistor (acting as a power fuse to protect laptop circuitry in case raspberry goes bad)
* 1x diode to prevent pico from feeding power back to your laptop through the VSYS in case it's connected through usb for programming. **(WARNING! SHOULD NOT POWER ON THE LAPTOP AND USB FOR PROGRAMMING AT THE SAME TIME!)**
* Insulated wire for powering and routing the raspberry pico.
  
The other parts are already included on the motherboard (2x 4.7ΚΩ are used as pull-up resistors for the EC PWMs and 2x 100Ω are used for current limiting to the fans.)

## How to connect?:
* Move the 2x100Ω resistors that connect the fans' PWM signals to the EC so 1 end is connected to the fan and the other end should be floating(not connected).
* Connect the 2 floating ends using wires to the outputs of our Raspberry (GP16 and GP17), effectively connecting the fans to the raspberry outputs.
* Connect the PWM signals coming from the EC after the 4.7KΩ resistors to the respective inputs (GP20 for CPU and GP21 for GPU).
* Place a 2.2Ω resistor at the VSYS input of the raspberry for short circuit protection and connect it to the 3.3VS voltage of the laptop (usually 2 coils one of them is 5V and the other one is 3.3V).

## Installing program to rapsberry
1. Download micropython for your device from [micropython](https://micropython.org/download/) and follow the instructions to install.
2. Download Thonny, connect your raspberry via usb and at the right corner select your device.
3. Now you can copy the main.py file to your root directory of your pico.
4. The program will run automatically when raspberry gets power through vsys pin.

## Images
![laptop2](https://github.com/user-attachments/assets/10ab43cd-39b1-4b6d-86f8-502fc4971833)
![laptop1](https://github.com/user-attachments/assets/ba9552c0-80b8-4fd3-8039-3fcb2006c14d)

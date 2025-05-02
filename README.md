# Asus G713PI 0RPM fan speed fix
## Issue: 
In this particular model after shutting down and powering the laptop again, the fans don't keep the last profile loaded via armoury crate, so both CPU and GPU fans stay at 0 RPM, overheating the CPU while no OS has loaded and no fan profile exists. This issue may exist in other laptop models as well, but it's a generic solution that could be potentially used in most laptops.

The fans turn on only after entering the system diagnostics in bios and performing a fan test which passes or enabling a fan profile while the OS is loaded via the armoury crate or third party software. The fans also stay on after the test, but will go off to 0 RPM again as soon as the device shuts down and turns on again.

## Proposed solution: 
This is a hardware solution using a small microcontroller like a Raspberry Pico with the RP2350 microcontroller chip which can fit inside our laptop and this is what will be used here. This is a difficult procedure because it requires expert soldering skills and possibly replacement smd components. If you don't have the required equipment for the soldering, please don't attempt it because you will likely damage your device and possibly beyond repair.

## Process:
The idea is to use our controller as an intermediate and isolate the PWM output signals that control the fans from the embedded controller (EC) that's already installed in the laptop, and route those to the inputs of our Raspberry Pico GPIOs, reading if there is any signal present. The fans will then be connected to the outputs of our Raspberry. In case the signal is none (0 RPM) or LOW state for at least some time, we will define a default PWM signal to the fans to counter the issue. When the inputs receive a signal from the laptop EC, the default output will translate that level so it's possible to control the fans with a profile from the OS as usual. Because the PWM signals are easier to read when they are converted to DC analog levels, we will use a low pass filter of 10k resistor and 100nF capacitor for each PWM signal and feed them to the ADC analog inputs of the raspberry. This might be not very accurate but it will do the job.

## Schematic diagram:
![circuit](https://github.com/user-attachments/assets/0f1291fa-37b1-4184-b942-5a31ad9e9605)

# Required electronics parts:
* 1x Rasperry pico (in our case raspberry pico 2, you can possibly use other versions too with slight or no modifications)  
* 1x 2.2Ω smd 0403 resistor (acting as a power fuse to protect laptop circuitry in case raspberry goes bad)
* 1x diode to prevent pico from feeding power back to your laptop through the VSYS in case it's connected through usb for programming.
* 2x 10kΩ and 2x 100nF smd 0403 resistors and capacitors (for low pass filter of the PWM signal to convert to analog DC)  
* Insulated wire for powering and routing the raspberry pico.  
  
The other parts are already included on the motherboard (2x 4.7ΚΩ are used as pull-up resistors for the EC PWMs and 2x 100Ω are used for current limiting to the fan.)  

## How to connect?:
* Move the 2x100Ω resistors that connect the fans' PWM signals to the EC so 1 end is connected to the fan and the other end should be floating(not connected).  
* Connect the 2 floating ends to the outputs of our Raspberry (GP16 and GP17), effectively connecting the fans to the raspberry outputs. 
* Connect the DC outputs between the 10K resistor and the 100nF capacitor to each respective ADC input of the raspberry (GP26 for CPU and GP27 for GPU).
* Place a 2.2Ω resistor at the VSYS input of the raspberry for short circuit protection and connect it to the 3.3VS voltage of the laptop (usually 2 coils one of them is 5V and the other one is 3.3V).

## Installing program to rapsberry
1. Download micropython for your device from [micropython](https://micropython.org/download/) and follow the instructions to install.
2. Download Thonny, connect your raspberry via usb and at the right corner select your device.
3. Now you can copy the main.py file to your root directory of your pico.
4. The program will run automatically when raspberry gets power through vsys pin.

## Images
![laptop2](https://github.com/user-attachments/assets/10ab43cd-39b1-4b6d-86f8-502fc4971833)
![laptop1](https://github.com/user-attachments/assets/ba9552c0-80b8-4fd3-8039-3fcb2006c14d)

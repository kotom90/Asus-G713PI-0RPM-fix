# Asus G713PI 0RPM fix
## Issue: 
In this particular model after shutting down and powering the laptop again, the fans don't keep the last profile loaded via armoury crate, so both CPU and GPU fans stay at 0 RPM, overheating the CPU while no OS has loaded and no fan profile exists. This issue may exist in other laptop models as well, but it's a generic solution that could be potentially used in most laptops.

The fans turn on only after entering the system diagnostics in bios and performing a fan test which passes or enabling a fan profile while the OS is loaded via the armoury crate or third party software. The fans also stay on after the test, but will go off to 0 RPM again as soon as the device shuts down and turns on again.

## Proposed solution: 
This is a hardware solution using a small microcontroller like a Raspberry Pico with the RP2350 microcontroller chip which can fit inside our laptop and this is what will be used here.

## Process:
The idea is to use our controller as an intermediate and isolate the PWM output signals that control the fans from the embedded controller (EC) that's already installed in the laptop, and route those to the inputs of our Raspberry Pico GPIOs, reading if there is any signal present. The fans will then be connected to the outputs of our Raspberry. In case the signal is none (0 RPM) or HIGH state for at least some time, we will define a default PWM signal to the fans to counter the issue. When the inputs receive a signal from the laptop EC, the default output will be routed to the outputs of Raspberry so it's possible to control the fans with a profile from the OS as usual.

## Schematic diagram:
![circuit](https://github.com/user-attachments/assets/9579ecbf-b43d-47ce-95f6-a60cbf5368fe)

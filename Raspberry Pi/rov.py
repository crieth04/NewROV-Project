import os
import pygame
import pigpio
import asyncio
from time import sleep
import RPi.GPIO as GPIO


# Set up GPIO pins
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

# Initialize Pygame
pygame.init()
pygame.joystick.init()

# Find the Logitech controller
controller = None
for i in range(pygame.joystick.get_count()):
    if "Logitech" in pygame.joystick.Joystick(i).get_name():
        controller = pygame.joystick.Joystick(i)
        controller.init()
        break

# Define motor control functions
def forward():
    GPIO.output(23, GPIO.HIGH)
    GPIO.output(24, GPIO.LOW)
    GPIO.output(18, GPIO.HIGH)
    print("Moving forward")

def backward():
    GPIO.output(23, GPIO.LOW)
    GPIO.output(24, GPIO.HIGH)
    GPIO.output(18, GPIO.HIGH)
    print("Moving backward")

def stop():
    GPIO.output(18, GPIO.LOW)
    print("Stopping")

# Initialize Pygame and setup the joystick
pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Joystick {joystick.get_name()} has been initialized.")

# Define the GPIO pin connected to your devices
ESC_GPIO = 27
SERVO_GPIO = 12

# To map joystick input to pulsewidth
def map_joystick_to_pulsewidth(value):
    pulsewidth = ((value + 1) / 2) * (1900 - 1100) + 1100
    return int(pulsewidth)

# Function to map joystick values to servo angle
# Function to map joystick values to servo pulse width
def map_angle(value):
    # limiting the input value to the range -1 to 1
    value = max(min(value, 0.75), -0.75)
    # mapping joystick value to pulse width range
    mapped_value = ((value + 1) / 2) * (2500 - 500) + 500
    # shift to the right by 3 degrees
    mapped_value += 55
    return int(mapped_value)

    
async def ensure_pigpiod_running():
    if os.system('pgrep pigpiod') != 0:
        print('pigpiod is not running, starting it now...')
        os.system('sudo pigpiod')

async def start_motor(pi):
    pi.set_servo_pulsewidth(ESC_GPIO, 1500)
    await asyncio.sleep(3)  # Let ESC initialize

async def stop_motor(pi):
    pi.set_servo_pulsewidth(ESC_GPIO, 0)

async def main():
    await ensure_pigpiod_running()

    # Create pigpio object
    pi = pigpio.pi()
    armed = True  # Motor state (False: Disarmed, True: Armed)

    while True:
        pygame.event.pump()  # Process event queue

        # Check if button 0 (usually the X button) is pressed
        if joystick.get_button(0):
            armed = not armed  # Toggle motor state
            await asyncio.sleep(0.2)

            # Only start the motor if armed, stop otherwise
            if armed:
                await start_motor(pi)  # start motor
            else:
                await stop_motor(pi)  # stop motor

        if armed:
            y_axis = joystick.get_axis(1)  # Y-axis controls throttle
            pulsewidth = map_joystick_to_pulsewidth(y_axis)
            temp= pulsewidth-1500
            go=1500-temp
            pi.set_servo_pulsewidth(ESC_GPIO, go)  # Control motor
            print(pulsewidth)
            # Get joystick axes values for the servo
            x_axis = joystick.get_axis(0)
            angle = map_angle(x_axis)
            pi.set_servo_pulsewidth(SERVO_GPIO, map_angle(x_axis)) # Control servo

        for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis == 3:  # Change the axis value to the appropriate one for the right joystick
                    # Y-axis controls motor direction
                    if event.value > 0:
                        forward()
                    elif event.value < 0:
                        backward()
                    else:
                        stop()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    # Start button stops the motor
                    stop()

        await asyncio.sleep(0.01)  # Non-blocking delay, allows CPU to process other tasks

# Ensure entire script is asynchronous
asyncio.run(main())

# ROV (Remotely Operated Vehicle) with Single Thruster, Servo, Rudder, DC Motor, Ballast Tank, and Raspberry Pi

![ROV](rov_image.jpg) <!-- Replace with an actual image of your ROV -->

This project focuses on building a Remotely Operated Vehicle (ROV) using various components like a single thruster, a servo, a rudder, a DC motor, a ballast tank, and a Raspberry Pi. The ROV can be controlled remotely using a Logitech joystick and provides functionalities for forward and backward movement, servo control, motor arming/disarming, and more.

## Hardware Components
- 1 Thruster
- 1 Servo
- 1 Rudder
- 1 DC Motor
- 1 Ballast Tank
- Raspberry Pi
- Logitech Joystick
- GPIO Cables
- Power Supply

## Software
The project involves writing Python code to control the ROV. The code uses libraries such as `pygame` for joystick input and `pigpio` for controlling GPIO pins on the Raspberry Pi.

## Installation and Setup
1. Connect the hardware components to the Raspberry Pi following the wiring diagram.
2. Install required libraries using pip: `pip install pygame pigpio`.
3. Upload the provided code (`rov_control.py`) to your Raspberry Pi.

## Wiring Diagram
![Wiring Diagram](wiring_diagram.jpg) <!-- Replace with an actual wiring diagram -->

## Code Explanation
The provided Python code (`rov_control.py`) does the following:

- Initializes GPIO pins and sets up joystick input.
- Maps joystick values to appropriate pulse widths for motor and servo control.
- Controls the motor's throttle and direction based on joystick input.
- Controls the servo's angle based on joystick input.
- Arming and disarming the motor using button input from the joystick.

## Usage
1. Connect the ROV to the power source.
2. Run the `rov_control.py` script on the Raspberry Pi.
3. Use the Logitech joystick to control the ROV's movement and servo.

## Note
Make sure to adjust GPIO pin numbers, joystick axis/button indices, and calibration values in the code to match your specific hardware setup.

## Contributions
Contributions to this project are welcome! Feel free to fork this repository, make improvements, and create pull requests.

## Acknowledgments
Special thanks to the open-source community, libraries like `pygame` and `pigpio`, and contributors who make projects like this possible.

## License
This project is licensed under the [MIT License](LICENSE).

---

Feel free to modify the above README template to fit your project's specifics. Add more sections if needed, such as a Troubleshooting section, additional images, or a Getting Started guide. Make sure to replace placeholders with actual content, images, and filenames.

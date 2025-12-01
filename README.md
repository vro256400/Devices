## Hardware
The code should work on any device that supports MicroPython, has a WiFi module and input/output pins. Tested on board Raspberry Pi Pico W.

## Prepare Debian 13 host

    sudo apt install python3 python3-pip python3.13-venv
    cd ~
    python3 -m venv venv_ampy
    source venv_ampy/bin/activate
    pip install adafruit-ampy

## Upload MicroPython to the Raspberry Pi Pico W
It is instructions for Raspberry Pi Pico W. For others use boards manuals.
Connect board using USB cable. On Debian or Windows will appear new USB device. Please, copy file <cloned repository>/Boards/PiPicoW/RPI_PICO_W-20250415-v1.25.0.uf2 to this disk. The disk will disappear after copy - it is ok.

For Windows will appear new COM port, for Debian will appear new device(something like /dev/ttyAxxx).
## Upload code to board

    source ~/venv_ampy/bin/activate
    cd <cloned repository>
    cd common
    
TODO:


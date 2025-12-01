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

For Windows will appear new COM port(something like COM3), for Debian will appear new device(something like /dev/ttyACM0).
If device/port is not added then board already runs script and you should exit. To exit script in this repository you can use following commands:

### Device connected to the network:
    cd <cloned repository>/Tools
    python3 exitDevScript.py <device ip>

### Device is not connected:
Use board manual. For Raspberry Pi Pico W press 'Reset' button and connect to PC's USB - USB disk will appear. You can copy <cloned repository>/Boards/PiPicoW/flash_nuke.uf2 to it and device will erase internal flash disk.

## Upload code to board

    source ~/venv_ampy/bin/activate
    cd <cloned repository>
    cd common

### for Windows

    upload.bat COM3
    
### for Debian

    upload.sh /dev/ttyACM0

## Devices types
### Switcher
It is for power management. Currently repository provides this type only. The device uses schedule to power on/off devices. The picture below gives look how it appears in GUI:

<p align="center">
  <img src="https://raw.githubusercontent.com/vro256400/homeautweb/main/readme/page.jpg" alt="Page with two devices"/>
</p>

The steps to make this device is simple:
#### Determine which electricity consumers in your home you want to control and determine pins for these devices.
Here is detail explanation about Raspbarry Pi Pico pins
https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html

In my home I use one board to control water pump and boiler and selected pins GP18 and GP19 on the board.  Using this controller we receive significantly lower electricity bills.

You can use a solid-state or mechanical relay. The choice depends on the device—you need to consider the power rating and ensure the relay is controlled at the 3.3-volt level for Pi Pico controllers.


#### You need create 3 files
2 is required to run board and one to manage it from browser(optional).

##### File config.txt

    wifi_name : <your wifi>
    wifi_pwd  : <your password>
    pw_ip : 192.168.1.2
    pw_login : boynas
    pw_passwd : passwd

    # switch 0
    sw_name0 : boyler
    sw_pin0 : 19
    sw_pin_default0 : 0

    # switch 1
    sw_name1 : nasos
    sw_pin1 : 18
    sw_pin_default1 : 0

This file is not changeable from web browser and uploads if you changes your hardware or WiFi.
pw_passwd - is any (it doesn’t use in this version)
pw_ip – PW server require when you want to manage device from browser. It is home server and device has functionality to discovery server in local network, but it is better to specify to avoid possibility hackers attack. If you plans but haven’t then reserve IP and specify this parameter.

Other parameters are clear. It declare several pins.

##### File settings.txt

It is changeable in web browser and it is schedule for pins declared in config.txt.

    tz_hours : 3
    boyler_mode : schedule
    boyler_on : False
    boyler_startH : [4, 17, 20]
    boyler_startM : [0, 0,  0]
    boyler_stopH : [6, 18, 22]
    boyler_stopM : [0, 0, 0]
    nasos_mode : schedule
    nasos_on : False
    nasos_startH : [7]
    nasos_startM : [0]
    nasos_stopH : [23]
    nasos_stopM : [59] 

tz_hours PW server changes automatically.
xxx_mode can be ‘schedule’ and ‘manual’. The second use xxx_on to switch on/off pin.
In the example ‘boyler’ works 4:00 – 6:00, 17:00 – 18:00, 20:00 – 22:00.

##### File schema.txt (optional if you use PW server)
This file is not for device flash – it is to configure PW.  In my case this file is:

    tz_hours : write_to_device : required : int : range -12 12
    boyler_mode : write_to_device : required : combo string : schedule,manual
    boyler_on : write_to_device : required : bool
    boyler_startH : write_to_device : required : array int : range 0 23
    boyler_startM : write_to_device : required : array int : range 0 59
    boyler_stopH : write_to_device : required : array int : range 0 23
    boyler_stopM : write_to_device : required : array int : range 0 59
    nasos_mode : write_to_device : required : combo string : schedule,manual
    nasos_on : write_to_device : required : bool
    nasos_startH : write_to_device : required : array int : range 0 23
    nasos_startM : write_to_device : required : array int : range 0 59
    nasos_stopH : write_to_device : required : array int : range 0 23
    nasos_stopM : write_to_device : required : array int : range 0 59

    validate len(boyler_startH)==len(boyler_startM)==len(boyler_stopH)==len(boyler_stopM)
    validate len(nasos_startH)==len(nasos_startM)==len(nasos_stopH)==len(nasos_stopM)
    



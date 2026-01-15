## Board 
<p align="center">
  <img src="https://raw.githubusercontent.com/vro256400/Devices/main/Boards/ESP8266_ESP_01/board.jpg" alt="Board picture"/>
</p>

## USB adapter
<p align="center">
  <img src="https://raw.githubusercontent.com/vro256400/Devices/main/Boards/ESP8266_ESP_01/usb_adapter.jpg" alt="usb adapter"/>
</p>

**This model of USB adapter doesn't work with ESP-01 without resistor 1K between VCC and CH_PD. So,solder it!!!**

## USB adapter and board connected
<p align="center">
  <img src="https://raw.githubusercontent.com/vro256400/Devices/main/Boards/ESP8266_ESP_01/IMG_0026.JPG" alt="usb adapter and board connected"/>
</p>


## Prepare Debian 13 host 
Use README.md in root folder to prepare your PC.
Additionally esptool should be installed:

    source ~/venv_ampy/bin/activate
    pip install esptool

The commands below suppose you activated Python environment(first command above).

## It is required command for ESP-01 to format flash for new boards

Set switcher(look to the picture of USB adapter) to program mode and execute command:

    esptool --port /dev/ttyUSB0 erase-flash

## Upload MicroPython for 1Mb flash

Switcher is still in program mode. Execute command:

    esptool --port /dev/ttyUSB0 --baud 460800 write_flash --flash-size=detect 0 ~/Devices/Boards/ESP8266_ESP-01/ESP8266_GENERIC-FLASH_1M-20251209-v1.27.0.bin

Set switcher to UART mode. MicroPython is installed and board is ready.

## connect using serial port to Python prompt to test
    tio -b 115200 /dev/ttyUSB0
    


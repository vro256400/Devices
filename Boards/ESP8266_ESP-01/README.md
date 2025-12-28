Модуль USB-перехідника для програмування і налагодження Wi-Fi модулів ESP-01 і ESP-01S на базі мікросхеми CH340G. Плата містить всю необхідну обв'язку для коректної роботи програмованих модулів. Для вибору режиму роботи (програмування / налагодження) на платі встановлений перемикач режиму роботи. Що б прошити всі варіанти плат ESP-01 - необхідно припаяти резистор 1-10 кОм між VCC і CH_PD.

## Prepare Debian 13 host 

    source ~/venv_ampy/bin/activate
    pip install esptool

## It is required command for ESP-01 to format flash for new boards

Set switcher to program mode and execute command

    esptool --port /dev/ttyUSB0 erase-flash

## Upload MicroPython for 1Mb flash

Set switcher to program mode and execute command

    esptool --port /dev/ttyUSB0 --baud 460800 write_flash --flash-size=detect 0 ~/Devices/Boards/ESP8266_ESP-01/ESP8266_GENERIC-FLASH_1M-20251209-v1.27.0.bin

Set switcher to serial port. MicroPython is installed and board is ready.

## connect using serial port to Python prompt to test
    tio -b 115200 /dev/ttyUSB0
    


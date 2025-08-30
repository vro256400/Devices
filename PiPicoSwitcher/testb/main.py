import machine
import utime

# Define the onboard LED pin
led_pin = machine.Pin("LED", machine.Pin.OUT)

# Define the frequency of blinking (in milliseconds)
blink_frequency_ms = 500

while True:
    print("Serial port message")
    # Turn on the LED
    led_pin.value(1)
    # Wait for the specified time
    utime.sleep_ms(blink_frequency_ms)
    # Turn off the LED
    led_pin.value(0)
    # Wait for the specified time
    utime.sleep_ms(blink_frequency_ms)
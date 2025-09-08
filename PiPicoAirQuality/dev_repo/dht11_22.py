from machine import Pin
from time import sleep
import dht 

class dht22():
    PinName = "DefaultName"
    PinNumber = 22 # default pin
    sensor = None
    ht = None
    def setupHardware(self):               
        self.sensor = dht.DHT22(Pin(self.PinNumber))

    def getTemperatureAndHumidity(self) :
        ret = None
        try:
            self.sensor.measure()
            ret = [0.0, 0.0]
            ret[0] = self.sensor.temperature()
            ret[1] = self.sensor.humidity()
            print('Temperature: %3.1f C' %ret[0])
            print('Humidity: %3.1f %%' %ret[1])
        except OSError as e:
            print('Failed to read sensor.')
            ret = None
        return ret
    
    def run(self) :
        ht = self.getTemperatureAndHumidity()

class dht11(dht22):
    def setupHardware(self):               
        self.sensor = dht.DHT11(Pin(self.PinNumber))


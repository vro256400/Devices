from machine import Pin
from time import sleep
import dht 
import time

class dht22():
    PinName = "DefaultName"
    PinNumber = 22 # default pin
    sensor = None
    ht = None
    measure_time = 0

    def setupHardware(self):               
        self.sensor = dht.DHT22(Pin(self.PinNumber))

    def getTemperatureAndHumidity(self) :
        if self.ht == None:
            self.run()
        return self.ht
    
    def measureTemperatureAndHumidity(self) :
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
        cur_time = time.time()
        if self.ht != None and cur_time - self.measure_time < 30: 
            return
        self.ht = self.measureTemperatureAndHumidity()
        self.measure_time = cur_time

class dht11(dht22):
    def setupHardware(self):               
        self.sensor = dht.DHT11(Pin(self.PinNumber))


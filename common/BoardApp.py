import time
import machine
import outpinwithindayplan
import router
import ntptimestore
import pycodeupdater
import pwio
import devconfig
from dht11_22 import *
from WatchDog import wdt

switcherLED = machine.Pin("LED", machine.Pin.OUT)
switcherLED.value(1)
time.sleep(1)
switcherLED.value(0)
time.sleep(1)

wdt.feed()

class PwProt(pwio.Pwio):
    settingsUpdated = False
    
    def onGetSettings(self):
        print("PwProt.onGetSettings")
        settings = devconfig.DevConfig("settings.txt", False)
        fc = settings.file_content
        print(fc)
        return fc
        
    def onNewSettings(self, content):
        print("PwProt.onNewSettings ", content)
        with open("settings.txt", "wb") as f:
            f.write(content)
            f.close()
        self.settingsUpdated = True

class BoardApp(PwProt) :
    config = None 
    pw = None  
    ntw = None
    ntp = None
    upd = None
    switchers = None
    config = None
    dht22 = None # dht11 also - it derives from dht22

    def onGetInputsVar(self):
        cnf = ""
        for dht in self.dht22 :
            vals = dht.getTemperatureAndHumidity()
            if vals == None or len(vals) != 2:
                continue
            cnf = cnf + "[" + str(vals[0]) + ", " + str(vals[1]) + "]\n"
    
        return cnf

    def createHdwDevices(self) :
        switchers_count = self.count_dev("sw")   
        self.pw.logInfo("Switchers ", switchers_count)
        self.switchers = [outpinwithindayplan.OutPinWithInDayPlan(self.pw) for i in range(switchers_count)]
        for index in range(len(self.switchers)):
            sw = self.switchers[index]
            sw.PinName = self.config.value["sw_name" + str(index)]
            sw.PinNumber = int(self.config.value["sw_pin" + str(index)])
            sw.PinDefault = int(self.config.value["sw_pin_default" + str(index)])
        self.pw.logInfo('Setup switchers hardware...')
        for sw in self.switchers :
            print(sw.PinName)
            sw.setupHardware()

        switchers_count = self.count_dev("dht22")
        self.pw.logInfo("Temp/Hum(dht22) ", switchers_count)
        self.dht22 = [dht22(self.pw) for i in range(switchers_count)]
        for index in range(len(self.dht22)):
            dht = self.dht22[index]
            dht.PinName = self.config.value["dht22_name" + str(index)]
            dht.PinNumber = int(self.config.value["dht22_pin" + str(index)])

        self.pw.logInfo('Setup dht22 hardware...')
        for dht in self.dht22 :
            print(dht.PinName)
            dht.setupHardware()


    def updateSettings(self):
        global switcherLED
        settings = devconfig.DevConfig("settings.txt")
        
        for index in range(len(self.switchers)):
            sw = self.switchers[index]
            v = settings.value.get(sw.PinName + "_startH")
            if (v != None) :
                sw.setStartH(v)
            v = settings.value.get(sw.PinName + "_startM")
            if (v != None) :
                sw.setStartM(v)
            v = settings.value.get(sw.PinName + "_stopH")
            if (v != None) :
                sw.setStopH(v)
            v = settings.value.get(sw.PinName + "_stopM")
            if (v != None) :
                sw.setStopM(v)
            v = settings.value.get(sw.PinName + "_mode")
            if (v!= None) :
                sw.setModeFromString(v)
            v = settings.value.get(sw.PinName + "_on")
            if (v!= None) :
                sw.setManualOn(v)

            print(sw.PinName, "mode :", sw.getModeString())
            print(sw.PinName, "on(for manual mode) :", sw.switchOn)
            print(sw.PinName, "startH :", sw.startH)
            print(sw.PinName, "startM :", sw.startM)
            print(sw.PinName, "stopH :", sw.stopH)
            print(sw.PinName, "stopM :", sw.stopM)    

        self.ntp.tz = int(settings.value["tz_hours"])

        switcherLED.value(1)

    def count_dev(self, dev_prefix) : 
        devCount = 0
        while (True):
            key = dev_prefix + "_name" + str(devCount)
            if not key in self.config.value.keys():
                break
            devCount = devCount + 1
        return devCount

    def __init__(self) :
        global wdt
        wdt.feed()

        self.config = devconfig.DevConfig("config.txt")

        self.pw = PwProt()
        self.pw.ip = self.config.value["pw_ip"] # port 7777
        self.pw.login = self.config.value["pw_login"]
        self.pw.passwd = self.config.value["pw_passwd"]
        self.pw.deviceType = self.config.value["pw_type"]

        self.pw.logInfo("Starting...")

        self.ntw = router.Router()
        self.ntw.networkName = self.config.value["wifi_name"]
        self.ntw.networkPass = self.config.value["wifi_pwd"]
        self.ntw.setupHardware()

        self.ntp = ntptimestore.NtpTimeStore(self.pw)
        self.ntp.serverDomain = self.config.value["pw_ip"] # port 123
        
        self.upd = pycodeupdater.PyCodeUpdater()

        self.createHdwDevices()
        self.updateSettings()
         
    def step(self) :
        return
    
    def run(self) :
        global wdt
        while True:    
            wdt.feed()
            self.ntw.run()
            if not self.ntw.isRouterConnected():
                wdt.sleep(10)
                
                for sw in self.switchers :
                    sw.switch(sw.PinDefault)
                continue
            
            if (not self.ntp.run()) :
                for sw in self.switchers :
                    sw.switch(sw.PinDefault)
                continue
            
            self.pw.run()
                
            if (self.pw.settingsUpdated) :
                self.pw.settingsUpdated = False
                self.updateSettings()

            for sw in self.switchers :
                sw.run(self.ntp.curH, self.ntp.curM)   

        
            self.upd.run()

            self.step()
            
            time.sleep(1)
        return
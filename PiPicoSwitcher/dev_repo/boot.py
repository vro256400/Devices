import time
import machine
switcherLED = machine.Pin("LED", machine.Pin.OUT)
switcherLED.value(1)
time.sleep(1)
switcherLED.value(0)
time.sleep(1)
import outpinwithindayplan
import router
import ntptimestore
import pycodeupdater
import pwio
import devconfig

class Kotel(outpinwithindayplan.OutPinWithInDayPlan):
    def __init__(self):
        global pw
        super().__init__(pw)
        
    def onSwitcherChange(self, current):
        global switcherLED, pw
        if (current) :
            switcherLED.value(1)
            pw.logInfo(self.PinName + " on")
        else :
            switcherLED.value(0)
            pw.logInfo(self.PinName + " off")
            
        return

class PwProt(pwio.Pwio):
    settingsUpdated = False
    
    def onGetSettings(self):
        print("onGetSettings")
        settings = devconfig.DevConfig("settings.txt", False)
        print(settings.file_content)
        return settings.file_content
    
    def onNewSettings(self, content):
        print("onNewSettings ", content)
        with open("settings.txt", "wb") as f:
            f.write(content)
            f.close()
        self.settingsUpdated = True

def updateSettings():
    global settings, switchers, switchers_count, config, switcherLED, ntp
    settings = devconfig.DevConfig("settings.txt")
    switchers = [Kotel() for i in range(switchers_count)]
    for index in range(len(switchers)):
        sw = switchers[index]
        sw.PinName = config.value["sw_name" + str(index)]
        sw.PinNumber = int(config.value["sw_pin" + str(index)])
        sw.PinDefault = int(config.value["sw_pin_default" + str(index)])
        v = settings.value.get(sw.PinName + "_startH")
        print(v)
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
        print(sw.PinName, "switchon(manual mode) :", sw.switchOn)
        print(sw.PinName, "startH :", sw.startH)
        print(sw.PinName, "startM :", sw.startM)
        print(sw.PinName, "stopH :", sw.stopH)
        print(sw.PinName, "stopM :", sw.stopM)    

    pw.logInfo('Setup switchers hardware...')
    for sw in switchers :
        print(sw.PinName)
        sw.setupHardware()
    switcherLED.value(1)

    ntp.tz = int(settings.value["tz_hours"])

config = devconfig.DevConfig("config.txt")

pw = PwProt()
pw.ip = config.value["pw_ip"] # port 7777
pw.login = config.value["pw_login"]
pw.passwd = config.value["pw_passwd"]
pw.deviceType = "switcher"

pw.logInfo("Starting...")

ntw = router.Router()
ntw.networkName = config.value["wifi_name"]
ntw.networkPass = config.value["wifi_pwd"]
ntw.setupHardware()

switchers_count = 0
while (True):
    key = "sw_name" + str(switchers_count)
    if not key in config.value.keys():
        break;
    switchers_count = switchers_count + 1
    
pw.logInfo("Switchers ", switchers_count)

ntp = ntptimestore.NtpTimeStore(pw)
ntp.serverDomain = config.value["pw_ip"] # port 123
upd = pycodeupdater.PyCodeUpdater()

updateSettings()

while True:    
    ntw.run()
    if not ntw.isRouterConnected():
        time.sleep(10)
        for sw in switchers :
            sw.switch(sw.PinDefault)
        continue
    
    if (not ntp.run()) :
        for sw in switchers :
            sw.switch(sw.PinDefault)
        continue

    pw.run()
        
    if (pw.settingsUpdated) :
        pw.settingsUpdated = False
        updateSettings()

    for sw in switchers :
        sw.run(ntp.curH, ntp.curM)
    
    print("upd start")
    upd.run()
    print("upd stop")
    
    time.sleep(1)


import machine

class OutPinWithInDayPlan():
    __pw = None
    PinName = "DefaultName"
    PinNumber = 18
    PinDefault = 1
    class Mode:
        Manual = 1
        Schedule = 2

    mode = Mode.Schedule

    # Manual mode data
    switchOn = False
    
    # Schedule mode data
    startH = [21, 0]
    startM = [0,  0]
    stopH = [23,  2]
    stopM = [59,  0]

    switcher = None
    logfirstTime = True 
    
    def __init__(self, pw):
        self.__pw = pw
        
    def setStartH(self, s):
        self.startH = eval(s)
        
    def setStartM(self, s):
        self.startM = eval(s)    
    
    def setStopH(self, s):
        self.stopH = eval(s)
    
    def setStopM(self, s):
        self.stopM = eval(s)
        
    def setModeFromString(self, s):
        if (s.lower() == "schedule") :
            self.mode = self.Mode.Schedule
        else :
            self.mode = self.Mode.Manual

    def getModeString(self) :
        if (self.mode == self.Mode.Schedule) :
            return "schedule"
        return "manual"

    def setManualOn(self, s) :
        self.switchOn = eval(s)

    def setupHardware(self):
        self.switcher = machine.Pin(self.PinNumber, machine.Pin.OUT) # GP18
        self.switcher.value(self.PinDefault)
        if (len(self.startH) != len(self.startM)) or (len(self.startH) != len(self.stopH)) or (len(self.stopH) != len(self.stopM)):
            self.__pw.logError("Incorrect settings in OutPinWithInDayPlan")
    
    def switch(self, val):
        changed = (self.logfirstTime or (self.switcher.value() != val));
        self.logfirstTime = False
        self.switcher.value(val)
        if (changed):
            self.onSwitcherChange(val)
    
    def isTimeToRun(self, curH, curM) -> bool:
        if (self.mode == self.Mode.Manual) :
            return self.isTimeToRunManual(curH, curM)
        
        return self.isTimeToRunSchedule(curH, curM)
    
    def isTimeToRunManual(self, curH, curM) -> bool:
        return self.switchOn
    
    def isTimeToRunSchedule(self, curH, curM) -> bool:
        cur = curH * 256 + curM
        
        for i in range(len(self.startH)):
            start = self.startH[i] * 256 + self.startM[i]
            stop = self.stopH[i] * 256 + self.stopM[i]
            
            if cur >= start and cur <= stop :
                return True
        
        return False
        
    def onSwitcherChange(self, current):
        return
            
    def run(self, curH, curM):
        if (self.isTimeToRun(curH, curM)) :
            self.switch(1)
        else :
            self.switch(0)
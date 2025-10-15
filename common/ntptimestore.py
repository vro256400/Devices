import ntptime
import time
import pwio
import utime
from srv_discovery import getPwServer

# the times in UTC, London - no summer or winter in UTC
class NtpTimeStore():
    __pw = None
    curH = 0
    curM = 0
    tz = 0
    serverDomain = None
    # port is 123
    
    ntpTimeLoadedAt0 = False
   
    def __init__(self, pw):
        self.__pw = pw
        
    def setNtpTime(self) -> bool:
        serverDomain = None
        if (self.serverDomain == None) :
            self.__pw.logInfo("Server discovery")
            getPwServer()
            serverDomain = getPwServer()
        else:
            serverDomain = self.serverDomain
            
        if (serverDomain == None):
            self.__pw.logInfo("Can't detect server")    
        else:
            ntptime.host = serverDomain
            self.__pw.logInfo("Loading time from ", ntptime.host)
            try:
                ntptime.settime()
                return True
            except:
                self.__pw.logInfo("Can't get time from ", ntptime.host)

        ntptime.host = "pool.ntp.org"
        self.__pw.logInfo("Loading time from ", ntptime.host)
        try:
            ntptime.settime()
        except:
            return False
        return True
    
    def getCurTime(self) :
        a = time.time() + self.tz*60*60
        t = time.localtime(a)
        timeChanged = ((self.curH != t[3]) or (self.curM != t[4]))
        self.curH = t[3]
        self.curM = t[4]
        if (timeChanged) :
            self.__pw.logInfo('Current Time:', self.curH, ":", self.curM)
        
    def run(self) -> bool:
        if (not self.ntpTimeLoadedAt0 and self.curH == 0 and self.curM == 0) :
            if (not self.setNtpTime()):
                self.__pw.logInfo("Can't load NTP time")
                return False
            self.__pw.logInfo("Set Time from NTP(UTC): ", time.localtime())
            self.ntpTimeLoadedAt0 = True
        if (self.curH != 0 or self.curM != 0) :
            self.ntpTimeLoadedAt0 = False
        
        self.getCurTime()
        
        return True
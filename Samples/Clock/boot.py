import BoardApp
import mclock
import time

class ClockApp(BoardApp.BoardApp):

    # it is info for web application
    def completeInputsVar(self, cnf):
        cnf = cnf + "ntp_domain : " + self.ntp.lastLoadedDomain + "\n"
        cnf = cnf + "timezone : " + self.ntp.tz + "\n"
        a = time.time() + self.ntp.tz*60*60
        t = time.localtime(a)
        cnf = cnf + "timeH : " + t[3] + "\n"
        cnf = cnf + "timeM : " + t[4] + "\n"
        
        return

theApp = ClockApp()
cl = mclock.mclock()
cl.start(theApp.ntp.tz)
theApp.run()

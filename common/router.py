import network
import time
from WatchDog import wdt

class Router():
    networkName = 'NoAccess'
    networkPass = ''
    connectToRouter = None
    
    def setupHardware(self):
        print("Setup WIFI hardware")
        self.connectToRouter = network.WLAN(network.STA_IF)
        self.isRouterConnected()
        
    def doConnectToRouter(self) -> bool:
        self.connectToRouter = network.WLAN(network.STA_IF)
        self.connectToRouter.active(True)
        self.connectToRouter.connect(self.networkName, self.networkPass)
        for x in range(10):
            if self.connectToRouter.isconnected():
                return True
            time.sleep(1)
            wdt.feed()
            
        return False    

    def isRouterConnected(self) -> bool:
        return self.connectToRouter.isconnected()
        
    def run(self):
        if not self.isRouterConnected():
            print("Connect to router")
            if self.doConnectToRouter():
                print('Connected to router')
                self.onRouterConnected(True)
                return
            else:
                print('Can not connect to router')
                self.onRouterConnected(False)
                return
                
    def onRouterConnected(self, connected):
        return


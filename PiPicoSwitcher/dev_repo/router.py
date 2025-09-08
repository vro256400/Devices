import network
import time

class Router():
    networkName = 'NoAccess'
    networkPass = ''
    connectToRouter = None
    
    def setupHardware(self):
        #global connectToRouter
        print("Setup WIFI hardware")
        self.connectToRouter = network.WLAN(network.STA_IF)
        self.isRouterConnected()
        
    def doConnectToRouter(self) -> bool:
        #global connectToRouter
        self.connectToRouter = network.WLAN(network.STA_IF)
        self.connectToRouter.active(True)
        self.connectToRouter.connect(self.networkName, self.networkPass)
        for x in range(2):
            if self.connectToRouter.isconnected():
                return True
            time.sleep(1)
        return False    

    def isRouterConnected(self) -> bool:
        #global connectToRouter
        return self.connectToRouter.isconnected()
        
    def run(self):
        if not self.isRouterConnected():
            print("Connect to router")
            if self.doConnectToRouter():
                self.onRouterConnected(True)
                return
            else:
                print('Can not connect to router')
                self.onRouterConnected(False)
                return
                
    def onRouterConnected(self, connected):
        return


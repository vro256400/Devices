from machine import WDT
import time

class WatchDog:
    enable = True
    wdt = None
    def __init__(self) :
        if self.enable:
            self.wdt = WDT(timeout=8300)
            self.wdt.feed()

    def feed(self):
        if self.enable:
            self.wdt.feed()

    def sleep(self, sec):
        if self.enable:
            for i in range(sec):
                self.wdt.feed()
                time.sleep(1)
        else:
            time.sleep(sec)

#if 'wdt' not in globals():
#    wdt = WatchDog()

try:
    wdt.feed()
except NameError:
    wdt = WatchDog()
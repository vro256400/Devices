import time

class WatchDog:
    enable = True
    wdt = None
    def __init__(self) :
        return

    def feed(self):
        return

    def sleep(self, sec):
        time.sleep(sec)

try:
    wdt.feed()
except NameError:
    wdt = WatchDog()
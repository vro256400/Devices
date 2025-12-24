import _thread
import time
import machine

digit_vals = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
tz = 2
def flashDigit(DIG, digit):
    global P_A, P_B, P_C, P_D, P_E, P_F, P_G, P_POINTS
    P_A.value(digit[0])
    P_B.value(digit[1])
    P_C.value(digit[2])
    P_D.value(digit[3])
    P_E.value(digit[4])
    P_F.value(digit[5])
    P_G.value(digit[6])
    P_POINTS.value(digit[7])
    DIG.value(0)
    time.sleep_ms(5)
    DIG.value(1)
    
mapSymbols = {
        " ": [0, 0, 0, 0, 0, 0, 0, 0],
        "0": [1, 1, 1, 1, 1, 1, 0, 0],
        "1": [0, 1, 1, 0, 0, 0, 0, 0],
        "2": [1, 1, 0, 1, 1, 0, 1, 0],
        "3": [1, 1, 1, 1, 0, 0, 1, 0],
        "4": [0, 1, 1, 0, 0, 1, 1, 0],
        "5": [1, 0, 1, 1, 0, 1, 1, 0],
        "6": [1, 0, 1, 1, 1, 1, 1, 0],
        "7": [1, 1, 1, 0, 0, 0, 0, 0],
        "8": [1, 1, 1, 1, 1, 1, 1, 0],
        "9": [1, 1, 1, 1, 0, 1, 1, 0]
        } 
        
def setSymbol(pos, symbol, point):
    global mapSymbols, digit_vals
    v = mapSymbols[symbol]
    v[7] = point
    digit_vals[pos] = v

    
def core_one_task(name, delay):
    global P_A, P_B, P_C, P_D, P_E, P_F, P_G, P_POINTS, digit_vals, tz
    DIG1 = machine.Pin(3, machine.Pin.OUT)
    DIG1.value(1)
    DIG2 = machine.Pin(0, machine.Pin.OUT)
    DIG2.value(1)
    DIG3 = machine.Pin(1, machine.Pin.OUT)
    DIG3.value(1)
    DIG4 = machine.Pin(2, machine.Pin.OUT)
    DIG4.value(1)
    DIG = [DIG1, DIG2, DIG3, DIG4]

    P_POINTS = machine.Pin(7, machine.Pin.OUT)
    P_POINTS.value(0)
    P_A = machine.Pin(11, machine.Pin.OUT)
    P_A.value(0)
    P_B = machine.Pin(6, machine.Pin.OUT)
    P_B.value(0)
    P_C = machine.Pin(9, machine.Pin.OUT)
    P_C.value(0)
    P_D = machine.Pin(8, machine.Pin.OUT)
    P_D.value(0)    
    P_E = machine.Pin(4, machine.Pin.OUT)
    P_E.value(0)
    P_F = machine.Pin(10, machine.Pin.OUT)
    P_F.value(0)
    P_G = machine.Pin(5, machine.Pin.OUT)
    P_G.value(0)
    curH = 0
    curM = 0
    while True:
        a = time.time() + tz*60*60
        t = time.localtime(a)
        timeChanged = ((curH != t[3]) or (curM != t[4]))
        if (timeChanged):
            curH = t[3]
            curM = t[4]
            strH = str(curH)
            strM = str(curM)
            h0 = strH[0]
            if (len(strH) == 1):
                h1 = h0 
                h0 = " "
            else:
                h1 = strH[1]
            m0 = strM[0]
            if (len(strM) == 1):
                m1 = m0 
                m0 = "0"
            else:
                m1 = strM[1]
                         
            setSymbol(0, h0, 0)
            setSymbol(1, h1, 0)
            setSymbol(2, m0, 0)
            setSymbol(3, m1, 0)
        if (t[5] % 2):
            p1 = 1
        else:
            p1 = 0     
        digit_vals[1][7] = p1            
        for index in range(len(digit_vals)):
            flashDigit(DIG[index], digit_vals[index])
        
        
class mclock():
    def start(self, t):
        global tz
        tz = t
        print("mclock")
        _thread.start_new_thread(core_one_task, ("Thread 1", 1))
        
        
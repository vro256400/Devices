import BoardApp
import time
import devconfig
import outpinwithindayplan

class HeatingApp(BoardApp.BoardApp):
    switchers_ex = dict()
    class SwitchTemp:
        temp = 0    
        temp_sh = 0    
        class ModeEx:
            pin_usual = 1 # manual or schedule control
            temp_control = 2 # temperature only control
            pin_usual_temp_control = 4 # temperature control when pin settings enable this
        mode_ex = ModeEx.temp_control    
        mode_backup = None
        switchOn_backup = None

    def updateSettings(self):
        super().updateSettings()
        settings = devconfig.DevConfig("settings.txt")
        for index in range(len(self.switchers)):
            sw = self.switchers[index]
            if sw.PinName == "kotel":
                continue
            if not sw.PinName in self.switchers_ex:
                new_item = HeatingApp.SwitchTemp()
                self.switchers_ex[sw.PinName] = new_item
            sw_ex = self.switchers_ex[sw.PinName]
            v = settings.value.get(sw.PinName + "_temp")
            sw_ex.temp = int(v)
            v = settings.value.get(sw.PinName + "_temp_sh")
            sw_ex.temp_sh = int(v)
            v = settings.value.get(sw.PinName + "_mode_ex")
            if (v == "pin_usual"):
                sw_ex.mode_ex = HeatingApp.SwitchTemp.ModeEx.pin_usual
            elif (v == "temp_control"):
                sw_ex.mode_ex = HeatingApp.SwitchTemp.ModeEx.temp_control
            elif (v == "pin_usual_temp_control"):
                sw_ex.mode_ex = HeatingApp.SwitchTemp.ModeEx.pin_usual_temp_control
            sw_ex.mode_backup = None
            sw_ex.switchOn_backup = None

    def step(self) :
        super().step()
        for index in range(len(self.switchers)):
            sw = self.switchers[index]
            if sw.PinName == "kotel":
                continue       
            sw_ex = self.switchers_ex[sw.PinName]
            switchOn = (sw_ex.temp < sw_ex.temp_sh)
            if sw_ex.mode_ex == HeatingApp.SwitchTemp.ModeEx.temp_control:
                sw.mode = outpinwithindayplan.OutPinWithInDayPlan.Mode.Manual    
                sw.switchOn = switchOn
            elif sw_ex.mode_ex == HeatingApp.SwitchTemp.ModeEx.pin_usual_temp_control:
                if sw_ex.mode_backup == None:
                    sw_ex.mode_backup = sw.mode
                    sw_ex.switchOn_backup = sw.switchOn                
                if switchOn:
                    # restore original pin settings to detect hearting time
                    sw.mode = sw_ex.mode_backup
                    sw.switchOn = sw_ex.switchOn_backup
                    switchOn = sw.isTimeToRun(self.ntp.curH, self.ntp.curM)
                sw.mode = outpinwithindayplan.OutPinWithInDayPlan.Mode.Manual    
                sw.switchOn = switchOn

        return


theApp = HeatingApp()
theApp.run()


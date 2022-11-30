## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (CircuitBreakerInterface, ContactInterface,
    DigitalInputInterface, DigitalIOInterface, EthernetClientInterface,
    EthernetServerInterfaceEx, FlexIOInterface, IRInterface, PoEInterface,
    RelayInterface, SerialInterface, SWACReceptacleInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level, Slider
from extronlib.system import (Email, Clock, MESet, Timer, Wait, File, RFile,
    ProgramLog, SaveProgramLog, Ping, WakeOnLan, SetAutomaticTime, SetTimeZone)

print(Version()) ## Sanity check ControlScript Import
## End ControlScript Import ----------------------------------------------------
##
## Begin Python Imports --------------------------------------------------------
from datetime import datetime
from json import json
from typing import Dict, Tuple, List
## End Python Imports ----------------------------------------------------------
##
## Begin User Import -----------------------------------------------------------
#### Custom Code Modules
import utilityFunctions
import config

#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Function Definitions --------------------------------------------------

def InitActivityModule(UIHost: extronlib.device,
                       activityBtns: Dict[extronlib.system.MESet,
                                          extronlib.system.MESet,
                                          extronlib.ui.Button,
                                          extronlib.ui.Button],
                       confTimeLbl: extronlib.ui.Label,
                       confTimeLvl: extronlib.ui.Level,
                       DoSystemStart: function,
                       DoSystemSwitch: function,
                       DoSystemShutdown: function):
    # TODO: verify the typing for activityBtns
    # TODO: write function doc string
    
    # actBtns: extronlib.system.MESet,
    # actInds: extronlib.system.MESet,
    # confEndBtn: extronlib.ui.Button,
    # confCancelBtn: extronlib.ui.Button,

    shutdownTimer = Timer(1, ConfHandler)        

    def ConfHandler(timer, count):
        timeTillShutdown = config.shutdownConfTimer - count

        confTimeLbl.SetText(utilityFunctions.TimeIntToStr(timeTillShutdown))
        confTimeLvl.SetLevel(count)
        if count >= config.shutdownConfTimer:
            timer.Stop()
            DoSystemShutdown()

    try:
        activityBtns['select'].SetCurrent(0)
        activityBtns['indicator'].SetCurrent(0)

        confTimeLvl.SetRange(0, config.shutdownConfTimer, 1)
        confTimeLvl.SetLevel(0)

        @event(activityBtns['select'].Objects, 'Pressed')
        def ActivityChange(button, action):
            if button.Name == "ActivitySelect-Off":
                activityBtns['indicator'].SetCurrent(0)
                if currentActivity != 'off':
                    shutdownTimer.Start()
                    UIHost.ShowPopup('Shutdown-Confirmation')
                currentActivity = 'off'
            elif button.Name == "ActivitySelect-Share":
                activityBtns['indicator'].SetCurrent(1)
                if currentActivity == 'off':
                    DoSystemStart('share')
                else:
                    DoSystemSwitch('share')
                currentActivity = 'share'
            elif button.Name == "ActivitySelect-AdvShare":
                activityBtns['indicator'].SetCurrent(2)
                if currentActivity == 'off':
                    DoSystemStart('adv_share')
                else:
                    DoSystemSwitch('adv_share')
                currentActivity = 'adv_share'
            elif button.Name == "ActivitySelect-GroupWork":
                activityBtns['indicator'].SetCurrent(3)
                if currentActivity == 'off':
                    DoSystemStart('group_work')
                else:
                    DoSystemSwitch('group_work')
                currentActivity = 'group_work'
        
        @event(activityBtns['end'], 'Pressed')
        def EndNow(button, action):
            shutdownTimer.Stop()
            DoSystemShutdown()
        @event(activityBtns['cancel'], 'Pressed')
        def CancelShutdown(button, action):
            shutdownTimer.Stop()
            UIHost.HidePopup("Shutdown-Confirmation")
            
        return True
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------



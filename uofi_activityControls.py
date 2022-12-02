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
import uofi_sourceControls
import settings

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
                       DoSystemShutdown: function) -> bool:
    # TODO: verify the typing for activityBtns
    """Initializes the Activity Selection module
    
    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        activityBtns (Dict[extronlib.system.MESet, extronlib.system.MESet,
          extronlib.ui.Button, extronlib.ui.Button]): a dictionary of activity
          buttons. Should contain the following keys/value pairs:
            select: MESet of selection buttons
            indicator: MESet of indicator buttons
            end: Shutdown Confirmation End Now button
            cancel: Shutdown confirmation cancel shutdown button
        confTimeLbl (extronlib.ui.Label): Shutdown confirmation text label
        confTimeLvl (extronlib.ui.Level): Shutdown confirmation level indicator
        DoSystemStart (function): System start function, receives no arguments
        DoSystemSwitch (function): System activity switch function,
          receives no arguments
        DoSystemShutdown (function): System shutdown function,
          receives no arguments

    Returns:
        bool: True on success or False on failure
    """

    shutdownTimer = Timer(1, ConfHandler)        

    def ConfHandler(timer, count):
        timeTillShutdown = settings.shutdownConfTimer - count

        confTimeLbl.SetText(utilityFunctions.TimeIntToStr(timeTillShutdown))
        confTimeLvl.SetLevel(count)
        if count >= settings.shutdownConfTimer:
            timer.Stop()
            DoSystemShutdown()

    try:
        activityBtns['select'].SetCurrent(0)
        activityBtns['indicator'].SetCurrent(0)

        confTimeLvl.SetRange(0, settings.shutdownConfTimer, 1)
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

def SystemStart(activity: str) -> None:
    startupTime = settings.startupTimer

    settings.TransitionDict['label'].SetText(
        'System is switching on. Please Wait...')
    settings.TransitionDict['level'].SetRange(0, startupTime, 1)
    settings.TransitionDict['level'].SetLevel(0)

    settings.TP_Main.ShowPopup('Power-Transition')
    settings.TP_Main.ShowPage('Main')

    @Timer(1)
    def StartUpTimerHandler(timer, count):
        timeRemaining = startupTime - count

        settings.TransitionDict['count'].SetText(
            utilityFunctions.TimeIntToStr(timeRemaining))
        settings.TransitionDict['level'].SetLevel(count)

        # TIME SYNCED SWITCH ITEMS HERE - function in main
        settings.TransitionDict['start']['sync'](count)

        # feedback can be used here to jump out of the startup process early

        if count >= startupTime:
            timer.Stop()
            print('System started in {} mode'.format(activity))
            ProgramLog('System started in {} mode'.format(activity), 'info')
            SystemSwitch(activity)

    # STARTUP ONLY ITEMS HERE - function in main
    settings.TransitionDict['start']['init']()
    
    # TODO: assign default source to all destinations
            
def SwitchTimerHandler(timer, count):
    timeRemaining = settings.switchTimer - count

    settings.TransitionDict['count'].SetText(
        utilityFunctions.TimeIntToStr(timeRemaining))
    settings.TransitionDict['level'].SetLevel(count)

    # TIME SYNCED SWITCH ITEMS HERE - function in Main
    settings.TransitionDict['switch']['sync'](count)

    # feedback can be used here to jump out of the switch process early

    if count >= settings.switchTimer:
        timer.Stop()
        settings.TP_Main.HidePopup('Power-Transition')
        print('System configured in {} mode'.format(settings.activity))
        ProgramLog('System configured in {} mode'.format(settings.activity),
                   'info')
        
systemSwitchTimer = Timer(1, SwitchTimerHandler)
systemSwitchTimer.Pause()

@event(systemSwitchTimer, 'StateChanged')        
def SwitchTimerStateHandler(timer, state):
    if state == 'Stopped':
        if settings.activity == 'share' or settings.activity == 'group-work':
            @Wait(settings.activitySplash) 
            def activitySplash():
                src = settings.sources[
                    uofi_sourceControls.SourceIDToIndex(settings.source)]
                popup = "Source-Control-{}".format(src['src-ctl'])
                if src['src-ctl'] == 'PC':
                    popup = popup + "_{}".format(len(settings.cameras))
                settings.TP_Main.ShowPopup(popup)

def SystemSwitch(activity) -> None:
    settings.TransitionDict['label'].SetText(
        'System is switching to {} mode. Please Wait...'
        .format(settings.activityDict[activity]))
    settings.TransitionDict['level'].SetRange(0, settings.switchTimer, 1)
    settings.TransitionDict['level'].SetLevel(0)

    settings.TP_Main.ShowPopup('Power-Transition')
    settings.TP_Main.ShowPage('Main')

    settings.activity = activity
    systemSwitchTimer.Restart()

    # configure system for current activity
    settings.TP_Main.HidePopupGroup('Source-Controls')
    if activity == "share":
        settings.TP_Main.HidePopupGroup('Activity-Controls')
        # get input assigned to the primaryDestination
        curSrc = \
            uofi_sourceControls.GetSourceByDestination(settings.primaryDestination)
        
        # update source selection to match primaryDestination
        for dest in settings.destinations:
            if uofi_sourceControls.GetSourceByDestination(dest['id']) != curSrc:
                uofi_sourceControls.SwitchSources(curSrc, dest['id'])
        
        settings.TP_Main.ShowPopup("Audio-Control-{},P".format(settings.micCtl))
        
        # show activity splash screen, will be updated config.activitySplash
        # seconds after the activity switch timer stops
        settings.TP_Main.ShowPopup("Source-Control-Splash-Share")
        
    elif activity == "adv_share":
        settings.TP_Main.ShowPopup("Activity-Control-AdvShare")
        settings.TP_Main.ShowPopup(settings.adv_share_layout)
        # TODO: get inputs assigned to destination outputs, update destination
        # buttons for these assignments
        settings.TP_Main.ShowPopup("Audio-Control-{}".format(settings.micCtl))
    elif  activity == "group_work":
        settings.TP_Main.ShowPopup("Activity-Control-Group")
        settings.TP_Main.ShowPopup("Audio-Control-{},P".format(settings.micCtl))
        for dest in settings.destinations:
            uofi_sourceControls.SwitchSources(dest['group-work-src'], dest['id'])
        
    srcList = uofi_sourceControls.GetCurrentSourceList()
    curSrcIndex = uofi_sourceControls.SourceIDToIndex(settings.source, srcList)
    
    # if the srcList is paginated, shift offset to make selected source visible
    if len(srcList) > 5: 
        if curSrcIndex < settings.sourceOffset:
            settings.sourceOffset -= (settings.sourceOffset - curSrcIndex)
        elif curSrcIndex >= (settings.sourceOffset + 5):
            settings.sourceOffset = curSrcIndex - 4
            
    
    uofi_sourceControls.UpdateSourceMenu(settings.TP_Main,
                     settings.SourceButtons['select'],
                     settings.SourceButtons['indicator'],
                     settings.SourceButtons['arrows'])

def SystemShutdown() -> None:
    shutdownTime = settings.shutdownTimer
    settings.activity = 'off'

    settings.TransitionDict['label']\
        .SetText('System is switching off. Please Wait...')
    settings.TransitionDict['level'].SetRange(0, shutdownTime, 1)
    settings.TransitionDict['level'].SetLevel(0)
    
    settings.TP_Main.ShowPopup('Power-Transition')
    settings.TP_Main.ShowPage('Opening')

    @Timer(1)
    def ShutdownTimerHandler(timer, count):
        timeRemaining = shutdownTime - count

        settings.TransitionDict['count']\
            .SetText(utilityFunctions.TimeIntToStr(timeRemaining))
        settings.TransitionDict['level'].SetLevel(count)

        # TIME SYNCED SHUTDOWN ITEMS HERE - function in main
        settings.TransitionDict['shutdown']['sync'](count)

        # feedback can be used here to jump out of the shutdown process early

        if count >= shutdownTime:
            timer.Stop()
            settings.TP_Main.HidePopup('Power-Transition')
            print('System shutdown')
            ProgramLog('System shutdown', 'info')
    
    # SHUTDOWN ITEMS HERE - function in main
    settings.TransitionDict['shutdown']['init']()

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------



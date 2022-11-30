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
## End Python Imports ----------------------------------------------------------
##
## Begin User Import -----------------------------------------------------------
#### Custom Code Modules
from uofi_guiControl import *
from uofi_activityControls import *
from uofi_pinCode import *
from uofi_sourceControls import *

import utilityFunctions
import config

#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------

CtlProc_Main = ProcessorDevice('CTL001')

## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------

TP_Main = UIDevice('TP001')

#### Build Buttons & Button Groups
TP_Btns = BuildButtons(TP_Main, jsonPath='controls.json')
TP_Btn_Grps = BuildButtonGroups(TP_Btns, jsonPath="controls.json")

#### Build Knobs
TP_Knobs = BuildKnobs(TP_Main, jsonPath='controls.json')

#### Build Levels
TP_Lvls = BuildLevels(TP_Main, jsonPath='controls.json')

#### Build Sliders
TP_Slds = BuildSliders(TP_Main, jsonPath='controls.json')

#### Build Labels
TP_Lbls = BuildLabels(TP_Main, jsonPath='controls.json')

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------

## End Communication Interface Definition --------------------------------------
##
## Begin Function Definitions --------------------------------------------------

def Initialize():
    TP_Main.ShowPage('Splash')

    TP_Btns['Room-Label'].SetText(config.roomName)
    
    #### PIN Code Module
    pinModBtns = {"numPad": [TP_Btns['PIN-0'],
                             TP_Btns['PIN-1'],
                             TP_Btns['PIN-2'],
                             TP_Btns['PIN-3'],
                             TP_Btns['PIN-4'],
                             TP_Btns['PIN-5'],
                             TP_Btns['PIN-6'],
                             TP_Btns['PIN-7'],
                             TP_Btns['PIN-8'],
                             TP_Btns['PIN-9']],
                  "backspace": TP_Btns['PIN-Del'],
                  "cancel": TP_Btns['PIN-Cancel']}
    InitPINModule(TP_Main,
                  TP_Btns['Header-Settings'],
                  pinModBtns,
                  TP_Lbls['PIN-Label'],
                  config.techPIN, 
                  'Tech')

    #### Activity Control Module
    TP_Main.ShowPopup('Menu-Activity-{}'.format(config.activityMode))
    TP_Main.ShowPopup('Menu-Activity-open-{}'.format(config.activityMode))

    actModBtns = {"select": TP_Btn_Grps['Activity-Select'],
                  "indicator": TP_Btn_Grps['Activity-Indicator'],
                  "end": TP_Btns['Shutdown-EndNow'],
                  "cancel": TP_Btns['Shutdown-Cancel']}
    InitActivityModule(TP_Main,
                       actModBtns,
                       TP_Lbls['ShutdownConf-Count'],
                       TP_Lvls['ShutdownConfIndicator'],
                       SystemStart,
                       SystemSwitch,
                       SystemShutdown)

    #### Source Control Module
    InitSourceModule(TP_Main,
                     TP_Btn_Grps['Source-Select'],
                     TP_Btn_Grps['Source-Indicator']
                     [TP_Btns['SourceMenu-Prev'], TP_Btns['SourceMenu-Next']],
                     SwitchSources)
    ## DO ADDITIONAL INITIALIZATION ITEMS HERE
    
    print('System Initialized')

def SwitchSources(src: str, dest: str = 'all') -> None:
    """Switch system sources

    Args:
        src (str): Source ID string
        dest (str, optional): Destination to send source. Defaults to 'all'.
        
    Return:
        none
    """    
    pass

def SystemStart(activity):
    startupTime = config.startupTimer

    TP_Lbls['PowerTransLabel-State'].SetText('System is starting up. Please Wait...')
    TP_Lvls['PowerTransIndicator'].SetRange(0, startupTime, 1)
    TP_Lvls['PowerTransIndicator'].SetLevel(0)

    TP_Main.ShowPopup('Power-Transition')
    TP_Main.ShowPage('Main')

    @Timer(1)
    def StartUpTimerHandler(timer, count):
        timeRemaining = startupTime - count

        TP_Lbls['PowerTransLabel-Count'].SetText(utilityFunctions.TimeIntToStr(timeRemaining))
        TP_Lvls['PowerTransIndicator'].SetLevel(count)

        # DO TIME SYNCED STARTUP ITEMS HERE

        # feedback can be used here to jump out of the startup process early

        if count >= startupTime:
            timer.Stop()
            print('System started in {} mode'.format(activity))
            ProgramLog('System started in {} mode'.format(activity), 'info')
            SystemSwitch(activity)

    # DO STARTUP ONLY ITEMS HERE
            
    

def SystemSwitch(activity):
    switchTime = config.switchTimer

    TP_Lbls['PowerTransLabel-State'].SetText('System is switching to {} mode. Please Wait...'
                                             .format(systemVars['activityDict'][activity]))
    TP_Lvls['PowerTransIndicator'].SetRange(0, switchTime, 1)
    TP_Lvls['PowerTransIndicator'].SetLevel(0)

    TP_Main.ShowPopup('Power-Transition')
    TP_Main.ShowPage('Main')

    @Timer(1)
    def SwitchTimerHandler(timer, count):
        timeRemaining = switchTime - count

        TP_Lbls['PowerTransLabel-Count'].SetText(utilityFunctions.TimeIntToStr(timeRemaining))
        TP_Lvls['PowerTransIndicator'].SetLevel(count)

        # DO TIME SYNCED SWITCH ITEMS HERE

        # feedback can be used here to jump out of the switch process early

        if count >= switchTime:
            timer.Stop()
            TP_Main.HidePopup('Power-Transition')
            print('System configured in {} mode'.format(activity))
            ProgramLog('System configured in {} mode'.format(activity), 'info')

    # configure system for current activity
    if activity == "share":
        TP_Main.HidePopupGroup('Activity-Controls')
    elif activity == "adv_share":
        TP_Main.ShowPopup("Activity-Control-AdvShare")
    elif  activity == "group_work":
        TP_Main.ShowPopup("Activity-Control-Group")
        
    UpdateSourceMenu(TP_Main,
                     TP_Btn_Grps['Source-Select'],
                     TP_Btn_Grps['Source-Indicator']
                     [TP_Btns['SourceMenu-Prev'], TP_Btns['SourceMenu-Next']])

def SystemShutdown():
    shutdownTime = config.shutdownTimer

    TP_Lbls['PowerTransLabel-State'].SetText('System is switching off. Please Wait...')
    TP_Lvls['PowerTransIndicator'].SetRange(0, shutdownTime, 1)
    TP_Lvls['PowerTransIndicator'].SetLevel(0)
    
    TP_Main.ShowPopup('Power-Transition')
    TP_Main.ShowPage('Opening')

    @Timer(1)
    def ShutdownTimerHandler(timer, count):
        timeRemaining = shutdownTime - count

        TP_Lbls['PowerTransLabel-Count'].SetText(utilityFunctions.TimeIntToStr(timeRemaining))
        TP_Lvls['PowerTransIndicator'].SetLevel(count)

        # DO TIME SYNCED SHUTDOWN ITEMS HERE

        # feedback can be used here to jump out of the shutdown process early

        if count >= shutdownTime:
            timer.Stop()
            TP_Main.HidePopup('Power-Transition')
            print('System shutdown')
            ProgramLog('System shutdown', 'info')
    
    # DO SHUTDOWN ITEMS HERE

## End Function Definitions ----------------------------------------------------
##
## Event Definitions -----------------------------------------------------------

## End Events Definitions ------------------------------------------------------
##
## Start Program ---------------------------------------------------------------
Initialize()

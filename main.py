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
import json
## End Python Imports ----------------------------------------------------------
##
## Begin User Import -----------------------------------------------------------
#### Custom Code Modules
from uofi_guiControl import *
from uofi_activityControls import *
from uofi_pinCode import *
from uofi_sourceControls import *

import utilityFunctions
import settings

#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Device/Processor Definition -------------------------------------------

settings.CtlProc_Main = ProcessorDevice('CTL001')

## End Device/Processor Definition ---------------------------------------------
##
## Begin Device/User Interface Definition --------------------------------------

settings.TP_Main = UIDevice('TP001')

#### Build Buttons & Button Groups
TP_Btns = BuildButtons(settings.TP_Main, jsonPath='controls.json')
TP_Btn_Grps = BuildButtonGroups(TP_Btns, jsonPath="controls.json")

#### Build Knobs
TP_Knobs = BuildKnobs(settings.TP_Main, jsonPath='controls.json')

#### Build Levels
TP_Lvls = BuildLevels(settings.TP_Main, jsonPath='controls.json')

#### Build Sliders
TP_Slds = BuildSliders(settings.TP_Main, jsonPath='controls.json')

#### Build Labels
TP_Lbls = BuildLabels(settings.TP_Main, jsonPath='controls.json')

## End Device/User Interface Definition ----------------------------------------
##
## Begin Communication Interface Definition ------------------------------------

## End Communication Interface Definition --------------------------------------
##
## Begin Function Definitions --------------------------------------------------

def Initialize() -> bool:
    #### Set initial page & room name
    settings.TP_Main.ShowPage('Splash')
    TP_Btns['Room-Label'].SetText(settings.roomName)
    
    #### Build Common Use UI Dictionaries ======================================
    settings.TransitionDict = \
        {
            "label": TP_Lbls['PowerTransLabel-State'],
            "level": TP_Lvls['PowerTransIndicator'],
            "count": TP_Lbls['PowerTransLabel-Count'],
            "start": {
                "init": StartupActions,
                "sync": StartUpSyncedActions
              },
            "switch": {
                "init": SwitchActions,
                "sync": SwitchSyncedActions
              },
            "shutdown": {
                "init": ShutdownActions,
                "sync": ShutdownSyncedActions
              }
        }
        
    settings.SourceButtons = \
        {
            "select": TP_Btn_Grps['Source-Select'],
            "indicator": TP_Btn_Grps['Source-Indicator'],
            "arrows": [
                TP_Btns['SourceMenu-Prev'],
                TP_Btns['SourceMenu-Next']
              ]
        }
        
    settings.ActModBtns = {"select": TP_Btn_Grps['Activity-Select'],
                           "indicator": TP_Btn_Grps['Activity-Indicator'],
                           "end": TP_Btns['Shutdown-EndNow'],
                           "cancel": TP_Btns['Shutdown-Cancel']}
    
    settings.PinButtons = \
        {
            "numPad": [
                TP_Btns['PIN-0'],
                TP_Btns['PIN-1'],
                TP_Btns['PIN-2'],
                TP_Btns['PIN-3'],
                TP_Btns['PIN-4'],
                TP_Btns['PIN-5'],
                TP_Btns['PIN-6'],
                TP_Btns['PIN-7'],
                TP_Btns['PIN-8'],
                TP_Btns['PIN-9']
              ],
            "backspace": TP_Btns['PIN-Del'],
            "cancel": TP_Btns['PIN-Cancel']
        }
        
    for dest in settings.destinations:
        settings.AdvDestinationDict[dest['id']] = \
            GetBtnsForDest(TP_Btns, dest['id'])
        settings.AdvDestinationDict[dest['id']]['label'] = \
            TP_Lbls['DispAdv-{p},{r}'.format(p = dest['adv-layout']['pos'],
                                             r = dest['adv-layout']['row'])]
    
    #### =======================================================================
    
    #### PIN Code Module
    InitPINModule(settings.TP_Main,
                  TP_Btns['Header-Settings'],
                  settings.PinButtons,
                  TP_Lbls['PIN-Label'],
                  settings.techPIN, 
                  'Tech')

    #### Activity Control Module
    InitActivityModule(settings.TP_Main,
                       settings.ActModBtns,
                       TP_Lbls['ShutdownConf-Count'],
                       TP_Lvls['ShutdownConfIndicator'],
                       SystemStart,
                       SystemSwitch,
                       SystemShutdown)

    #### Source Control Module
    InitSourceModule(settings.TP_Main,
                     TP_Btn_Grps['Source-Select'],
                     TP_Btn_Grps['Source-Indicator'],
                     [TP_Btns['SourceMenu-Prev'], TP_Btns['SourceMenu-Next']],
                     settings.AdvDestinationDict,
                     SwitchSources)
    
    ## DO ADDITIONAL INITIALIZATION ITEMS HERE
    
    print('System Initialized')
    return True

def StartupActions() -> None:
    pass

def StartUpSyncedActions(count: int) -> None:
    pass

def SwitchActions() -> None:
    pass

def SwitchSyncedActions(count: int) -> None:
    pass

def ShutdownActions() -> None:
    pass

def ShutdownSyncedActions(count: int) -> None:
    pass

## End Function Definitions ----------------------------------------------------
##
## Event Definitions -----------------------------------------------------------

## End Events Definitions ------------------------------------------------------
##
## Start Program ---------------------------------------------------------------
Initialize()

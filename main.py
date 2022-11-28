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
from guiControl import *

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
    
    ## DO ADDITIONAL STARTUP ITEMS HERE
    
    print('System Initialized')

## End Function Definitions ----------------------------------------------------
##
## Event Definitions -----------------------------------------------------------

## End Events Definitions ------------------------------------------------------
##
## Start Program ---------------------------------------------------------------
Initialize()

## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (CircuitBreakerInterface, ContactInterface,
    DigitalInputInterface, DigitalIOInterface, EthernetClientInterface,
    EthernetServerInterfaceEx, FlexIOInterface, IRInterface, PoEInterface,
    RelayInterface, SerialInterface, SWACReceptacleInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level, Slider
from extronlib.system import Clock, MESet, Timer, Wait, File, SaveProgramLog

print(Version()) ## Sanity check ControlScript Import
## End ControlScript Import ----------------------------------------------------
##
## Begin Python Imports --------------------------------------------------------
from datetime import datetime
from json import *
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

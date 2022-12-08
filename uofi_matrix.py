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
import re

## End Python Imports ----------------------------------------------------------
##
## Begin User Import -----------------------------------------------------------
#### Custom Code Modules
import utilityFunctions
import settings

#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Function Definitions --------------------------------------------------

matrix_mode = 'AV'

def InitManualMatrix(UIHost: UIDevice,
                     matrixBtns: Dict,
                     matrixCtls: Dict):
    
    @event(matrixBtns, 'Pressed')
    def matrixSelectHandler(button, action):
        regex = r"Tech-Matrix-(\d+),(\d+)"
        re_match = re.match(regex, button.Name)
        # 0 is full match, 1 is input, 2 is output
        input = re_match.group(1)
        output = re_match.group(2)
        
        # TODO: figure out 
        if matrix_mode == "untie":
            pass
        elif matrix_mode == "AV":
            pass
        elif matrix_mode == "Aud":
            pass
        elif matrix_mode == "Vid":
            pass
    pass
    

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------



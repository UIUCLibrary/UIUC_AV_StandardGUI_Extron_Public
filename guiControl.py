## Begin ControlScript Import --------------------------------------------------
from extronlib import event, Version
from extronlib.device import eBUSDevice, ProcessorDevice, UIDevice
from extronlib.interface import (CircuitBreakerInterface, ContactInterface,
    DigitalInputInterface, DigitalIOInterface, EthernetClientInterface,
    EthernetServerInterfaceEx, FlexIOInterface, IRInterface, PoEInterface,
    RelayInterface, SerialInterface, SWACReceptacleInterface, SWPowerInterface,
    VolumeInterface)
from extronlib.ui import Button, Knob, Label, Level
from extronlib.system import Clock, MESet, Timer, Wait, File, RFile, ProgramLog

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
from guiControl import *
#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Function Definitions --------------------------------------------------

def BuildButtons(jsonObj = {}, jsonPath = ""):
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    buttonDict = {}
    
    ## load json file and parse into object
    if jsonObj == {} and jsonPath != "" and File.Exists(jsonPath):
        jsonFile = File(jsonPath)
        jsonStr = jsonFile.read()
        jsonFile.close()
        jsonObj = json.loads(jsonStr)

    ## format button info into buttonDict
    for button in jsonObj.buttons:
        ## TODO: Sort out initializing hold and repeat times
        buttonDict[button.Name] = Button(button.UIHost, button.ID)

    ## return buttonDict
    return buttonDict

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------
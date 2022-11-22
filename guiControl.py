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

#### Extron Global Scripter Modules

## End User Import -------------------------------------------------------------
##
## Begin Function Definitions --------------------------------------------------


def BuildButtons(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = ""):
    """Build a dictionary of Extron Buttons from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign buttons to\n
        jsonObj -- the json object containing button information\n
        jsonPath -- the path to the file containing json formatted button information\n
    
    Returns a dictionary object containing buttons on success.
    Returns false on failure.
    """
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    buttonDict = {}
    
    ## load json file and parse into object
    if jsonObj == {} and jsonPath != "" and File.Exists(jsonPath):
        jsonFile = File(jsonPath)
        jsonStr = jsonFile.read()
        jsonFile.close()
        jsonObj = json.loads(jsonStr)
    elif jsonPath != "" and not File.Exists(jsonPath):
        return False

    
    try:
        ## format button info into buttonDict
        for button in jsonObj.buttons:
            if button.holdTime == None and button.repeatTime == None:
                buttonDict[button.Name] = Button(UIHost, button.ID)
            elif button.holdTime != None and button.repeatTime == None:
                buttonDict[button.Name] = Button(UIHost, button.ID,
                                                 holdTime = button.holdTime)
            elif button.holdTime == None and button.repeatTime != None:
                buttonDict[button.Name] = Button(UIHost, button.ID, 
                                                 repeatTime = button.repeatTime)
            elif button.holdTime != None and button.repeatTime != None:
                buttonDict[button.Name] = Button(UIHost, button.ID,
                                                 holdTime = button.holdTime,
                                                 repeatTime = button.repeatTime)
        ## return buttonDict
        return buttonDict
    except Exception as inst:
        ## TODO: log exception to program log
        # https://docs.python.org/3/tutorial/errors.html
        # file:///C:/Program%20Files%20(x86)/Extron/GlobalScripter/Help/Content/Resources/ExtronLib/latest/system.html#other-methods
        return False

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------
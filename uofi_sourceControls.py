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

def InitSourceModule(UIHost: extronlib.device,
                     sourceBtns: extronlib.system.MESet,
                     sourceInds: extronlib.system.MESet,
                     arrowBtns: List[extronlib.ui.Button],
                     DoSourceSwitch: function) -> bool:
    # TODO: ensure argument typing is correct
    """Initializes Source Switching module

    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        sourceBtns (extronlib.system.MESet): MESet of source buttons
        sourceInds (extronlib.system.MESet): MESet of source indicators
        arrowBtns (List[extronlib.ui.Button]): List of arrow button objects, 0 must be previous/left button and 1 must be next/right button
        DoSourceSwitch (function): Function to run when doing a source switch should accept two arguments, first source, second destination if destination is not provided, all is assumed

    Returns:
        bool: true on success and false on failure
    """

    try:
        @event(sourceBtns.Objects, 'Pressed')
        def sourceBtnHandler(button, action):
            btnIndex = int(button.Name[-1:]) - 1 # capture last character of button.Name
            sourceInds.SetCurrent(sourceInds.Objects[btnIndex])

            srcList = GetCurrentSourceList()

            srcIndex = btnIndex + config.sourceOffset

            srcID = srcList[srcIndex]['id']
            config.source = srcID

            if config.activity != "adv_share": # advanced share doesn't switch until destination has been selected
                DoSourceSwitch(srcID)          # all other activities switch immediately
        
        @event(arrowBtns, 'Pressed')
        def sourcePageHandler(button, action):
            btnAction = button.Name[-4:] # capture last 4 characters of button.Name
            if btnAction == "Prev":
                config.sourceOffset -= 1
            elif btnAction == "Next":
                config.sourceOffset += 1
            UpdateSourceMenu(UIHost, sourceBtns, sourceInds, arrowBtns)

        return True
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def UpdateSourceMenu(UIHost: extronlib.device,
                     sourceBtns: extronlib.system.MESet,
                     sourceInds: extronlib.system.MESet,
                     arrowBtns: List[extronlib.ui.Button]) -> None:
    # TODO: ensure the typing is correct
    """Updates the formatting of the source menu. Use when the number of sources
    or the pagination of the source bar changes

    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        sourceBtns (extronlib.system.MESet): MESet of source buttons
        sourceInds (extronlib.system.MESet): MESet of source indicators
        arrowBtns (List[extronlib.ui.Button]): List of arrow buttons, 0 must be previous/left button and 1 must be next/right button

    Returns:
        none
    """    
    
    offset = config.sourceOffset
    srcList = GetCurrentSourceList()
    
    for btn in sourceBtns.Objects:
        offState = int('{}0'.format(srcList[offset]['icon']))
        onState = int('{}1'.format(srcList[offset]['icon']))
        sourceBtns.SetStates(btn, offState, onState)
        btn.SetText[srcList[offset]['name']]
        offset += 1
    
    if len(srcList) <= 5:
        UIHost.ShowPopup('Menu-Source-{}'.format(len(srcList)))
    else:
        # enable/disable previous arrow
        if offset == 0:
            arrowBtns[0].setEnable(False)
            arrowBtns[0].SetState(2)
        else:
            arrowBtns[0].setEnable(True)
            arrowBtns[0].SetState(0)
        # enable/disable next arrow
        if (offset + 5) >= len(srcList):
            arrowBtns[1].setEnable(False)
            arrowBtns[1].SetState(2)
        else:
            arrowBtns[1].setEnable(True)
            arrowBtns[1].SetState(0)
        
        UIHost.ShowPopup('Menu-Source-5+')
        
    # reset currently selected source
    currentSourceIndex = SourceIDToIndex(config.source, srcList)
    
    btnIndex = currentSourceIndex - offset
    # TODO: error handling, btnIndex should always be an int 0-4
    sourceBtns.SetCurrent(sourceBtns.Objects[btnIndex])
    sourceInds.SetCurrent(sourceInds.Objects[btnIndex])

def GetCurrentSourceList() -> List:
    """Get the current source list

    Returns:
        List: The list of currently displayable source definitions
    """    
    srcList = []
    srcNone = {"id": "none", "name": "None", "icon": 0, "input": 0}
    
    if config.activity == 'adv_share':
        srcList.append(srcNone)
    srcList.extend(config.sources)
    
    return srcList

def SourceIDToIndex(id: str, srcList: List = config.sources) -> int:
    """Get Source Index from ID. Will fail for the 'none' source if using config.sources.

    Args:
        id (str): Source ID string
        srcList (List, optional): List of source data. Defailts to config.sources

    Returns:
        int|False: Returns source dict index
    """    
    i = 0
    for src in srcList:
        if id == src['id']:
            return i
        i += 1
    ## if we get here then there was no valid index for the id and an exception should be raised
    raise LookupError("Provided ID ({}) not found".format(id))
    
def SourceNameToIndex(name: str, srcList: List = config.sources) -> int:
    """Get Source Index from Name. Will fail for the 'none' source if using config.sources.

    Args:
        name (str): Source name string
        srcList (List, optional): List of source data. Defailts to config.sources

    Returns:
        int: Returns source dict index
    """    
    i = 0
    for src in srcList:
        if name == src['name']:
            return i
        i += 1
    ## if we get here then there was no valid index for the name and an exception should be raised
    raise LookupError("Provided name ({}) not found".format(name))

def SourceNameToID(name: str, srcList: List = config.sources) -> str:
    """Get Source ID from Source Name. Will fail for the 'none' source if using config.sources

    Args:
        name (str): Source name string
        srcList (List, optional): List of source data. Defailts to config.sources

    Returns:
        str|False: Returns source ID string
    """
    
    for src in srcList:
        if name == src['name']:
            return src['id']
        i += 1
    ## if we get here then there was no valid match for the name and an exception should be raised
    raise LookupError("Provided name ({}) not found".format(name))

def SourceIDToName(id: str, srcList: List = config.sources) -> str:
    """Get Source Name from Source ID. Will fail for the 'none' source if using config.sources

    Args:
        id (str): Source ID string
        srcList (List, optional): List of source data. Defailts to config.sources

    Returns:
        str: Returns source Name string
    """
    if id == "none": return "None"    
    for src in srcList:
        if id == src['id']:
            return src['name']
        i += 1
    ## if we get here then there was no valid match for the id and an exception should be raised
    raise LookupError("Provided ID ({}) not found".format(id))

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------



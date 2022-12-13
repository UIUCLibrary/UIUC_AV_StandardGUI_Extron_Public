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
from typing import Dict, Tuple, List, Callable, Union

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

def InitSourceModule(UIHost: UIDevice,
                     sourceBtns: MESet,
                     sourceInds: MESet,
                     arrowBtns: List[Button],
                     advDest: Dict[str, Dict[str, Union[Label, Button]]],
                     DoSourceSwitch: Callable) -> bool:
    """Initializes Source Switching module

    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        sourceBtns (extronlib.system.MESet): MESet of source buttons
        sourceInds (extronlib.system.MESet): MESet of source indicators
        arrowBtns (List[extronlib.ui.Button]): List of arrow button objects, 0
            must be previous/left button and 1 must be next/right button
        advDest (Dict[str, Dict[str, Unions[extronlib.ui.Label, extronlib.ui.Button]]]):
            Dictionary of dictionaries containing advanced switching labels and
            buttons
        DoSourceSwitch (function): Function to run when doing a source switch
            should accept two arguments, first source, second destination if
            destination is not provided, all is assumed

    Returns:
        bool: true on success and false on failure
    """
    try:
        settings.adv_share_layout = GetAdvShareLayout()
        # iterate over advDest dictionary and initialize the labels/buttons as required
        for adv in advDest:
            destination = settings.destinations[DestIDToIndex(adv)]
            
            # set distination label
            advDest[adv]['label'].SetText(destination['name'])
            
            # select buttons
            advDest[adv]['select'].SetText("") 
            
            @event(advDest[adv]['select'], 'Pressed')
            def advSelectHandler(button, action):
                DoSourceSwitch(settings.source, adv)
                curSource = settings.sources[SourceIDToIndex(settings.source)]
                UpdateAdvDestButton(button, curSource)
                
            # Source Control Buttons
            advDest[adv]['ctl'].SetVisible(False)
            advDest[adv]['ctl'].Enabled(False)
            
            @event(advDest[adv]['ctl'], 'Pressed')
            def advSrcCtrHandler(button, action):
                # open source control page
                btnLoc = button.Name[-3:]
                btnPR = btnLoc.split(',')
                pos = btnPR[0]
                row = btnPR[1]
                srcID = GetSourceByAdvShareLoc(pos, row)
                curSource = settings.sources[SourceIDToIndex(srcID)]
                UIHost.ShowPopup("Modal-SrcCtl-{}"
                                 .format(curSource['adv-src-ctl']))
            
            # Destination Audio Buttons
            advDest[adv]['aud'].SetState(1)
            
            @event(advDest[adv]['aud'], ['Tapped', 'Released'])
            def advAudHandler(button, action):
                if action == "Tapped":
                    # TODO: handle system audio changes
                    if button.State == 0: # system audio unmuted
                        pass # deselect this destination as the system audio follow
                    elif button.State == 1: # system audio muted
                        pass # select this destination as the system audio follow, deselect any other destination as the system audio follow
                    elif button.State == 2: # local audio unmuted
                        pass # mute local audio
                    elif button.State == 3: # local audio muted
                        pass # unmute local audio
                elif action == "Released":
                    if (button.State == 0 or button.State == 1) \
                    and destination['type'] == 'mon':
                        # TODO: if this destination is the system audio follow, unfollow
                        muteState = 0 # TODO: get current mute state of the destination monitor
                        if muteState:
                            # TODO: set destination to unmute
                            button.SetState(2)
                        else:
                            # TODO: set mute
                            button.SetState(3)
                    elif (button.State == 2 or button.State == 3):
                        button.SetState(1)
            
            # Destination Alert Buttons
            advDest[adv]['alert'].SetVisible(False)
            advDest[adv]['alert'].Enabled(False)
            
            @event(advDest[adv]['alert'], 'Pressed')
            def destAlertHandler(button, action):
                pass # TODO: show alert modal
            
            # scnCtlBtns[adv] = advDest[adv]['scn']
            if destination['type'] == "proj+scn":
                advDest[adv]['scn'].SetVisible(True)
                advDest[adv]['scn'].Enabled(True)
            else:
                advDest[adv]['scn'].SetVisible(False)
                advDest[adv]['scn'].Enabled(False)
                
            @event(advDest[adv]['scn'], 'Pressed')
            def destScnHandler(button, action):
                pass # TODO: show screen control modal
            
        
        @event(sourceBtns.Objects, 'Pressed')
        def sourceBtnHandler(button, action):
            # capture last character of button.Name
            btnIndex = int(button.Name[-1:]) - 1
            sourceInds.SetCurrent(sourceInds.Objects[btnIndex])

            srcList = GetCurrentSourceList()

            srcIndex = btnIndex + settings.sourceOffset

            srcID = srcList[srcIndex]['id']
            settings.source = srcID

            # advanced share doesn't switch until destination has been selected
            # all other activities switch immediately
            if settings.activity != "adv_share": 
                DoSourceSwitch(srcID)         
                UIHost.ShowPopup("Source-Control-{}"
                                 .format(srcList[srcIndex]['src-ctl']))
        
        @event(arrowBtns, 'Pressed')
        def sourcePageHandler(button, action):
            # capture last 4 characters of button.Name
            btnAction = button.Name[-4:]
            if btnAction == "Prev":
                settings.sourceOffset -= 1
            elif btnAction == "Next":
                settings.sourceOffset += 1
            UpdateSourceMenu(UIHost, sourceBtns, sourceInds, arrowBtns)

        return True
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def UpdateSourceMenu(UIHost: UIDevice,
                     sourceBtns: MESet,
                     sourceInds: MESet,
                     arrowBtns: List[Button]) -> None:
    # TODO: ensure the typing is correct
    """Updates the formatting of the source menu. Use when the number of sources
    or the pagination of the source bar changes

    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        sourceBtns (extronlib.system.MESet): MESet of source buttons
        sourceInds (extronlib.system.MESet): MESet of source indicators
        arrowBtns (List[extronlib.ui.Button]): List of arrow buttons, 0 must be
            previous/left button and 1 must be next/right button

    Returns:
        none
    """    
    
    offset = settings.sourceOffset
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
    currentSourceIndex = SourceIDToIndex(settings.source, srcList)
    
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
    
    if settings.activity == 'adv_share':
        srcList.append(srcNone)
    srcList.extend(settings.sources)
    
    return srcList

def SourceIDToIndex(id: str, srcList: List = settings.sources) -> int:
    """Get Source Index from ID. Will fail for the 'none' source if using
    config.sources.

    Args:
        id (str): Source ID string
        srcList (List, optional): List of source data. Defaults to config.sources
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        int: Returns source dict index
    """    
    i = 0
    for src in srcList:
        if id == src['id']:
            return i
        i += 1
    ## if we get here then there was no valid index for the id
    raise LookupError("Provided ID ({}) not found".format(id))
    
def SourceNameToIndex(name: str, srcList: List = settings.sources) -> int:
    """Get Source Index from Name. Will fail for the 'none' source if using
    config.sources.

    Args:
        name (str): Source name string
        srcList (List, optional): List of source data. Defaults to config.sources
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        int: Returns source dict index
    """    
    i = 0
    for src in srcList:
        if name == src['name']:
            return i
        i += 1
    ## if we get here then there was no valid index for the name
    raise LookupError("Provided name ({}) not found".format(name))

def SourceNameToID(name: str, srcList: List = settings.sources) -> str:
    """Get Source ID from Source Name. Will fail for the 'none' source if using
    config.sources

    Args:
        name (str): Source name string
        srcList (List, optional): List of source data. Defaults to config.sources
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        str: Returns source ID string
    """
    
    for src in srcList:
        if name == src['name']:
            return src['id']
        i += 1
    ## if we get here then there was no valid match for the name
    raise LookupError("Provided name ({}) not found".format(name))

def SourceIDToName(id: str, srcList: List = settings.sources) -> str:
    """Get Source Name from Source ID. Will fail for the 'none' source if using
    config.sources

    Args:
        id (str): Source ID string
        srcList (List, optional): List of source data. Defaults to config.sources

    Raises:
        LookupError: raised if ID is not found in list

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

def DestIDToIndex(id: str, destList: List = settings.destinations) -> int:
    """Get Destination Index from ID.

    Args:
        id (str): Destination ID string
        destList (List, optional): List of destination data. Defaults to
            config.destinations
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        int: Returns destination dict index
    """    
    i = 0
    for dest in destList:
        if id == dest['id']:
            return i
        i += 1
    ## if we get here then there was no valid index for the id
    raise LookupError("Provided ID ({}) not found".format(id))

def DestNameToIndex(name: str, destList: List = settings.destinations) -> int:
    """Get Destination Index from Name. Will fail for the 'none' destination if
    using config.sources.

    Args:
        name (str): Destination name string
        destList (List, optional): List of destination data. Defaults to
            config.destinations
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        int: Returns destination dict index
    """    
    i = 0
    for dest in destList:
        if name == dest['name']:
            return i
        i += 1
    ## if we get here then there was no valid index for the name
    raise LookupError("Provided name ({}) not found".format(name))

def DestNameToID(name: str, destList: List = settings.destinations) -> str:
    """Get Destination ID from Destination Name. Will fail for the 'none'
    destination if using config.sources

    Args:
        name (str): Destination name string
        destList (List, optional): List of destination data. Defaults to
            config.destinations
    
    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        str: Returns destination ID string
    """
    
    for dest in destList:
        if name == dest['name']:
            return dest['id']
        i += 1
    ## if we get here then there was no valid match for the name
    raise LookupError("Provided name ({}) not found".format(name))

def DestIDToName(id: str, destList: List = settings.destinations) -> str:
    """Get Destination Name from Destination ID. Will fail for the 'none'
    destination if using config.sources

    Args:
        id (str): Destination ID string
        destList (List, optional): List of destination data. Defaults to
            config.destinations.

    Raises:
        LookupError: raised if ID is not found in list

    Returns:
        str: Returns destination Name string
    """
    if id == "none": return "None"    
    for dest in destList:
        if id == dest['id']:
            return dest['name']
        i += 1
    ## if we get here then there was no valid match for the id
    raise LookupError("Provided ID ({}) not found".format(id))

def GetBtnsForDest(btnDict: Dict[str, Button],
                   destID: str) -> Dict[str, Button]:
    """Get Advanced Display button objects for a given destination ID

    Args:
        btnDict (Dict[extronlib.ui.Button]): Dictionary of available buttons
        destID (str): Destination ID to lookup

    Raises:
        LookupError: raised when destination ID is not found in destinations
        KeyError: raised if the buttons could not be found in the dict of
            available buttons

    Returns:
        Dict[extronlib.ui.Button]: Dictionary containing the button objects for
            the specified destination
    """     
    
    destDict = {}
    
    for dest in settings.destinations:
        if dest['id'] == destID:
            pos = dest['adv-layout']['pos']
            row = dest['adv-layout']['row']
    
    if not (type(row) == type(1) and type(pos) == type(1)): 
        raise LookupError("Provided destination ID ({}) not found in destination."
                          .format(id))
    
    try:           
        destDict['select'] = btnDict['Disp-Select-{p},{r}'
                                     .format(p = pos, r = row)]
        destDict['ctl'] = btnDict['Disp-Ctl-{p},{r}'.format(p = pos, r = row)]
        destDict['aud'] = btnDict['Disp-Aud-{p},{r}'.format(p = pos, r = row)]
        destDict['alert'] = btnDict['Disp-Alert-{p},{r}'
                                    .format(p = pos, r = row)]
        destDict['scn'] = btnDict['Disp-Scn-{p},{r}'.format(p = pos, r = row)]
        
        return destDict
    except:
        raise KeyError("At least one destination button not found.".format(id))

def GetAdvShareLayout(dest: List = settings.destinations) -> str:
    layout = {}
    for d in dest:
        r = str(dest[d]['adv-layout']['row'])
        if type(layout[r]) == 'List':
            layout[r].append(dest[d]['id'])
        else:
            layout[r] = [dest[d]['id']]
            
    rows = []
    i = 0
    while i < len(layout.keys()):
        rows.append(len(layout[str(i)]))
        i += 1
        
    return "Source-Control-Adv_{}".format(",".join(rows))
            
def UpdateAdvDestButton(btn: Button,
                        ctlBtn: Button,
                        curSource: str) -> None:
    btn.SetText(curSource['name'])
    
    if curSource['adv-src-ctl'] == None:
        ctlBtn.SetVisible(False)
        ctlBtn.Enabled(False)
    else:
        ctlBtn.SetVisible(True)
        ctlBtn.Enabled(True)
        
def GetSourceByAdvShareLoc(pos: int, row: int) -> str:
    """Get the source ID based on the Adv Share location (row and position)

    Args:
        pos (int): Advanced Sharing position
        row (int): Advanced Sharing row

    Raises:
        LookupError: raised if position cannot be matched to a destination

    Returns:
        str: The string ID of the source at the advanced sharing
            location provided
    """    
    for dest in settings.destinations:
        if dest['adv-layout']['pos'] == pos \
        and dest['adv-layout']['row'] == row:
            srcID = GetSourceByDestination(dest['id'])
    if srcID == None:
        raise LookupError("Button position ({p},{r}) not found"
                          .format(p = pos, r = row))
    return srcID
        
def GetSourceByDestination(dest: str) -> str:
    """Get source ID based on destination ID

    Args:
        dest (str): The string ID of the destination of which to find the
            current source

    Returns:
        str: The string ID of the source sent to the provided destination
    """    
    
    # get switcher output from config.destinations for provided dest
    swDest = settings.destinations[DestIDToIndex(dest)]['output']
    
    # get tied input for dest output
    #### TODO: query the switcher for input tied to swDest store as swSrc
    swSrc = None
    
    # iterate over settings.sources to match switcher input to source
    for src in settings.sources:
        if swSrc == src['input']:
            # return source id string
            return src['id']
    
    raise LookupError("Source for destination ({}) could not be found"
                      .format(dest))

def SwitchSources(src: str, dest: str = 'all') -> bool:
    """Switch system sources

    Args:
        src (str): Source ID string
        dest (str, optional): Destination ID string to send source or 'all'.
            Defaults to 'all'.
        
    Return:
        bool: True on success and False on failure
    """    
    # handle src='none' as a blank input/untie
    # all should iterate over all defined destinations, and not all switcher outputs 
    # TODO: build switching functionality
    return True

def MatrixSwitchSources(src: int, dest: Union[str, int] = 'all', mode: str='AV') -> bool:
    # handle src=0 as a blank input/untie
    # all should iterate over all switcher outputs, and not just defined destinations
    # mode can be 'AV', 'Vid', or 'Aud'
    # TODO: build switching functionality
    return True

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------



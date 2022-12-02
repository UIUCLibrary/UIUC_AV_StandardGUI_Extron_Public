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
from typing import Dict, Tuple, List, Union
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


def BuildButtons(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of Extron Buttons from a json object or file

    Args (only one json arg required, jsonObj takes precedence over jsonPath):
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        jsonObj (Dict, optional): The json object containing button information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted button information. Defaults to "".

    Returns:
        Dict|None: Returns dictionary object of buttons on success or none on failure
    """    
    
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    btnDict = {}
    
    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None

    
    try:
        ## format button info into btnDict
        for button in jsonObj['buttons'].values():
            ## only sets holdTime or repeatTime for non null/None values
            if button['holdTime'] == None and button['repeatTime'] == None:
                btnDict[button['Name']] = Button(UIHost, button['ID'])
            elif button['holdTime'] != None and button['repeatTime'] == None:
                btnDict[button['Name']] = Button(UIHost, button['ID'],
                                                 holdTime = button['holdTime'])
            elif button['holdTime'] == None and button['repeatTime'] != None:
                btnDict[button['Name']] = Button(UIHost, button['ID'], 
                                                 repeatTime = button['repeatTime'])
            elif button['holdTime'] != None and button['repeatTime'] != None:
                btnDict[button['Name']] = Button(UIHost, button['ID'],
                                                 holdTime = button['holdTime'],
                                                 repeatTime = button['repeatTime'])
        
        ## return btnDict
        return btnDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return none (error)
        return None

def BuildButtonGroups(btnDict: Dict, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of mutually exclusive button groups from a json object or file

    Args (only one json arg required, jsonObj takes precedence over jsonPath):
        btnDict (Dict): The dictionary of available button objects
        jsonObj (Dict, optional): The json object containing button group information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted button group information. Defaults to "".

    Returns:
        Dict|None: Returns a dictionary containing Extron MESet objects on success, or None on failure
    """
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    grpDict = {}
    
    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None
    
    try:
        ## create MESets and build grpDict
        for group in jsonObj['buttonGroups'].values():
            ## reset btnList and populate it from the jsonObj
            btnList = []
            for btn in group['Buttons'].values():
                ## get button objects from Dict and add to list
                btnList.append(btnDict[btn])
            grpDict[group['Name']] = MESet(btnList)
        
        ## return grpDict
        return grpDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return None (error)
        return None

def BuildKnobs(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of Extron Knobs from a json object or file

    Args (only one json arg required, jsonObj takes precedence over jsonPath):
        UIHost (extronlib.device): UIHost to which the knobs are assigned
        jsonObj (Dict, optional): The json object containing knob information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted knob information. Defaults to "".

    Returns:
        Dict|None: Returns a dictionary containing Extron Knob objects on success, or None on failure
    """    
    
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    knobDict = {}

    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None
    
    try:
        ## format knob info into knobDict
        for knob in jsonObj['knobs'].values():
            knobDict[knob['Name']] = Knob(UIHost, knob['ID'])
        
        ## return knobDict
        return knobDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return none (error)
        return None

def BuildLevels(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of Extron Levels from a json object or file

    Args:
        UIHost (extronlib.device): UIHost to which the levels are assigned
        jsonObj (Dict, optional): The json object containing level information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted level information. Defaults to "".

    Returns:
        Dict|False: Returns a dictionary containing Extron Level objects on success, or False on failure
    """    
    
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    lvlDict = {}

    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None
    
    try:
         ## format level info into knobDict
        for lvl in jsonObj['levels'].values():
            lvlDict[lvl['Name']] = Level(UIHost, lvl['ID'])
        
        ## return lvlDict
        return lvlDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return none (error)
        return None

def BuildSliders(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of Extron Sliders from a json object or file

    Args (only one json arg required, jsonObj takes precedence over jsonPath):
        UIHost (extronlib.device): UIHost to which the sliders are assigned
        jsonObj (Dict, optional): The json object containing slider information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted slider information. Defaults to "".

    Returns:
        Dict|None: Returns a dictionary of Extron Slider objects on success, or None on failure
    """    
    
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    sliderDict = {}
    
    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None
    
    try:
         ## format slider info into knobDict
        for slider in jsonObj['sliders'].values():
            sliderDict[slider['Name']] = Slider(UIHost, slider['ID'])
        
        ## return sliderDict
        return sliderDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return none (error)
        return None

def BuildLabels(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = "") -> Union[Dict, None]:
    """Builds a dictionary of Extron Labels from a json object or file

    Args (only one json arg required, jsonObj takes precedence over jsonPath):
        UIHost (extronlib.device): UIHost to which the labels are assigned
        jsonObj (Dict, optional): The json object containing label information. Defaults to {}.
        jsonPath (str, optional): The path to the file containing json formatted label information. Defaults to "".

    Returns:
        Dict|None: Returns a dictionary of Extron Label objects on success, or None on failure
    """    
    
    ## do not expect both jsonObj and jsonPath
    ## jsonObj should take priority over jsonPath
    labelDict = {}

    if jsonObj == {} and jsonPath != "": # jsonObj is empty and jsonPath not blank
        if File.Exists(jsonPath): # jsonPath is valid, so load jsonObj from path
            jsonFile = File(jsonPath)
            jsonStr = jsonFile.read()
            jsonFile.close()
            jsonObj = json.loads(jsonStr)
        else: ## jsonPath was invalid, so return none (error)
            return None
    
    try:
         ## format label info into knobDict
        for lbl in jsonObj['labels'].values():
            labelDict[lbl['Name']] = Label(UIHost, lbl['ID'])
        
        ## return labelDict
        return labelDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return none (error)
        return None

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------
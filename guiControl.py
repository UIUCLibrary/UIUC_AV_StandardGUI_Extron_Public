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
    """Builds a dictionary of Extron Buttons from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign buttons to\n
        jsonObj -- the json object containing button information\n
        jsonPath -- the path to the file containing json formatted button information\n
    
    Returns a dictionary object containing buttons on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False

    
    try:
        ## format button info into btnDict
        for button in jsonObj.buttons:
            ## only sets holdTime or repeatTime for non null/None values
            if button.holdTime == None and button.repeatTime == None:
                btnDict[button.Name] = Button(UIHost, button.ID)
            elif button.holdTime != None and button.repeatTime == None:
                btnDict[button.Name] = Button(UIHost, button.ID,
                                                 holdTime = button.holdTime)
            elif button.holdTime == None and button.repeatTime != None:
                btnDict[button.Name] = Button(UIHost, button.ID, 
                                                 repeatTime = button.repeatTime)
            elif button.holdTime != None and button.repeatTime != None:
                btnDict[button.Name] = Button(UIHost, button.ID,
                                                 holdTime = button.holdTime,
                                                 repeatTime = button.repeatTime)
        
        ## return btnDict
        return btnDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def BuildButtonGroups(btnDict: Dict, jsonObj: Dict = {}, jsonPath: str = ""):
    """Builds a dictionary of mutually exclusive button groups from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        btnDict (required) -- the dictionary of available button objects\n
        jsonObj -- the json object containing button group information\n
        jsonPath -- the path to the file containing json formatted button group information\n
    
    Returns a dictionary object containing Extron MESet objects on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False
    
    try:
        ## create MESets and build grpDict
        for group in jsonObj.buttonGroups:
            ## reset btnList and populate it from the jsonObj
            btnList = []
            for btn in group.buttons:
                ## get button objects from Dict and add to list
                btnList.append(btnDict[btn])
            grpDict[group.name] = MESet(btnList)
        
        ## return grpDict
        return grpDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def BuildKnobs(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = ""):
    """Builds a dictionary of Extron Knobs from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign knobs to\n
        jsonObj -- the json object containing knob information\n
        jsonPath -- the path to the file containing json formatted knob information\n
    
    Returns a dictionary object containing knobs on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False
    
    try:
        ## 
        ## TODO: complete BuildKnobs function definition
        
        ## return knobDict
        return knobDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def BuildLevels(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = ""):
    """Builds a dictionary of Extron Levels from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign levels to\n
        jsonObj -- the json object containing level information\n
        jsonPath -- the path to the file containing json formatted level information\n
    
    Returns a dictionary object containing levels on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False
    
    try:
        ## 
        ## TODO: complete BuildLevels function definition
        
        ## return lvlDict
        return lvlDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def BuildSliders(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = ""):
    """Builds a dictionary of Extron Sliders from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign sliders to\n
        jsonObj -- the json object containing slider information\n
        jsonPath -- the path to the file containing json formatted slider information\n
    
    Returns a dictionary object containing sliders on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False
    
    try:
        ## 
        ## TODO: complete BuildSliders function definition
        
        ## return sliderDict
        return sliderDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

def BuildLabels(UIHost: extronlib.device, jsonObj: Dict = {}, jsonPath: str = ""):
    """Builds a dictionary of Extron Labels from a json object or file
    
    Keyword arguments (only one json arg required, jsonObj takes precedence over jsonPath):\n
        UIHost (required) -- the UIHost object to assign labels to\n
        jsonObj -- the json object containing label information\n
        jsonPath -- the path to the file containing json formatted label information\n
    
    Returns a dictionary object containing labels on success.
    Returns false on failure.
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
        else: ## jsonPath was invalid, so return false (error)
            return False
    
    try:
        ## 
        ## TODO: complete BuildLabels function definition
        
        ## return labelDict
        return labelDict
    except Exception as inst: 
        ## catch exceptions which may occure from misformated or missing data
        ## log execption data to program log
        execptStr = "Python Execption: {} ({})".format(inst, inst.args)
        ProgramLog(execptStr, 'warning')
        ## return false (error)
        return False

## End Function Definitions ----------------------------------------------------
##
## Begin Script Definition -----------------------------------------------------
if __name__ == "__main__": ## this module does not run as a script
    pass
## End Script Definition -------------------------------------------------------
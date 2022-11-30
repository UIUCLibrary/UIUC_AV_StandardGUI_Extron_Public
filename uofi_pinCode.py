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
currentPin = ""

def pinMask(pinLbl: extronlib.ui.Label, pinStr: str):
    """Generates and sets Masked PIN feedback

    Keywork arguments - all required:\n
        pinLbl -- the label object to send the masked string to\n
        pinStr -- the string to be masked\n

    Returns the masked string
    """
    mask = ""
    while (len(mask) < len(pinStr)):
        mask = mask + "*"
    pinLbl.SetText(mask)
    return mask

def InitPINModule(UIHost: extronlib.device,
                  startBtn: extronlib.ui.Button,
                  pinBtns: Dict[List[extronlib.ui.Button], # 0-9 buttons
                                extronlib.ui.Button,       # backspace button
                                extronlib.ui.Button],      # cancel button
                  pinLbl: extronlib.ui.Label,
                  pinCode: str,
                  destPage: str):
    # TODO: verify the typing for pinBtns
    """Initialized the PIN Code Security Module.

    Keywork arguments - all required:\n
        UIHost -- the UIHost object to assign buttons to\n
        startBtn -- the button object which triggers the pin code module\n
        pinBtns -- dictionary containing pin page buttons such as:\n
              {"numPad": [TP_Btns['PIN-0'],\n
                          TP_Btns['PIN-1'],\n
                          TP_Btns['PIN-2'],\n
                          TP_Btns['PIN-3'],\n
                          TP_Btns['PIN-4'],\n
                          TP_Btns['PIN-5'],\n
                          TP_Btns['PIN-6'],\n
                          TP_Btns['PIN-7'],\n
                          TP_Btns['PIN-8'],\n
                          TP_Btns['PIN-9']],\n
              "backspace": TP_Btns['PIN-Del'],\n
              "cancel": TP_Btns['PIN-Cancel']}\n
        pinLbl -- the label object which will contain masked user feedback\n
        pinCode -- the master pin value to match against,\n
        destPage -- the page to show on successful pin auth\n

        Returns true on success and false on failure.
    """

    try:
        currentPIN = ""
        
        pinMask(pinLbl, currentPIN)

        @event(pinBtns['numPad'], 'Pressed')
        def UpdatePIN(button, action):
            val = button['ID'] - 9000
                # pin button IDs should start at 9000 and be in numerical order
            currentPIN = currentPIN + str(val)
            pinMask(pinLbl, currentPIN) #remask pin after change
            if (currentPIN == pinCode):
                UIHost.ShowPopup("PIN Outcome Success", 2)
                # clean up and go to destination page while success popup is up
                UIHost.ShowPage(destPage)
                UIHost.HidePopup("PIN Code")
            elif (len(currentPIN) >= 10):
                UIHost.ShowPopup("PIN Outcome Failure", 2)
                # clean up and go back to pin page while failure popup is up
                currentPIN = ""
                pinMask(pinLbl, currentPIN)
        
        @event(pinBtns['backspace'], 'Pressed')
        def BackspacePIN(button, action):
            currentPIN = currentPIN[:-1] # remove last character of current pin
            pinMask(pinLbl, currentPIN)  # remask pin after change

        @event(pinBtns['cancel'], 'Pressed')
        def CancelPIN(button, action):
            UIHost.HidePopup("PIN Code")

        @event(startBtn, 'Held')
        # triggers on startBtn defined long press, 3 sec recommended
        def ShowPIN(button, action):
            currentPIN = ""
            pinMask(pinLbl, currentPIN)
            UIHost.ShowPopup("PIN Code")
            
        return True
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



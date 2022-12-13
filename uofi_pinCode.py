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
from typing import Dict, Tuple, List, Union
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
currentPin = ""

def pinMask(pinLbl: Label, pinStr: str) -> str:
    """Generates and sets Masked PIN feedback

    Args:
        pinLbl (extronlib.ui.Label): the label object to send the masked string
        pinStr (str): the string to be masked

    Returns:
        str: the masked string
    """    

    mask = ""
    while (len(mask) < len(pinStr)):
        mask = mask + "*"
    pinLbl.SetText(mask)
    return mask

def InitPINModule(UIHost: UIDevice,
                  startBtn: Button,
                  pinBtns: Dict[str, Union[List[Button], Button]],
                  pinLbl: Label,
                  pinCode: str,
                  destPage: str) -> bool:
    """Initializes the PIN security module

    Args:
        UIHost (extronlib.device): UIHost to which the buttons are assigned
        startBtn (extronlib.ui.Button): the button object which triggers the pin
            code module
        pinBtns (Dict[List[extronlib.ui.Button],
                      extronlib.ui.Button,
                      extronlib.ui.Button]): dictionary containing pin page
            buttons such as:
            {
                "numPad":
                    [
                        TP_Btns['PIN-0'],
                        TP_Btns['PIN-1'],
                        TP_Btns['PIN-2'],
                        TP_Btns['PIN-3'],
                        TP_Btns['PIN-4'],
                        TP_Btns['PIN-5'],
                        TP_Btns['PIN-6'], 
                        TP_Btns['PIN-7'],
                        TP_Btns['PIN-8'],
                        TP_Btns['PIN-9']
                    ],
             "backspace": TP_Btns['PIN-Del'],
             "cancel": TP_Btns['PIN-Cancel']
            }
        pinLbl (extronlib.ui.Label): the label object which will contain masked
            user feedback
        pinCode (str): the master pin value to match against
        destPage (str): the page to show on successful pin auth

    Returns:
        bool: true on success, false on failure
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



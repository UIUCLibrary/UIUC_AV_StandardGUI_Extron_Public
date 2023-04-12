import unittest
import os
import importlib

import sys
sys.path.append(".\\src")
sys.path.append(".\\tests")
sys.path.append(".\\tests\\reqs")


## test imports ----------------------------------------------------------------
from uofi_gui import GUIController
from uofi_gui.uiObjects import ExUIDevice
from uofi_gui.systemHardware import SystemHardwareController
from uofi_gui.deviceControl import AudioController, CameraController, DisplayController
from uofi_gui.sourceControls import Destination
import test_settings as settings

from extronlib.device import UIDevice
from extronlib.ui import Button, Label, Level, Slider
from extronlib.system import MESet, File
## -----------------------------------------------------------------------------

import test_uofi_gui_deviceControl_audioControl
import test_uofi_gui_deviceControl_cameraControl
import test_uofi_gui_deviceControl_displayControl


if __name__ == '__main__':
    unittest.main()
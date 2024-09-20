from typing import TYPE_CHECKING, Dict, Tuple, List, Union, Callable
if TYPE_CHECKING: # pragma: no cover
    from uofi_gui import GUIController

from extronlib.interface import SerialInterface, EthernetClientInterface
import re
from struct import pack, unpack
from itertools import cycle

import utilityFunctions

class DeviceClass:
    def __init__(self):
        self.Unidirectional = 'False'
        self.connectionCounter = 15
        self.DefaultResponseTimeout = 0.3
        self.Subscription = {}
        self.counter = 0
        self.connectionFlag = True
        self.initializationChk = True
        self.Debug = False
        self.Models = {}
        self.Commands = {
            'ConnectionStatus': {'Status': {}},
            'AspectRatio': {'Status': {}},
            'AudioMute': {'Status': {}},
            'AutoImage': {'Status': {}},
            'DeviceStatus': {'Status': {}},
            'FilterUsage': {'Status': {}},
            'Freeze': {'Status': {}},
            'Input': {'Status': {}},
            'LampMode': {'Status': {}},
            'LampUsage': {'Status': {}},
            'LensControl': {'Parameters': ['Type'], 'Status': {}},
            'LensProfile': {'Status': {}},
            'LensProfileControl': {'Status': {}},
            'MenuNavigation': {'Status': {}},
            'OnScreenDisplay': {'Status': {}},
            'Power': {'Status': {}},
            'Shutter': {'Status': {}},
            'VideoMute': {'Status': {}},
            'Volume': {'Status': {}},
        }
      
        if self.Unidirectional == 'False':
            self.SetRegAspectRatio = re.compile(b'(\xA3\x10[\x00-\xFF]{6}|\x23\x10[\x00-\xFF]{6})')
            self.SetRegAudioMute = re.compile(b'(\xA2[\x12\x13][\x00-\xFF]{6}|\x22[\x12\x13][\x00-\xFF]{4})')
            self.SetRegAutoImage = re.compile(b'(\xA2\x0F[\x00-\xFF]{6}|\x22\x0F[\x00-\xFF]{5})')
            self.SetRegFreeze = re.compile(b'(\xA1\x98[\x00-\xFF]{6}|\x21\x98[\x00-\xFF]{5})')
            self.SetRegInput = re.compile(b'(\xA2\x03[\x00-\xFF]{6}|\x22\x03[\x00-\xFF]{5})')
            self.SetRegLampMode = re.compile(b'(\xA3\xB1[\x00-\xFF]{6}|\x23\xB1[\x00-\xFF]{6})')
            self.SetRegLensControl = re.compile(b'(\xA2\x18[\x00-\xFF]{6}|\x22\x18[\x00-\xFF]{5})')
            self.SetRegLensProfile = re.compile(b'(\xA2\x27[\x00-\xFF]{6}|\x22\x27[\x00-\xFF]{6})')
            self.SetRegLensProfileControl = re.compile(b'(\xA2\x1F[\x00-\xFF]{6}|\x22\x1F[\x00-\xFF]{6})')
            self.SetRegMenuNavigation = re.compile(b'(\xA2\x0F[\x00-\xFF]{6}|\x22\x0F[\x00-\xFF]{5})')
            self.SetRegOnScreenDisplay = re.compile(b'(\xA2[\x14\x15][\x00-\xFF]{6}|\x22[\x14\x15][\x00-\xFF]{4})')
            self.SetRegPower = re.compile(b'(\xA2[\x00\x01][\x00-\xFF]{6}|\x22[\x00\x01][\x00-\xFF]{4})')
            self.SetRegShutter = re.compile(b'(\xA2[\x16\x17][\x00-\xFF]{6}|\x22[\x16\x17][\x00-\xFF]{4})')
            self.SetRegVideoMute = re.compile(b'(\xA2[\x10\x11][\x00-\xFF]{6}|\x22[\x10\x11][\x00-\xFF]{4})')
            self.SetRegVolume = re.compile(b'(\xA3\x10[\x00-\xFF]{6}|\x23\x10[\x00-\xFF]{6})')

            self.GetRegDeviceStatus = re.compile(b'(\xA0\x88[\x00-\xFF]{6}|\x20\x88[\x00-\xFF]{16})')
            self.GetRegFilterUsage = re.compile(b'(\xA3\x95[\x00-\xFF]{6}|\x23\x95[\x00-\xFF]{12})')
            self.GetRegLampMode = re.compile(b'(\xA3\xB0[\x00-\xFF]{6}|\x23\xB0[\x00-\xFF]{6})')
            self.GetRegLampUsage = re.compile(b'(\xA3\x96[\x00-\xFF]{6}|\x23\x96[\x00-\xFF]{10})')
            self.GetRegLensProfile = re.compile(b'(\xA2\\x28[\x00-\xFF]{6}|\x22\\x28[\x00-\xFF]{6})')
            self.GetRegPower = re.compile(b'(\xA0\xBF[\x00-\xFF]{6}|\x20\xBF[\x00-\xFF]{20})')
            self.GetRegVolume = re.compile(b'(\xA3\x05[\x00-\xFF]{6}|\x23\x05[\x00-\xFF]{20})')

            self.SetDelim = {
                'AspectRatio': self.SetRegAspectRatio,
                'AudioMute': self.SetRegAudioMute,
                'AutoImage': self.SetRegAutoImage,
                'Freeze': self.SetRegFreeze,
                'Input': self.SetRegInput,
                'LampMode': self.SetRegLampMode,
                'LensControl': self.SetRegLensControl,
                'LensProfile': self.SetRegLensProfile,
                'LensProfileControl': self.SetRegLensProfileControl,
                'MenuNavigation': self.SetRegMenuNavigation,
                'OnScreenDisplay': self.SetRegOnScreenDisplay,
                'Power': self.SetRegPower,
                'Shutter': self.SetRegShutter,
                'VideoMute': self.SetRegVideoMute,
                'Volume': self.SetRegVolume
            }

            self.UpdateDelim = {
                'DeviceStatus': self.GetRegDeviceStatus,
                'FilterUsage': self.GetRegFilterUsage,
                'LampMode': self.GetRegLampMode,
                'LampUsage': self.GetRegLampUsage,
                'LensProfile': self.GetRegLensProfile,
                'Power': self.GetRegPower,
                'Volume': self.GetRegVolume
            }

## -----------------------------------------------------------------------------
## Start Feedback Callback Functions
## -----------------------------------------------------------------------------

    # def AudioMuteStatusHandler(self, command, value, qualifier, hardware=None):
    #     utilityFunctions.Log('{} {} Callback; Value: {}; Qualifier {}'.format(hardware.Name, command, value, qualifier))
    #     for TP in self.GUIHost.TPs:
    #         TP.DispCtl.DisplayMuteFeedback(hardware.Id, value)
        
    def PowerStatusHandler(self, command, value, qualifier, hardware=None):
        utilityFunctions.Log('{} {} Callback; Value: {}; Qualifier {}'.format(hardware.Name, command, value, qualifier))
        for TP in self.GUIHost.TPs:
            TP.DispCtl.DisplayPowerFeedback(hardware.Id, value)
        
    # def VolumeStatusHandler(self, command, value, qualifier, hardware=None):
    #     utilityFunctions.Log('{} {} Callback; Value: {}; Qualifier {}'.format(hardware.Name, command, value, qualifier))
    #     for TP in self.GUIHost.TPs:
    #         TP.DispCtl.DisplayVolumeFeedback(hardware.Id, value)

## -----------------------------------------------------------------------------
## End Feedback Callback Functions
## -----------------------------------------------------------------------------

    def SetAspectRatio(self, value, qualifier):

        ValueStateValues = {
            '4:3': b'\x03\x10\x00\x00\x05\x18\x00\x00\x00\x00\x30',
            'Letterbox': b'\x03\x10\x00\x00\x05\x18\x00\x00\x01\x00\x31',
            '16:9': b'\x03\x10\x00\x00\x05\x18\x00\x00\x02\x00\x32',
            'Full': b'\x03\x10\x00\x00\x05\x18\x00\x00\x06\x00\x36',
            'Zoom': b'\x03\x10\x00\x00\x05\x18\x00\x00\x07\x00\x37',
            '5:4': b'\x03\x10\x00\x00\x05\x18\x00\x00\x0b\x00\x3b',
            '16:10': b'\x03\x10\x00\x00\x05\x18\x00\x00\x0c\x00\x3c',
            '15:9': b'\x03\x10\x00\x00\x05\x18\x00\x00\x0d\x00\x3d',
            'Native': b'\x03\x10\x00\x00\x05\x18\x00\x00\x0e\x00\x3e',
            'Auto': b'\x03\x10\x00\x00\x05\x18\x00\x00\x0f\x00\x3f',
            'Normal': b'\x03\x10\x00\x00\x05\x18\x00\x00\x10\x00\x40'
        }

        AspectRatioCmdString = ValueStateValues[value]
        self.__SetHelper('AspectRatio', AspectRatioCmdString, value, qualifier)

    def SetAudioMute(self, value, qualifier):

        AudioMuteState = {
            'On': b'\x02\x12\x00\x00\x00\x14',
            'Off': b'\x02\x13\x00\x00\x00\x15'
        }

        AudioMuteCmdString = AudioMuteState[value]
        self.__SetHelper('AudioMute', AudioMuteCmdString, value, qualifier)

    def SetAutoImage(self, value, qualifier):

        AutoImageCmdString = b'\x02\x0f\x00\x00\x02\x05\x00\x18'
        self.__SetHelper('AutoImage', AutoImageCmdString, value, qualifier)

    def UpdateDeviceStatus(self, value, qualifier):
        
        DeviceStatusState = {
            b'\x00\x00\x00\x00': 'Normal',
            b'\x01\x00\x00\x00': 'Lamp Cover Error',
            b'\x02\x00\x00\x00': 'Temperature Error',
            b'\x08\x00\x00\x00': 'Fan Failure',
            b'\x10\x00\x00\x00': 'Fan Failure',
            b'\x20\x00\x00\x00': 'Power Error',
            b'\x40\x00\x00\x00': 'Lamp Error',
            b'\x80\x00\x00\x00': 'Lamp Life Expired',
            b'\x00\x01\x00\x00': 'Lamp Beyond Limit',
            b'\x00\x02\x00\x00': 'Format Error',
            b'\x00\x00\x02\x00': 'FPGA Error',
            b'\x00\x00\x04\x00': 'Temp Sensor Failure',
            b'\x00\x00\x08\x00': 'Lamp Housing Error',
            b'\x00\x00\x10\x00': 'Lamp Data Error',
            b'\x00\x00\x20\x00': 'Mirror Cover Error',
            b'\x00\x00\x00\x04': 'High Temperature',
            b'\x00\x00\x00\x08': 'Sensor Error',
            b'\x00\x00\x00\x20': 'Ballast Communication Error',
            b'\x00\x00\x00\x40': 'Iris Calibration Error',
            b'\x00\x00\x00\x80': 'Lens Not Properly Installed'
        }
        
        res = self.__UpdateHelper('DeviceStatus', b'\x00\x88\x00\x00\x00\x88', value, qualifier)
        if res:
            try:
                value = DeviceStatusState.get(res[5:9], 'Multiple Errors')
                self.WriteStatus('DeviceStatus', value, qualifier)
            except (KeyError, IndexError):
                self.Error(['Device Status: Invalid/Unexpected Response'])

    def UpdateFilterUsage(self, value, qualifier):

        res = self.__UpdateHelper('FilterUsage', b'\x03\x95\x00\x00\x00\x98', value, qualifier)
        if res:
            try:
                value = int(unpack('>I', res[8:9] + res[7:8] + res[6:7] + res[5:6])[0] / 3600)
                self.WriteStatus('FilterUsage', value, qualifier)
            except (ValueError, IndexError):
                self.Error(['Filter Usage: Invalid/Unexpected Response'])

    def SetFreeze(self, value, qualifier):

        FreezeState = {
            'On': b'\x01\x98\x00\x00\x01\x01\x9B',
            'Off': b'\x01\x98\x00\x00\x01\x02\x9C'
        }

        FreezeCmdString = FreezeState[value]
        self.__SetHelper('Freeze', FreezeCmdString, value, qualifier)

    def SetInput(self, value, qualifier):

        ValueStateValues = {
            'HDMI 1': b'\x02\x03\x00\x00\x02\x01\xa1\xa9',
            'HDMI 2': b'\x02\x03\x00\x00\x02\x01\xa2\xaa',
            'DisplayPort': b'\x02\x03\x00\x00\x02\x01\xa6\xae',
            'Computer': b'\x02\x03\x00\x00\x02\x01\x01\x09',
            'HDBaseT': b'\x02\x03\x00\x00\x02\x01\xbf\xc7'
        }

        InputCmdString = ValueStateValues[value]
        self.__SetHelper('Input', InputCmdString, value, qualifier)

    def SetLampMode(self, value, qualifier):

        LampModeState = {
            'Normal': b'\x03\xB1\x00\x00\x02\x07\x00\xBD',
            'Eco 1': b'\x03\xB1\x00\x00\x02\x07\x02\xBF',
            'Eco 2': b'\x03\xB1\x00\x00\x02\x07\x03\xC0',
            'Long Life': b'\x03\xB1\x00\x00\x02\x07\x04\xC1',
        }

        LampModeCmdString = LampModeState[value]
        self.__SetHelper('LampMode', LampModeCmdString, value, qualifier)

    def UpdateLampMode(self, value, qualifier):

        LampModeState = {
            0x00: 'Normal',
            0x02: 'Eco 1',
            0x03: 'Eco 2',
            0x04: 'Long Life'
            }
        
        res = self.__UpdateHelper('LampMode', b'\x03\xB0\x00\x00\x01\x07\xBB', value, qualifier)
        if res:
            try:
                value = LampModeState[res[6]]
                self.WriteStatus('LampMode', value, qualifier)
            except (KeyError, IndexError):
                self.Error(['Lamp Mode: Invalid/Unexpected Response'])

    def UpdateLampUsage(self, value, qualifier):

        res = self.__UpdateHelper('LampUsage', b'\x03\x96\x00\x00\x02\x00\x01\x9C', value, qualifier)
        if res:
            try:
                value = int(unpack('>I', res[10:11] + res[9:10] + res[8:9] + res[7:8])[0] / 3600)
                self.WriteStatus('LampUsage', value, qualifier)
            except (ValueError, IndexError):
                self.Error(['Lamp Usage: Invalid/Unexpected Response'])

    def SetLensControl(self, value, qualifier):

        TypeStates = {
            'Zoom': 0x00,
            'Focus': 0x01,
            'Lens Shift (H)': 0x02,
            'Lens Shift (V)': 0x03,
        }

        ValueStateValues = {
            'Plus': 0x7F,
            'Minus': 0x81,
            'Stop': 0x00,
        }

        control_type = qualifier['Type']
        if control_type in TypeStates and value in ValueStateValues:
            data01 = TypeStates[control_type]
            data02 = ValueStateValues[value]
            CKS = 0x1C + data01 + data02
            LensControlCmdString = pack('8B', 0x02, 0x18, 0x00, 0x00, 0x02, data01, data02, CKS)
            self.__SetHelper('LensControl', LensControlCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetLensControl')

    def SetLensProfile(self, value, qualifier):

        ValueStateValues = {
            '1': b'\x02\x27\x00\x00\x01\x00\x2A',
            '2': b'\x02\x27\x00\x00\x01\x01\x2B'
        }

        LensProfileCmdString = ValueStateValues[value]
        self.__SetHelper('LensProfile', LensProfileCmdString, value, qualifier)

    def UpdateLensProfile(self, value, qualifier):

        LensProfileState = {
            0x00: '1',
            0x01: '2'
        }
        res = self.__UpdateHelper('LensProfile', b'\x02\x28\x00\x00\x00\x2A', value, qualifier)
        if res:
            try:
                value = LensProfileState[res[5]]
                self.WriteStatus('LensProfile', value, qualifier)
            except (KeyError, IndexError):
                self.Error(['Lens Profile: Invalid/Unexpected Response'])

    def SetLensProfileControl(self, value, qualifier):

        ValueStateValues = {
            'Move': b'\x02\x1F\x00\x00\x01\x00\x22',
            'Store': b'\x02\x1F\x00\x00\x01\x01\x23',
            'Reset': b'\x02\x1F\x00\x00\x01\x02\x24'
        }

        LensProfileControlCmdString = ValueStateValues[value]
        self.__SetHelper('LensProfileControl', LensProfileControlCmdString, value, qualifier)

    def SetMenuNavigation(self, value, qualifier):

        MenuNavigationState = {
            'Up': b'\x02\x0F\x00\x00\x02\x07\x00\x1A',
            'Down': b'\x02\x0F\x00\x00\x02\x08\x00\x1B',
            'Left': b'\x02\x0F\x00\x00\x02\x0A\x00\x1D',
            'Right': b'\x02\x0F\x00\x00\x02\x09\x00\x1C',
            'Enter': b'\x02\x0F\x00\x00\x02\x0B\x00\x1E',
            'Exit': b'\x02\x0F\x00\x00\x02\x0C\x00\x1F',
            'Menu': b'\x02\x0F\x00\x00\x02\x06\x00\x19'
        }

        MenuNavigationCmdString = MenuNavigationState[value]
        self.__SetHelper('MenuNavigation', MenuNavigationCmdString, value, qualifier)

    def SetOnScreenDisplay(self, value, qualifier):

        OnScreenDisplayState = {
            'On': b'\x02\x15\x00\x00\x00\x17',
            'Off': b'\x02\x14\x00\x00\x00\x16'
        }

        OnScreenDisplayCmdString = OnScreenDisplayState[value]
        self.__SetHelper('OnScreenDisplay', OnScreenDisplayCmdString, value, qualifier)

    def SetPower(self, value, qualifier):

        ValueStateValues = {
            'On': b'\x02\x00\x00\x00\x00\x02',
            'Off': b'\x02\x01\x00\x00\x00\x03'
        }

        PowerCmdString = ValueStateValues[value]
        self.__SetHelper('Power', PowerCmdString, value, qualifier)

    def UpdateDeviceStatus(self, value, qualifier):
        self.UpdatePower(value, qualifier)
        
    def UpdateAudioMute(self, value, qualifier):
        self.UpdatePower(value, qualifier)
        
    def UpdateFreeze(self, value, qualifier):
        self.UpdatePower(value, qualifier)
        
    def UpdateInput(self, value, qualifier):
        self.UpdatePower(value, qualifier)
        
    def UpdateOnScreenDisplay(self, value, qualifier):
        self.UpdatePower(value, qualifier)
    
    def UpdateVideoMute (self, value, qualifier):
        self.UpdatePower(value, qualifier)
        
    def UpdatePower(self, value, qualifier):        

        PowerState = {
            0x04: 'On',
            0x00: 'Off',  
            0x06: 'Off',  
            0x0F: 'Off',  
            0x10: 'Off',  
            0x01: 'Warming Up',
            0x02: 'Warming Up',
            0x03: 'Warming Up',
            0x09: 'Warming Up',
            0x05: 'Cooling Down',
            0x07: 'Cooling Down'
        }

        FreezeState = {
            0x01: 'On',
            0x00: 'Off'
        }

        VideoMuteState = {
            0x01: 'On',
            0x00: 'Off'
        }

        AudioMuteState = {
            0x01: 'On',
            0x00: 'Off'
        }

        OnScreenDisplayState = {
            0x00: 'On',
            0x01: 'Off'
        }

        InputState = {
           b'\x01\x21': 'HDMI 1',
           b'\x02\x21': 'HDMI 2',
           b'\x01\x22': 'DisplayPort',
           b'\x01\x01': 'Computer',
           b'\x01\x27': 'HDBaseT',
        }        

        res = self.__UpdateHelper('Power', b'\x00\xBF\x00\x00\x01\x02\xC2', value, qualifier)
        if res:            
            try:
                value = PowerState[res[6]]
                self.WriteStatus('Power', value, None)
            except (KeyError, IndexError):
                self.Error(['Power: Invalid/Unexpected Response'])

            try:
                value = InputState[res[8:10]]
                self.WriteStatus('Input', value, None)
            except (KeyError, IndexError):
                self.Error(['Input: Invalid/Unexpected response'])

            try:
                value = FreezeState[res[14]]
                self.WriteStatus('Freeze', value, None)
            except (KeyError, IndexError):
                self.Error(['Freeze: Invalid/Unexpected Response'])

            try:
                value = VideoMuteState[res[11]]
                self.WriteStatus('VideoMute', value, None)
            except (KeyError, IndexError):
                self.Error(['Video Mute: Invalid/Unexpected Response'])

            try:
                value = AudioMuteState[res[12]]
                self.WriteStatus('AudioMute', value, None)
            except (KeyError, IndexError):
                self.Error(['Audio Mute: Invalid/Unexpected Response'])

            try:
                value = OnScreenDisplayState[res[13]]
                self.WriteStatus('OnScreenDisplay', value, None)
            except (KeyError, IndexError):
                self.Error(['On Screen Display: Invalid/Unexpected Response'])

           

    def SetShutter(self, value, qualifier):

        ValueStateValues = {
            'Open': b'\x02\x17\x00\x00\x00\x19',
            'Close': b'\x02\x16\x00\x00\x00\x18'
        }

        ShutterCmdString = ValueStateValues[value]
        self.__SetHelper('Shutter', ShutterCmdString, value, qualifier)

    def SetVideoMute(self, value, qualifier):

        ValueStateValues = {
            'On': b'\x02\x10\x00\x00\x00\x12',
            'Off': b'\x02\x11\x00\x00\x00\x13'
        }

        VideoMuteCmdString = ValueStateValues[value]
        self.__SetHelper('VideoMute', VideoMuteCmdString, value, qualifier)

    def SetVolume(self, value, qualifier):

        ValueConstraints = {
            'Min': 0,
            'Max': 31
        }

        if ValueConstraints['Min'] <= value <= ValueConstraints['Max']:
            CKS = 0x1D + value
            VolumeCmdString = pack('>11B', 0x03, 0x10, 0x00, 0x00, 0x05, 0x05, 0x00, 0x00, value, 0x00, CKS)
            self.__SetHelper('Volume', VolumeCmdString, value, qualifier)
        else:
            self.Discard('Invalid Command for SetVolume')

    def UpdateVolume(self, value, qualifier):

        res = self.__UpdateHelper('Volume', b'\x03\x05\x00\x00\x03\x05\x00\x00\x10', value, qualifier)
        if res:
            try:
                self.WriteStatus('Volume', int(res[12]), qualifier)
            except (ValueError, IndexError):
                self.Error(['Volume: Invalid/unexpected response'])

    def __CheckResponseForErrors(self, sourceCmdName, response):

        DEVICE_ERROR_CODES = {
            b'\x00\x00': 'The command cannot be recognized',
            b'\x00\x01': 'The command is not supported by the model in use',
            b'\x01\x00': 'The specified value is invalid',
            b'\x01\x01': 'The specified input terminal is invalid',
            b'\x01\x02': 'The specified language is invalid',
            b'\x02\x00': 'Memory allocation error',
            b'\x02\x02': 'Memory in use',
            b'\x02\x03': 'The specified value cannot be set',
            b'\x02\x04': 'Forced onscreen mute on',
            b'\x02\x06': 'Viewer error',
            b'\x02\x07': 'No signal',
            b'\x02\x08': 'A test pattern of filer is destroyed',
            b'\x02\x09': 'No PC card is inserted',
            b'\x02\x0A': 'Memory operation error',
            b'\x02\x0C': 'An entry list is displayed',
            b'\x02\x0D': 'The command cannot be accepted because the power is off',
            b'\x02\x0E': 'The command execution failed',
            b'\x02\x0F': 'There is no authority necessary for the operation',
            b'\x03\x00': 'The specified gain number is incorrect',
            b'\x03\x01': 'The specified gain is invalid',
            b'\x03\x02': 'Adjustment failed'
        }

        if response and response[0:1] in {b'\xA0', b'\xA1', b'\xA2', b'\xA3'}:
            errorstring = 'An error occurred: {}: {}.'.format(sourceCmdName, DEVICE_ERROR_CODES.get(response[5:7], 'Unknown error'))
            response = b''
            self.Error([errorstring])
        return response

    def __SetHelper(self, command, commandstring, value, qualifier):
        self.Debug = True

        if self.Unidirectional == 'True' or command == 'UserDefinedCommand':
            self.Send(commandstring)
            return ''
        else:
            res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliRex=self.SetDelim[command])
            if not res:
                self.Error(['{}: Invalid/Unexpected Response'.format(command)])
            else:
                res = self.__CheckResponseForErrors(command, res)

    def __UpdateHelper(self, command, commandstring, value, qualifier):

        if self.Unidirectional == 'True':
            self.Discard('Inappropriate Command ' + command)
            return ''
        else:
            if self.initializationChk:
                self.OnConnected()
                self.initializationChk = False

            self.counter = self.counter + 1
            if self.counter > self.connectionCounter and self.connectionFlag:
                self.OnDisconnected()
                
            res = self.SendAndWait(commandstring, self.DefaultResponseTimeout, deliRex=self.UpdateDelim[command])
            if not res:
                return ''
            else:
                return self.__CheckResponseForErrors(command, res)            

    def OnConnected(self):
        self.connectionFlag = True
        self.WriteStatus('ConnectionStatus', 'Connected')
        self.counter = 0

    def OnDisconnected(self):
        self.WriteStatus('ConnectionStatus', 'Disconnected')
        self.connectionFlag = False

    ######################################################    
    # RECOMMENDED not to modify the code below this point
    ######################################################

    # Send Control Commands
    def Set(self, command, value, qualifier=None):
        method = getattr(self, 'Set%s' % command, None)
        if method is not None and callable(method):
            method(value, qualifier)
        else:
            raise AttributeError(command + 'does not support Set.')


    # Send Update Commands
    def Update(self, command, qualifier=None):
        method = getattr(self, 'Update%s' % command, None)
        if method is not None and callable(method):
            method(None, qualifier)
        else:
            raise AttributeError(command + 'does not support Update.')

    # This method is to tie an specific command with a parameter to a call back method
    # when its value is updated. It sets how often the command will be query, if the command
    # have the update method.
    # If the command doesn't have the update feature then that command is only used for feedback 
    def SubscribeStatus(self, command, qualifier, callback):
        Command = self.Commands.get(command, None)
        if Command:
            if command not in self.Subscription:
                self.Subscription[command] = {'method':{}}
        
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
        
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        if Parameter in qualifier:
                            Method[qualifier[Parameter]] = {}
                            Method = Method[qualifier[Parameter]]
                        else:
                            return
        
            Method['callback'] = callback
            Method['qualifier'] = qualifier    
        else:
            raise KeyError('Invalid command for SubscribeStatus ' + command)

    # This method is to check the command with new status have a callback method then trigger the callback
    def NewStatus(self, command, value, qualifier):
        if command in self.Subscription :
            Subscribe = self.Subscription[command]
            Method = Subscribe['method']
            Command = self.Commands[command]
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Method = Method[qualifier[Parameter]]
                    except:
                        break
            if 'callback' in Method and Method['callback']:
                Method['callback'](command, value, qualifier)  

    # Save new status to the command
    def WriteStatus(self, command, value, qualifier=None):
        self.counter = 0
        if not self.connectionFlag:
            self.OnConnected()
        Command = self.Commands[command]
        Status = Command['Status']
        if qualifier:
            for Parameter in Command['Parameters']:
                try:
                    Status = Status[qualifier[Parameter]]
                except KeyError:
                    if Parameter in qualifier:
                        Status[qualifier[Parameter]] = {}
                        Status = Status[qualifier[Parameter]]
                    else:
                        return  
        try:
            if Status['Live'] != value:
                Status['Live'] = value
                self.NewStatus(command, value, qualifier)
        except:
            Status['Live'] = value
            self.NewStatus(command, value, qualifier)

    # Read the value from a command.
    def ReadStatus(self, command, qualifier=None):
        Command = self.Commands.get(command, None)
        if Command:
            Status = Command['Status']
            if qualifier:
                for Parameter in Command['Parameters']:
                    try:
                        Status = Status[qualifier[Parameter]]
                    except KeyError:
                        return None
            try:
                return Status['Live']
            except:
                return None
        else:
            raise KeyError('Invalid command for ReadStatus: ' + command)

class SerialClass(SerialInterface, DeviceClass):

    def __init__(self, Host, Port, Baud=38400, Data=8, Parity='None', Stop=1, FlowControl='Off', CharDelay=0, Mode='RS232', Model =None):
        SerialInterface.__init__(self, Host, Port, Baud, Data, Parity, Stop, FlowControl, CharDelay, Mode)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self)
        # Check if Model belongs to a subclass
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'Host Alias: {0}, Port: {1}'.format(self.Host.DeviceAlias, self.Port)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')
  
    def Discard(self, message):
        self.Error([message])

class SerialOverEthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Serial'
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'IP Address/Host: {0}:{1}'.format(self.Hostname, self.IPPort)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')
  
    def Discard(self, message):
        self.Error([message])

    def Disconnect(self):
        EthernetClientInterface.Disconnect(self)
        self.OnDisconnected()

class EthernetClass(EthernetClientInterface, DeviceClass):

    def __init__(self, GUIHost: 'GUIController', Hostname, IPPort, Protocol='TCP', ServicePort=0, Model=None):
        EthernetClientInterface.__init__(self, Hostname, IPPort, Protocol, ServicePort)
        self.ConnectionType = 'Ethernet'
        self.GUIHost = GUIHost
        DeviceClass.__init__(self) 
        # Check if Model belongs to a subclass       
        if len(self.Models) > 0:
            if Model not in self.Models: 
                print('Model mismatch')              
            else:
                self.Models[Model]()

    def Error(self, message):
        portInfo = 'IP Address/Host: {0}:{1}'.format(self.Hostname, self.IPPort)
        print('Module: {}'.format(__name__), portInfo, 'Error Message: {}'.format(message[0]), sep='\r\n')
  
    def Discard(self, message):
        self.Error([message])

    def Disconnect(self):
        EthernetClientInterface.Disconnect(self)
        self.OnDisconnected()


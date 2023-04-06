'''Copyright (c) 2014-2017 Extron Electronics. All rights reserved.'''
from services.parser import manifestMode as _ext3969ron__manifestMode

def Version():
    '''Return EUP version string in the form of <major>.<minor>.<revision>'''
    import sys
    return sys.modules['__main__'].EUP_VERSION

def Platform():
    '''Return Extron IPCP platform string, either Pro or Pro xi'''
    import sys
    return sys.modules['__main__'].EUP_PLATFORM

# Mapping of Interface type provided by GCP to hardware port type
IFCLASS_2_PORT = {
    'AVInterface'            : 'AVI',
    'CECOutputInterface'     : 'CEO',
    'CECInputInterface'      : 'CEI',
    'ContactInputInterface'  : 'CII',
    'ContactInterface'       : 'CII',
    'DigitalIOInterface'     : 'DIO',
    'DigitalInputInterface'  : 'DII',
    'FlexIOInterface'        : 'FIO',
    'IRInterface'            : 'IRI',
    'IRSerialInterface'      : 'IRS',
    'PoEInterface'           : 'POE',
    'RelayInterface'         : 'RLY',
    'SerialInterface'        : 'COM',
    'SwitchedPowerSupply'    : 'SPS',
    'SwitchedPowerInterface' : 'SPI',
    'SWPowerInterface'       : 'SPI',
    'SWACReceptacleInterface': 'SAC',
    'VolumeControlInterface' : 'VOL',
    'VolumeInterface'        : 'VOL',
    'CircuitBreakerInterface': 'CBR',
    'CircuitBreaker'         : 'CBR',
    'TallyInterface'         : 'TAL'
}

if _ext3969ron__manifestMode() == 'programmable':
    DIN = 'DII'
    IR  = 'IRI'          # workaroud as GCP could not pass IRI
else:
    DIN = 'DIO'
    IR  = 'IRS'

IFASSET_2_PORT = {
    'av_interface'       : 'AVI',
    'poeInjectors'       : 'POE',
    'comPorts'           : 'COM',
    'irSerialPorts'      : 'IRS',
    'irPorts'            :  IR,
    'irTxPorts'          :  IR,
    'relays'             : 'RLY',
    'contactInput'       : 'CII',
    'digitalIoPorts'     : 'DIO',
    'digitalInPorts'     :  DIN,
    'flexIoPorts'        : 'FIO',
    'switched12vDcSupply': 'SPS',
    'unswitchedDcSupply' : 'SPS',
    'switched12vDcPorts' : 'SPI',
    'volumeControl'      : 'VOL',
    'CircuitBreaker'     : 'CBR',
    'tallyPorts'         : 'TAL',
    'ciPorts'            : 'CII'
}

# Mapping of non data-driven ports to interface class
NON_DATA_PORTS = [
    'POE', 'RLY', 'CII', 'DIO', 'FIO', 'SPS', 'SPI', 'VOL', 'CBR', 'SAC'
]
import sys
import importlib
import importlib.abc

# custom loader is just a wrapper around the right init-function
class CythonPackageLoader(importlib.abc.Loader):
    def __init__(self, init_function):
        super(CythonPackageLoader, self).__init__()
        self.init_module = init_function

    def load_module(self, fullname):
        if fullname not in sys.modules:
            sys.modules[fullname] = self.init_module()

        return sys.modules[fullname]

# custom finder just maps the module name to init-function      
class CythonPackageMetaPathFinder(importlib.abc.MetaPathFinder):
    def __init__(self, init_dict):
        super(CythonPackageMetaPathFinder, self).__init__()
        self.init_dict=init_dict

    def find_module(self, fullname, path):
        try:
            return CythonPackageLoader(self.init_dict[fullname])
        except KeyError:
            return None

# injecting custom finder/loaders into sys.meta_path:

import extron_impl
def FileChanged_init():
	return extron_impl.FileChanged()

def DataCommon_init():
	return extron_impl.DataCommon()

def Events_init():
	return extron_impl.Events()

def UDPInterface_init():
	return extron_impl.UDPInterface()

def UIControl_init():
	return extron_impl.UIControl()

def ButtonObject_init():
	return extron_impl.ButtonObject()

def DigitalIOInterface_init():
	return extron_impl.DigitalIOInterface()

def LabelObject_init():
	return extron_impl.LabelObject()

def KnobObject_init():
	return extron_impl.KnobObject()

def SocketInterface_init():
	return extron_impl.SocketInterface()

def eBUSDevice_init():
	return extron_impl.eBUSDevice()

def Const_init():
	return extron_impl.Const()

def DigitalInputInterface_init():
	return extron_impl.DigitalInputInterface()

def PoEInterface_init():
	return extron_impl.PoEInterface()

def CECInterface_init():
	return extron_impl.CECInterface()

def FlexIOInterface_init():
	return extron_impl.FlexIOInterface()

def Video_init():
	return extron_impl.Video()

def RelayInterface_init():
	return extron_impl.RelayInterface()

def AVInterface_init():
	return extron_impl.AVInterface()

def NetServ_init():
	return extron_impl.NetServ()

def AnnotatorInterface_init():
	return extron_impl.AnnotatorInterface()

def SliderObject_init():
	return extron_impl.SliderObject()

def Device_init():
	return extron_impl.Device()

def IRInterface_init():
	return extron_impl.IRInterface()

def UIDevice_init():
	return extron_impl.UIDevice()

def tlpuicreator_init():
	return extron_impl.tlpuicreator()

def LevelObject_init():
	return extron_impl.LevelObject()

def TCPInterface_init():
	return extron_impl.TCPInterface()

def TallyInterface_init():
	return extron_impl.TallyInterface()

def IOInterface_init():
	return extron_impl.IOInterface()

def SwitchedACReceptacleInterface_init():
	return extron_impl.SwitchedACReceptacleInterface()

def VolumeControlInterface_init():
	return extron_impl.VolumeControlInterface()

def CircuitBreakerInterface_init():
	return extron_impl.CircuitBreakerInterface()

def Timer_init():
	return extron_impl.Timer()

def SerialRemote_init():
	return extron_impl.SerialRemote()

def DanteInterface_init():
	return extron_impl.DanteInterface()

def AdapterDevice_init():
	return extron_impl.AdapterDevice()

def ContactInputInterface_init():
	return extron_impl.ContactInputInterface()

def SerialInterface_init():
	return extron_impl.SerialInterface()

def SwitchedPowerSupply_init():
	return extron_impl.SwitchedPowerSupply()

def CodecConnect_init():
	return extron_impl.CodecConnect()

def SwitchedPowerInterface_init():
	return extron_impl.SwitchedPowerInterface()

init_dict={ "Extron.FileChanged" : FileChanged_init,
"Extron.DataCommon" : DataCommon_init,
"Extron.Events" : Events_init,
"Extron.UDPInterface" : UDPInterface_init,
"Extron.UIControl" : UIControl_init,
"Extron.ButtonObject" : ButtonObject_init,
"Extron.DigitalIOInterface" : DigitalIOInterface_init,
"Extron.LabelObject" : LabelObject_init,
"Extron.KnobObject" : KnobObject_init,
"Extron.SocketInterface" : SocketInterface_init,
"Extron.eBUSDevice" : eBUSDevice_init,
"Extron.Const" : Const_init,
"Extron.DigitalInputInterface" : DigitalInputInterface_init,
"Extron.PoEInterface" : PoEInterface_init,
"Extron.CECInterface" : CECInterface_init,
"Extron.FlexIOInterface" : FlexIOInterface_init,
"Extron.Video" : Video_init,
"Extron.RelayInterface" : RelayInterface_init,
"Extron.AVInterface" : AVInterface_init,
"Extron.NetServ" : NetServ_init,
"Extron.AnnotatorInterface" : AnnotatorInterface_init,
"Extron.SliderObject" : SliderObject_init,
"Extron.Device" : Device_init,
"Extron.IRInterface" : IRInterface_init,
"Extron.UIDevice" : UIDevice_init,
"Extron.tlpuicreator" : tlpuicreator_init,
"Extron.LevelObject" : LevelObject_init,
"Extron.TCPInterface" : TCPInterface_init,
"Extron.TallyInterface" : TallyInterface_init,
"Extron.IOInterface" : IOInterface_init,
"Extron.SwitchedACReceptacleInterface" : SwitchedACReceptacleInterface_init,
"Extron.VolumeControlInterface" : VolumeControlInterface_init,
"Extron.CircuitBreakerInterface" : CircuitBreakerInterface_init,
"Extron.Timer" : Timer_init,
"Extron.SerialRemote" : SerialRemote_init,
"Extron.DanteInterface" : DanteInterface_init,
"Extron.AdapterDevice" : AdapterDevice_init,
"Extron.ContactInputInterface" : ContactInputInterface_init,
"Extron.SerialInterface" : SerialInterface_init,
"Extron.SwitchedPowerSupply" : SwitchedPowerSupply_init,
"Extron.CodecConnect" : CodecConnect_init,
"Extron.SwitchedPowerInterface" : SwitchedPowerInterface_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


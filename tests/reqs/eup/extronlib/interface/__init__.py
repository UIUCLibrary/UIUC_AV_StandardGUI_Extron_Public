"""Copyright (c) 2014-2018. Extron Electronics. All rights reserved.

The package contains libraries for Extron hardware interfaces. 
"""

from Extron.TallyInterface import TallyInterface

__file__ = '/extronlib/interface/__init__.py'
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

import extronlib_impl
def EthernetServerInterfaceEx_init():
	m1 = extronlib_impl.EthernetServerInterfaceEx()
	r1 = m1.EthernetServerInterfaceEx
	return r1

def SPInterface_init():
	m1 = extronlib_impl.SPInterface()
	r1 = m1.SPInterface
	return r1

def DigitalIOInterface_init():
	m1 = extronlib_impl.DigitalIOInterface()
	r1 = m1.DigitalIOInterface
	return r1

def EthernetClientInterface_init():
	m1 = extronlib_impl.EthernetClientInterface()
	r1 = m1.EthernetClientInterface
	return r1

def DigitalInputInterface_init():
	m1 = extronlib_impl.DigitalInputInterface()
	r1 = m1.DigitalInputInterface
	return r1

def SWACReceptacleInterface_init():
	m1 = extronlib_impl.SWACReceptacleInterface()
	r1 = m1.SWACReceptacleInterface
	return r1

def PoEInterface_init():
	m1 = extronlib_impl.PoEInterface()
	r1 = m1.PoEInterface
	return r1

def CECInterface_init():
	m1 = extronlib_impl.CECInterface()
	r1 = m1.CECInterface
	return r1

def FlexIOInterface_init():
	m1 = extronlib_impl.FlexIOInterface()
	r1 = m1.FlexIOInterface
	return r1

def EthernetServerInterface_init():
	m1 = extronlib_impl.EthernetServerInterface()
	r1 = m1.EthernetServerInterface
	return r1

def RelayInterface_init():
	m1 = extronlib_impl.RelayInterface()
	r1 = m1.RelayInterface
	return r1

def AnnotatorInterface_init():
	m1 = extronlib_impl.AnnotatorInterface()
	r1 = m1.AnnotatorInterface
	return r1

def SWPowerInterface_init():
	m1 = extronlib_impl.SWPowerInterface()
	r1 = m1.SWPowerInterface
	return r1

def VolumeInterface_init():
	m1 = extronlib_impl.VolumeInterface()
	r1 = m1.VolumeInterface
	return r1

def IRInterface_init():
	m1 = extronlib_impl.IRInterface()
	r1 = m1.IRInterface
	return r1

def IRHelper_init():
	return extronlib_impl.IRHelper()

def CircuitBreakerInterface_init():
	m1 = extronlib_impl.CircuitBreakerInterface()
	r1 = m1.CircuitBreakerInterface
	return r1

def DanteInterface_init():
	m1 = extronlib_impl.DanteInterface()
	r1 = m1.DanteInterface
	return r1

def ContactInterface_init():
	m1 = extronlib_impl.ContactInterface()
	r1 = m1.ContactInterface
	return r1

def PARITY_NONE_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.PARITY_NONE
	return r1

def PARITY_EVEN_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.PARITY_EVEN
	return r1

def PARITY_ODD_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.PARITY_ODD
	return r1

def FLOW_CONTROL_OFF_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.FLOW_CONTROL_OFF
	return r1

def FLOW_CONTROL_HW_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.FLOW_CONTROL_HW
	return r1

def FLOW_CONTROL_SW_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.FLOW_CONTROL_SW
	return r1

def SerialInterface_init():
	m1 = extronlib_impl.SerialInterface()
	r1 = m1.SerialInterface
	return r1

def CalendarEvent_init():
	return extronlib_impl.CalendarEvent()

init_dict={ "extronlib.interface.EthernetServerInterfaceEx" : EthernetServerInterfaceEx_init,
"extronlib.interface.SPInterface" : SPInterface_init,
"extronlib.interface.DigitalIOInterface" : DigitalIOInterface_init,
"extronlib.interface.EthernetClientInterface" : EthernetClientInterface_init,
"extronlib.interface.DigitalInputInterface" : DigitalInputInterface_init,
"extronlib.interface.SWACReceptacleInterface" : SWACReceptacleInterface_init,
"extronlib.interface.PoEInterface" : PoEInterface_init,
"extronlib.interface.CECInterface" : CECInterface_init,
"extronlib.interface.FlexIOInterface" : FlexIOInterface_init,
"extronlib.interface.EthernetServerInterface" : EthernetServerInterface_init,
"extronlib.interface.RelayInterface" : RelayInterface_init,
"extronlib.interface.AnnotatorInterface" : AnnotatorInterface_init,
"extronlib.interface.SWPowerInterface" : SWPowerInterface_init,
"extronlib.interface.VolumeInterface" : VolumeInterface_init,
"extronlib.interface.IRInterface" : IRInterface_init,
"extronlib.IRHelper" : IRHelper_init,
"extronlib.interface.IRHelper" : IRHelper_init,
"extronlib.interface.CircuitBreakerInterface" : CircuitBreakerInterface_init,
"extronlib.interface.DanteInterface" : DanteInterface_init,
"extronlib.interface.ContactInterface" : ContactInterface_init,
"extronlib.interface.PARITY_NONE" : PARITY_NONE_init,
"extronlib.interface.PARITY_EVEN" : PARITY_EVEN_init,
"extronlib.interface.PARITY_ODD" : PARITY_ODD_init,
"extronlib.interface.FLOW_CONTROL_OFF" : FLOW_CONTROL_OFF_init,
"extronlib.interface.FLOW_CONTROL_HW" : FLOW_CONTROL_HW_init,
"extronlib.interface.FLOW_CONTROL_SW" : FLOW_CONTROL_SW_init,
"extronlib.interface.SerialInterface" : SerialInterface_init,
"extronlib.CalendarEvent" : CalendarEvent_init,
"extronlib.interface.CalendarEvent" : CalendarEvent_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


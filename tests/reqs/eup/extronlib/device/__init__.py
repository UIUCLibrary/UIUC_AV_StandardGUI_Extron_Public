#
# Copyright (c) 2014. Extron Electronics. All rights reserved.
#
"""The package contains library to interact with Extron Control Devices."""


__file__ = '/extronlib/device/__init__.py'
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
def eBUSDevice_init():
	m1 = extronlib_impl.eBUSDevice()
	r1 = m1.eBUSDevice
	return r1

def str2Multiplier_init():
	m1 = extronlib_impl.str2Multiplier()
	r1 = m1.str2Multiplier
	return r1

def ProcessorDevice_init():
	m1 = extronlib_impl.ProcessorDevice()
	r1 = m1.ProcessorDevice
	return r1

def UIDevice_init():
	m1 = extronlib_impl.UIDevice()
	r1 = m1.UIDevice
	return r1

def SPDevice_init():
	m1 = extronlib_impl.SPDevice()
	r1 = m1.SPDevice
	return r1

def AdapterDevice_init():
	m1 = extronlib_impl.AdapterDevice()
	r1 = m1.AdapterDevice
	return r1

init_dict={ "extronlib.device.eBUSDevice" : eBUSDevice_init,
"extronlib.device.str2Multiplier" : str2Multiplier_init,
"extronlib.device.ProcessorDevice" : ProcessorDevice_init,
"extronlib.device.UIDevice" : UIDevice_init,
"extronlib.device.SPDevice" : SPDevice_init,
"extronlib.device.AdapterDevice" : AdapterDevice_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


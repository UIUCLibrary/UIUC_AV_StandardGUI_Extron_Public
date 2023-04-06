#
# Copyright (c) 2014. Extron Electronics. All rights reserved.
# 
__file__ = '/extronlib/interface/utils/__init__.py'
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
def RoomSchedulingInterfaceListener_init():
	return extronlib_impl.RoomSchedulingInterfaceListener()

def IRHelper_impl_init():
	return extronlib_impl.IRHelper_impl()

def KeepAlive_init():
	return extronlib_impl.KeepAlive()

init_dict={ "extronlib.RoomSchedulingInterfaceListener" : RoomSchedulingInterfaceListener_init,
"extronlib.interface.RoomSchedulingInterfaceListener" : RoomSchedulingInterfaceListener_init,
"extronlib.interface.utils.RoomSchedulingInterfaceListener" : RoomSchedulingInterfaceListener_init,
"extronlib.IRHelper_impl" : IRHelper_impl_init,
"extronlib.interface.IRHelper_impl" : IRHelper_impl_init,
"extronlib.interface.utils.IRHelper_impl" : IRHelper_impl_init,
"extronlib.KeepAlive" : KeepAlive_init,
"extronlib.interface.KeepAlive" : KeepAlive_init,
"extronlib.interface.utils.KeepAlive" : KeepAlive_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


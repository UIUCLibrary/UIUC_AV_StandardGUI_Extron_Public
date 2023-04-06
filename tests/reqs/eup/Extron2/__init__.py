'''
Modules designed solely for Extron GCP software usage

    *When I see a bird that walks like a duck and swims like a duck and quacks 
    like a duck, I call that bird a duck.*    
    -- Wikipedia "Duck typing"

*Copyright (c) 2013. Extron Electronics. All rights reserved.*
'''

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

import extron2_impl
def AppDriver_init():
	return extron2_impl.AppDriver()

def IRDriver_init():
	return extron2_impl.IRDriver()

def HTTPDriver_init():
	return extron2_impl.HTTPDriver()

def CECDriver_init():
	return extron2_impl.CECDriver()

def AbstractDriver_init():
	return extron2_impl.AbstractDriver()

def Automation_init():
	return extron2_impl.Automation()

def XDriver_init():
	return extron2_impl.XDriver()

def BaseDriver_init():
	return extron2_impl.BaseDriver()

init_dict={ "Extron2.AppDriver" : AppDriver_init,
"Extron2.IRDriver" : IRDriver_init,
"Extron2.HTTPDriver" : HTTPDriver_init,
"Extron2.CECDriver" : CECDriver_init,
"Extron2.AbstractDriver" : AbstractDriver_init,
"Extron2.Automation" : Automation_init,
"Extron2.XDriver" : XDriver_init,
"Extron2.BaseDriver" : BaseDriver_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


#
# Copyright (c) 2015. Extron Electronics. All rights reserved.
#
"""The package defines classes for user interactive controls.

UI control object's states are retained and will be recovered in case the end 
points lose connection to the primary control processor.
"""
from Extron import UIControl as _ext3969ron__UIControl

from services import safe_delattr
safe_delattr(_ext3969ron__UIControl.UIControl, 'Enable')
safe_delattr(_ext3969ron__UIControl.UIControl, 'Disable')

__file__ = '/extronlib/ui/__init__.py'
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
def Level_init():
	m1 = extronlib_impl.Level()
	r1 = m1.Level
	return r1

def Knob_init():
	m1 = extronlib_impl.Knob()
	r1 = m1.Knob
	return r1

def Video_init():
	m1 = extronlib_impl.Video()
	r1 = m1.Video
	return r1

def Slider_init():
	m1 = extronlib_impl.Slider()
	r1 = m1.Slider
	return r1

def Label_init():
	m1 = extronlib_impl.Label()
	r1 = m1.Label
	return r1

def Button_init():
	m1 = extronlib_impl.Button()
	r1 = m1.Button
	return r1

init_dict={ "extronlib.ui.Level" : Level_init,
"extronlib.ui.Knob" : Knob_init,
"extronlib.ui.Video" : Video_init,
"extronlib.ui.Slider" : Slider_init,
"extronlib.ui.Label" : Label_init,
"extronlib.ui.Button" : Button_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


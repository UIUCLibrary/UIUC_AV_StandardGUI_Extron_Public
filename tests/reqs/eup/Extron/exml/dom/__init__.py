"""Extron wrapper of Python xml.dom package"""
from xml.dom import *

__file__ = '/extronlib/standard/exml/dom/__init__.py'
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
def minidom_init():
	return extron_impl.minidom()

def pulldom_init():
	return extron_impl.pulldom()

init_dict={ "Extron.minidom" : minidom_init,
"Extron.exml.minidom" : minidom_init,
"Extron.exml.dom.minidom" : minidom_init,
"Extron.pulldom" : pulldom_init,
"Extron.exml.pulldom" : pulldom_init,
"Extron.exml.dom.pulldom" : pulldom_init,
"extronlib.minidom" : minidom_init,
"extronlib.standard.minidom" : minidom_init,
"extronlib.standard.exml.minidom" : minidom_init,
"extronlib.standard.exml.dom.minidom" : minidom_init,
"extronlib.pulldom" : pulldom_init,
"extronlib.standard.pulldom" : pulldom_init,
"extronlib.standard.exml.pulldom" : pulldom_init,
"extronlib.standard.exml.dom.pulldom" : pulldom_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


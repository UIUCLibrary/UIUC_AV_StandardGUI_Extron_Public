"""This package is identical to Python standard library""" 
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
def expat_init():
	return extron_impl.expat()

init_dict={ "Extron.expat" : expat_init,
"Extron.exml.expat" : expat_init,
"Extron.exml.parsers.expat" : expat_init,
,
"extronlib.expat" : expat_init,
"extronlib.standard.expat" : expat_init,
"extronlib.standard.exml.expat" : expat_init,
"extronlib.standard.exml.parsers.expat" : expat_init,
}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


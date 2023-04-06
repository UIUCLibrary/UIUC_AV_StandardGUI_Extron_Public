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

import extron3_impl
def SysSrv_init():
	return extron3_impl.SysSrv()

def ExQueue_init():
	return extron3_impl.ExQueue()

def DataStorage_init():
	return extron3_impl.DataStorage()

init_dict={ "Extron3.SysSrv" : SysSrv_init,
"Extron3.ExQueue" : ExQueue_init,
"Extron3.DataStorage" : DataStorage_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


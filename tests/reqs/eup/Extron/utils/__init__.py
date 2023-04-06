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
def UIDevice_impl_init():
	return extron_impl.UIDevice_impl()

def EthernetClientInterface_init():
	return extron_impl.EthernetClientInterface()

def RegexMatch_init():
	return extron_impl.RegexMatch()

def KeepAlive_init():
	return extron_impl.KeepAlive()

init_dict={ "Extron.UIDevice_impl" : UIDevice_impl_init,
"Extron.utils.UIDevice_impl" : UIDevice_impl_init,
"Extron.EthernetClientInterface" : EthernetClientInterface_init,
"Extron.utils.EthernetClientInterface" : EthernetClientInterface_init,
"Extron.RegexMatch" : RegexMatch_init,
"Extron.utils.RegexMatch" : RegexMatch_init,
"Extron.KeepAlive" : KeepAlive_init,
"Extron.utils.KeepAlive" : KeepAlive_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


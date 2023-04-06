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
def NFSCalendar_init():
	return extron_impl.NFSCalendar()

def AdAstraCalendar_init():
	return extron_impl.AdAstraCalendar()

def EMSCalendar_init():
	return extron_impl.EMSCalendar()

def MSExchangeCalendar_init():
	return extron_impl.MSExchangeCalendar()

def TwentyFiveLiveCalendar_init():
	return extron_impl.TwentyFiveLiveCalendar()

def tlps_init():
	return extron_impl.tlps()

def GoogleCalendar_init():
	return extron_impl.GoogleCalendar()

init_dict={ "Extron.NFSCalendar" : NFSCalendar_init,
"Extron.Scheduler.NFSCalendar" : NFSCalendar_init,
"Extron.AdAstraCalendar" : AdAstraCalendar_init,
"Extron.Scheduler.AdAstraCalendar" : AdAstraCalendar_init,
"Extron.EMSCalendar" : EMSCalendar_init,
"Extron.Scheduler.EMSCalendar" : EMSCalendar_init,
"Extron.MSExchangeCalendar" : MSExchangeCalendar_init,
"Extron.Scheduler.MSExchangeCalendar" : MSExchangeCalendar_init,
"Extron.TwentyFiveLiveCalendar" : TwentyFiveLiveCalendar_init,
"Extron.Scheduler.TwentyFiveLiveCalendar" : TwentyFiveLiveCalendar_init,
"Extron.tlps" : tlps_init,
"Extron.Scheduler.tlps" : tlps_init,
"Extron.GoogleCalendar" : GoogleCalendar_init,
"Extron.Scheduler.GoogleCalendar" : GoogleCalendar_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


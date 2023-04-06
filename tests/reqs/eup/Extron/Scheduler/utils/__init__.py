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
def CalendarEventEMS_init():
	return extron_impl.CalendarEventEMS()

def O365TimeZone_init():
	return extron_impl.O365TimeZone()

def CalendarEventAdAstra_init():
	return extron_impl.CalendarEventAdAstra()

def utils_init():
	return extron_impl.utils()

def CalendarEventNFS_init():
	return extron_impl.CalendarEventNFS()

def Outlook365Event_init():
	return extron_impl.Outlook365Event()

def CalendarEvent365_init():
	return extron_impl.CalendarEvent365()

def Connection_init():
	return extron_impl.Connection()

def GenericData_init():
	return extron_impl.GenericData()

def CalendarEventGoogle_init():
	return extron_impl.CalendarEventGoogle()

def CalendarEventTwentyFiveLive_init():
	return extron_impl.CalendarEventTwentyFiveLive()

def CalendarEvent_init():
	return extron_impl.CalendarEvent()

init_dict={ "Extron.CalendarEventEMS" : CalendarEventEMS_init,
"Extron.Scheduler.CalendarEventEMS" : CalendarEventEMS_init,
"Extron.Scheduler.utils.CalendarEventEMS" : CalendarEventEMS_init,
"Extron.O365TimeZone" : O365TimeZone_init,
"Extron.Scheduler.O365TimeZone" : O365TimeZone_init,
"Extron.Scheduler.utils.O365TimeZone" : O365TimeZone_init,
"Extron.CalendarEventAdAstra" : CalendarEventAdAstra_init,
"Extron.Scheduler.CalendarEventAdAstra" : CalendarEventAdAstra_init,
"Extron.Scheduler.utils.CalendarEventAdAstra" : CalendarEventAdAstra_init,
"Extron.utils" : utils_init,
"Extron.Scheduler.utils" : utils_init,
"Extron.Scheduler.utils.utils" : utils_init,
"Extron.CalendarEventNFS" : CalendarEventNFS_init,
"Extron.Scheduler.CalendarEventNFS" : CalendarEventNFS_init,
"Extron.Scheduler.utils.CalendarEventNFS" : CalendarEventNFS_init,
"Extron.Outlook365Event" : Outlook365Event_init,
"Extron.Scheduler.Outlook365Event" : Outlook365Event_init,
"Extron.Scheduler.utils.Outlook365Event" : Outlook365Event_init,
"Extron.CalendarEvent365" : CalendarEvent365_init,
"Extron.Scheduler.CalendarEvent365" : CalendarEvent365_init,
"Extron.Scheduler.utils.CalendarEvent365" : CalendarEvent365_init,
"Extron.Connection" : Connection_init,
"Extron.Scheduler.Connection" : Connection_init,
"Extron.Scheduler.utils.Connection" : Connection_init,
"Extron.GenericData" : GenericData_init,
"Extron.Scheduler.GenericData" : GenericData_init,
"Extron.Scheduler.utils.GenericData" : GenericData_init,
"Extron.CalendarEventGoogle" : CalendarEventGoogle_init,
"Extron.Scheduler.CalendarEventGoogle" : CalendarEventGoogle_init,
"Extron.Scheduler.utils.CalendarEventGoogle" : CalendarEventGoogle_init,
"Extron.CalendarEventTwentyFiveLive" : CalendarEventTwentyFiveLive_init,
"Extron.Scheduler.CalendarEventTwentyFiveLive" : CalendarEventTwentyFiveLive_init,
"Extron.Scheduler.utils.CalendarEventTwentyFiveLive" : CalendarEventTwentyFiveLive_init,
"Extron.CalendarEvent" : CalendarEvent_init,
"Extron.Scheduler.CalendarEvent" : CalendarEvent_init,
"Extron.Scheduler.utils.CalendarEvent" : CalendarEvent_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


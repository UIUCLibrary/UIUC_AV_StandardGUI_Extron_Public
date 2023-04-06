"""Copyright (c) 2014. Extron Electronics. All rights reserved."""
from .Wait import Wait
from .Timer import Timer
from Extron2.BaseDriver import WakeOnLan
from Extron.NetServ import Email as _ext3969ron__Email
from Extron.NetServ import Ping as _ext3969ron__Ping
from Extron2.HTTPDriver import GetUnverifiedContext, GetSSLContext
import logging as _ext3969ron__logging


__file__ = '/extronlib/system/__init__.py'

def GetSystemUpTime():
    """Return system up time in seconds"""
    #
    # http://planzero.org/blog/2012/01/26/system_uptime_in_python,_a_better_way
    #
    with open('/proc/uptime', 'r') as f:
        return float(f.readline().split()[0])

class Email(_ext3969ron__Email):
    def __init__(self, smtpServer=None, port=None, username=None,
                 password=None, sslEnabled=None):
        super().__init__(smtpServer, port, username,
                              password, sslEnabled)

    @classmethod
    def mro(cls):
        raise NotImplementedError()

def Ping(hostname='127.0.0.1', count=5):
    return _ext3969ron__Ping(hostname, count)


def ProgramLog(Entry, Severity='error'):
    assert isinstance(Entry, str), 'Invalid Parameter: Entry must be a string'
    assert isinstance(Severity, str), 'Invalid Parameter: Severity must be a string'

    if Severity == 'error':
        _ext3969ron__logging.error(Entry)
    elif Severity == 'warning':
        _ext3969ron__logging.warning(Entry)
    elif Severity == 'info':
        _ext3969ron__logging.info(Entry)
    else:
        raise Exception('Invalid Parameter: Severity must be "error" or "warning" or "info"')

    print(Severity + ': ' + Entry, end='', flush=True)


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
def FileChanged_init():
	return extronlib_impl.FileChanged()

def Clock_init():
	m1 = extronlib_impl.Clock()
	r1 = m1.Clock
	return r1

def SaveProgramLog_init():
	m1 = extronlib_impl.SaveProgramLog()
	r1 = m1.SaveProgramLog
	return r1

def RestartSystem_init():
	m1 = extronlib_impl.RestartSystem()
	r1 = m1.RestartSystem
	return r1

def File_init():
	m1 = extronlib_impl.File()
	r1 = m1.File
	return r1

def RFile_init():
	m1 = extronlib_impl.File()
	r1 = m1.RFile
	return r1

def Persistent_init():
	m1 = extronlib_impl.Persistent()
	r1 = m1.Persistent
	return r1

def GetTimezoneList_init():
	m1 = extronlib_impl.SystemTime()
	r1 = m1.GetTimezoneList
	return r1

def SetTimeZone_init():
	m1 = extronlib_impl.SystemTime()
	r1 = m1.SetTimeZone
	return r1

def SetManualTime_init():
	m1 = extronlib_impl.SystemTime()
	r1 = m1.SetManualTime
	return r1

def GetCurrentTimezone_init():
	m1 = extronlib_impl.SystemTime()
	r1 = m1.GetCurrentTimezone
	return r1

def SetAutomaticTime_init():
	m1 = extronlib_impl.SystemTime()
	r1 = m1.SetAutomaticTime
	return r1

def MESet_init():
	m1 = extronlib_impl.MESet()
	r1 = m1.MESet
	return r1

def Debug_init():
	return extronlib_impl.Debug()

init_dict={ "extronlib.FileChanged" : FileChanged_init,
"extronlib.system.FileChanged" : FileChanged_init,
"extronlib.system.Clock" : Clock_init,
"extronlib.system.SaveProgramLog" : SaveProgramLog_init,
"extronlib.system.RestartSystem" : RestartSystem_init,
"extronlib.File" : File_init,
"extronlib.RFile" : RFile_init,
"extronlib.system.File" : File_init,
"extronlib.system.RFile" : RFile_init,
"extronlib.system.Persistent" : Persistent_init,
"extronlib.system.GetTimezoneList" : GetTimezoneList_init,
"extronlib.system.SetTimeZone" : SetTimeZone_init,
"extronlib.system.SetManualTime" : SetManualTime_init,
"extronlib.system.GetCurrentTimezone" : GetCurrentTimezone_init,
"extronlib.system.SetAutomaticTime" : SetAutomaticTime_init,
"extronlib.system.MESet" : MESet_init,
"extronlib.Debug" : Debug_init,
"extronlib.system.Debug" : Debug_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


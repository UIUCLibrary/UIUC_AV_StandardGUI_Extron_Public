from typing import Dict, Tuple, List, NamedTuple, Union, Callable
from datetime import datetime
import re
import os

## CLASS DEFINITIONS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Clock:
    WEEKDAYS = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
    def __init__(self, Times: List[str], Days: List[str]=None, Function=None) -> None:
        self.Days = Days
        self.Function = Function
        self.State = 'enabled'
        self.Times = Times
        
    def Disable(self) -> None:
        self.State = 'disabled'
        
    def Enable(self) -> None:
        self.State = 'enabled'
        
    def SetDays(self, Days: List[str]):
        self.Days = Days
        
    def SetTimes(self, Times: List[str]):
        self.Times = Times

class Email:
    def __init__(self, smtpServer: str=None, port: int=None, username: str=None, password: str=None, sslEnabled: bool=None) -> None:
        self._smtpServer = smtpServer
        self._port = port
        self._username = username
        self._password = password
        self._sslEnabled = sslEnabled
        self._to = None
        self._cc = None
        self._from = 'no-reply@extron.com'
        self._subject = ''
        
    def Receiver(self, receiver: List[str]=None, cc: bool=False) -> None:
        if not cc:
            self._to = receiver
        else:
            self._cc = receiver
            
    def SendMessage(self, msg: str) -> None:
        pass
    
    def Sender(self, sender: str) -> None:
        self._from = sender
    
    def Subject(self, subject: str) -> None:
        self._subject = subject

class File:
    _pathroot = './emulatedFileSystem/SFTP'
    _path = '/'
    
    def __init__(self, Filename: str, mode: str='r', encoding: str=None, newline: str=None) -> None:
        self.FileName = Filename
        
        re_str = r"[rwa]{1}\+?([bt]?)"
        re_match = re.match(re_str, mode)
        if not re_match:
            raise ValueError("Open mode is not a valid value")

        if re_match.group(1) == '':
            self._binary = False
            self._mode = '{m}t'.format(m=mode)
        elif re_match.group(1) == 'b':
            self._binary = True
            self._mode = mode
        else:
            self._binary = False
            self._mode = mode
        
        if encoding != None:
            self._enc = encoding
        else:
            self._enc = 'ascii'
        self._new_line = newline
        
        self._file_object = open('{path}{file}'.format(path=self._get_path(), file=self.FileName),
                  mode= self._mode,
                  encoding= self._enc,
                  newline= self._new_line)
        
    
    @classmethod
    def _get_path(cls) -> None:
        return cls._pathroot + cls._path
    
    @classmethod
    def ChangeDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        cls._path = path
    
    @classmethod
    def DeleteDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
        os.rmdir(cls._pathroot+path)
    
    @classmethod
    def DeleteFile(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
        os.remove(cls._pathroot+path)
    
    @classmethod
    def Exists(cls, path: str) -> bool:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
        fullpath = cls._pathroot+path
        #winpath = fullpath.replace('/','\\')
        #print(winpath)
        return os.path.exists(fullpath)
    
    @classmethod
    def GetCurrentDir(cls) -> str:
        return cls._path
    
    @classmethod
    def ListDir(cls, path: str=None) -> List[str]:
        if not path:
            path = cls._path
            
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        os.listdir(cls._pathroot+path)
    
    @classmethod
    def MakeDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        os.mkdir(cls._pathroot+path)
    
    @classmethod
    def RenameFile(cls, oldname, newname) -> None:
        os.rename(cls._get_path()+oldname, cls._get_path()+newname)
    
    def close(self) -> None:
        self._file_object.close()
    
    def read(self, size: int=-1) -> bytes:
        return self._file_object.read(size)
    
    def readline(self) -> bytes:
        return self._file_object.readline()
    
    def seek(self, offset, whence: int=0) -> None:
        if whence >= 0 and whence <= 2:
            self._file_object.seek(offset, whence)
        else:
            raise ValueError('Whence may only be 0, 1, or 2')
    
    def tell(self) -> int:
        return self._file_object.tell()
    
    def write(self, data: Union[str, bytes]) -> None:
        self._file_object.write(data)
    
    def writelines(self, seq: List[str]) -> None:
        self._file_object.writelines(seq)
        
class RFile:
    _pathroot = './emulatedFileSystem/SFTP'
    _path = '/'
    
    def __init__(self, Filename: str, mode: str='r', encoding: str=None, newline: str=None) -> None:
        self.FileName = Filename
        
        re_str = r"[rwa]{1}\+?[bt]?"
        re_match = re.match(re_str, mode)
        if not re_match:
            raise ValueError("Open mode is not a valid value")
        if re_match.group(1) == '':
            self._binary = False
            self._mode = '{m}t'
        elif re_match.group(1) == 'b':
            self._binary = True
            self._mode = mode
        else:
            self._binary = False
            self._mode = mode
        
        if encoding != None:
            self._enc = encoding
        else:
            self._enc = 'ascii'
        self._new_line = newline
        
        with open('{path}{file}'.format(path=self._get_path(), file=self.FileName),
                  mode= self._mode,
                  encoding= self._enc,
                  newline= self._new_line) as f:
            self._file_object = f
        
    
    @classmethod
    def _get_path(cls) -> None:
        return cls._pathroot + cls._path
    
    @classmethod
    def ChangeDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        cls._path = path
    
    @classmethod
    def DeleteDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
        os.rmdir(cls._pathroot+path)
    
    @classmethod
    def DeleteFile(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
        os.remove(cls._pathroot+path)
    
    @classmethod
    def Exists(cls, path: str) -> bool:
        os.path.exists(cls._pathroot+path)
    
    @classmethod
    def GetCurrentDir(cls) -> str:
        return cls._path
    
    @classmethod
    def ListDir(cls, path: str=None) -> List[str]:
        if not path:
            path = cls._path
            
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        os.listdir(cls._pathroot+path)
    
    @classmethod
    def MakeDir(cls, path: str) -> None:
        if not path.startswith('/'):
            path = '/{p}'.format(p = path)
            
        if not path.endswith('/'):
            path = '{p}/'.format(p = path)
            
        os.mkdir(cls._pathroot+path)
    
    @classmethod
    def RenameFile(cls, oldname, newname) -> None:
        os.rename(cls._get_path()+oldname, cls._get_path()+newname)
    
    def close(self) -> None:
        self._file_object.close()
    
    def read(self, size: int=-1) -> bytes:
        return self._file_object.read(size)
    
    def readline(self) -> bytes:
        return self._file_object.readline()
    
    def seek(self, offset, whence: int=0) -> None:
        if whence >= 0 and whence <= 2:
            self._file_object.seek(offset, whence)
        else:
            raise ValueError('Whence may only be 0, 1, or 2')
    
    def tell(self) -> int:
        return self._file_object.tell()
    
    def write(self, data: Union[str, bytes]) -> None:
        self._file_object.write(data)
    
    def writelines(self, seq: List[str]) -> None:
        self._file_object.writelines(seq)
        
class MESet:
    def __init__(self, Objects: List) -> None: # TODO: update Objects list subtype
        self.Objects = Objects
        self._activeIndex = 0
        self._states = []
        for o in self.Objects:
            self._states.append([0,1])

    def Append(self, obj) -> None: # TODO: update obj type
        self.Objects.append(obj)
        self._states.append([0, 1])
        
    def GetCurrent(self): # TODO: Update return type
        return self.Objects[self._activeIndex]
    
    def Remove(self, obj) -> None: # TODO: update obj type
        if type(obj) == 'int':
            self.Objects.pop(obj)
            self._states.pop(obj)
        else:
            index = self.Objects.index(obj)
            self.Objects.remove(obj)
            self._states.pop(index)
        
    def SetCurrent(self, obj) -> None: # TODO: update obj type
        if type(obj) == 'int':
            self._activeIndex = obj
        else:
            self._activeIndex = self.Objects.index(obj)
        
    def SetStates(self, obj, offState: int, onState: int) -> None: # TODO: update obj type
        if type(obj) == 'int':
            self._states[obj][0] = offState
            self._states[obj][1] = onState
        else:
            index = self.Objects.index(obj)
            self._states[index][0] = offState
            self._states[index][1] = onState

class Timer:
    def __init__(self, Interval: float, Function: Callable=None) -> None:
        # TODO: figure out if this decorator definition works in a class
        def timer_wrapper(func=self.Function):
            func(Timer = self, Count = self.Count)
        
        self.Count = 0
        self.Function = Function
        self.Interval = Interval
        self.State = 'Running'
        
        ## Untracked Events
        # StateChanged
        
    def Change(self, Interval: float) -> None:
        self.Interval = Interval
        
    def Pause(self) -> None:
        self.State = 'Paused'
        
    def Restart(self) -> None:
        self.State = 'Running'
        self.Count = 0
        
    def Resume(self) -> None:
        self.State = 'Running'
        
    def Stop(self) -> None:
        self.State = 'Stopped'
        self.Count = 0

class Wait:
    def __init__(self, Time: float, Function: Callable=None) -> None:
        # TODO: figure out if this decorator definition works in a class
        def wait_wrapper(func=self.Function):
            func(Time = self.Time, Count = self.Count)
            
        self.Function = Function
        self.Time = Time
        self._currentTime = Time
        
    def Add(self, Time: float) -> None:
        self._currentTime = self._currentTime + Time
        
    def Cancel(self) -> None:
        self._currentTime = 0
        
    def Change(self, Time: float) -> None:
        self.Time = Time
        
    def Restart(self) -> None:
        self._currentTime = self.Time
    
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##
## SSL METHODS -----------------------------------------------------------------
import ssl

def GetUnverifiedContext() -> ssl.SSLContext:
    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_OPTIONAL
    context.load_default_certs()
    return context

def GetSSLContext(alias: str) -> ssl.SSLContext:
    context = ssl.SSLContext()
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_default_certs()
    
    certs = context.get_ca_certs()
    for c in certs:
        if alias == c['subject'][1][0][1]:
            return context
    raise Exception('CA Cert Alias not found')

## -----------------------------------------------------------------------------
##
## TIME METHODS ----------------------------------------------------------------
from collections import namedtuple
_ntp_server = ''
_TZTuple = namedtuple('_TZTuple', ['id', 'description', 'MSid'])
# TODO: verify the formatting of the timezone entries
_tz = _TZTuple('CST','Central Standard Time (US & Canada)','Central Standard Time')
_tz_list = \
    [
        _TZTuple('EST','Eastern Standard Time (US & Canada)','Eastern Standard Time'),
        _TZTuple('CST','Central Standard Time (US & Canada)','Central Standard Time'),
        _TZTuple('MST','Mountian Standard Time (US & Canada)','Mountain Standard Time'),
        _TZTuple('PST','Pacific Standard Time (US & Canada)','Pacific Standard Time')
    ]

_system_time = datetime.now() # add a timezone to this

def SetAutomaticTime(Server: str) -> None:
    _ntp_server = Server
    
def SetManualTime(DateAndTime: datetime) -> None:
    _system_time = DateAndTime
    
def GetCurrentTimezone() -> NamedTuple:
    return _tz

def GetTimezoneList() -> List[NamedTuple]:
    return _tz_list

def SetTimeZone(id: str) -> None:
    for tz in _tz_list:
        if id == tz.id:
            _tz = tz
            return None
    raise LookupError('Timezone with id ({}) not found in available Timezones list'.format(id))

## -----------------------------------------------------------------------------
##
## NETWORK METHODS -------------------------------------------------------------
import subprocess

def Ping(hostname: str='localhost', count: int=5) -> Tuple[int, int, float]:
    ping = subprocess.getoutput('ping -n {c} {h}'.format(c = count, h = hostname))
    # successes, # failure, avg time
    reSucc = r"Received = (\d+)"
    re_match_Succ = re.match(reSucc, ping)
    Succ = int(re_match_Succ.group(1))
    reFail = r"Lost = (\d+)"
    re_match_Fail = re.match(reFail, ping)
    Fail = int(re_match_Fail.group(1))
    reAvg = r"Average = (\d+)ms"
    re_match_Avg = re.match(reAvg, ping)
    Avg = float(re_match_Avg.group(1))
    return (Succ, Fail, Avg)
    
import struct, socket
def WakeOnLan(macAddress: str, port: int=9) -> None:
    # Construct 6 byte hardware address
    add_oct = macAddress.split('-') # extronlib expects "-" separators
    if len(add_oct) != 6:
        raise ValueError("MAC Address must be provided in six groups of two hex digits, separated by hyphens ('01-23-45-67-ab-cd', e.g.)")
    hwa = struct.pack('BBBBBB', int(add_oct[0],16),
        int(add_oct[1],16),
        int(add_oct[2],16),
        int(add_oct[3],16),
        int(add_oct[4],16),
        int(add_oct[5],16))

    # Build magic packet

    msg = '\xff' * 6 + hwa * 16

    # Send packet to broadcast address using UDP port 9 or provided port

    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast = ['127.0.0.1']
    for i in broadcast:
        soc.sendto(msg,(i,port))
    soc.close()

## -----------------------------------------------------------------------------
##
## OTHER METHODS ---------------------------------------------------------------

def GetSystemUpTime() -> float:
    return 1867.2022

_ProgramLog = ''
def ProgramLog(Entry: str, Severity: str = 'error') -> None:
    global _ProgramLog
    
    dt = datetime.now()
    if Severity == 'error':
        _ProgramLog += '[{t}] ERROR - {e}\n'.format(t = dt.isoformat(), e=Entry)
    elif Severity == 'warning':
        _ProgramLog += '[{t}] WARNING - {e}\n'.format(t = dt.isoformat(), e=Entry)
    elif Severity == 'info':
        _ProgramLog += '[{t}] INFO - {e}\n'.format(t = dt.isoformat(), e=Entry)
    else:
        raise ValueError("Severity must be either 'error', 'warning', or 'info'")

def SaveProgramLog(path: Union[File, str]=None) -> None:
    if path == None:
        dt = datetime.now()
        path = 'ProgramLog {year}-{month}-{day} {hr}{min}{sec}.txt'.format(
            year = dt.year,
            month = dt.month,
            day = dt.day,
            hr = str(dt.hour).zfill(2),
            min = str(dt.minute).zfill(2),
            sec = str(dt.second).zfill(2)
        )
    
    if type(path) == 'str':
        f = File(path, 'w')
        f.write(_ProgramLog)
        f.close()
    else:
        path.write(_ProgramLog)
        

def RestartSystem() -> None:
    pass

## -----------------------------------------------------------------------------


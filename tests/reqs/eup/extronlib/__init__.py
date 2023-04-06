"""Copyright (c) 2014. Extron Electronics. All rights reserved."""
import re
import inspect as _ext3969ron__inspect
from Extron import Events as _ext3969ron__Events
from Extron import Version, Platform
import logging as _ext3969ron__logging

__file__ = '/extronlib/__init__.py'

class GenericMixIn:
    @property
    def Error(self):
        return self.getEventHandler(_ext3969ron__Events.EVT_ERROR)

    @Error.setter
    def Error(self, handler):
        self.setEventHandler(handler, _ext3969ron__Events.EVT_ERROR)
        
    @property
    def Online(self):
        '''
        Online - fires when port goes online 
        '''
        return self.getEventHandler(_ext3969ron__Events.EVT_ONLINE)

    @Online.setter
    def Online(self, handler):   
        '''
        Online - fires when port goes online 
        '''
        self.setEventHandler(handler, _ext3969ron__Events.EVT_ONLINE)

    @property
    def Offline(self):
        '''
        Offline - fires when port goes offline
        '''
        return self.getEventHandler(_ext3969ron__Events.EVT_OFFLINE)

    @Offline.setter
    def Offline(self, handler):
        '''
        Offline - fires when port goes offline
        '''
        self.setEventHandler(handler, _ext3969ron__Events.EVT_OFFLINE)


def event(Object, EventName):
    """event decorator
    Decorate a function to make it the handler for *Object* when *EventName*
    happens 
    The decorated function must have exact signature as specified by the 
    definition of EventName, which must appear in the Object class or
    one of its parent classes. Lists of Objects and/or events can be passed
    in to apply the same handler to multiple events.

    : Parameters:
    : Object(object or list of objects) - An objct or list of objects whose class
                    or one of its/their parent classes defines EventName
    : EventName(string or list of strings) - name of an event or list of events

    """
    #
    # Refer to the links on how to use decorators
    # https://docs.python.org/3.3/howto/descriptor.html
    # http://thecodeship.com/patterns/guide-to-python-function-decorators/
    #
    if type(Object) is not list:
        ObjectList = [Object]
    else:
        ObjectList = Object[:]

    t = type(EventName) 
    if t is str:
        EventList = [EventName]
    elif t is not list:
        raise AttributeError(EventName, 'should be string type or list of strings')
    else:
        EventList = EventName[:]

    for e in EventList:
        assert isinstance(e, str), 'AttributeError: EventName must be a string'

    # In order to use event decorator, Object, or one of its base class must 
    # declare a property under EventName and it must be a data descriptor 
    # (implement getter and setter).

    # Create a decorator on-the-fly
    def decorator(func):
        # Assign function by calling descriptor directly
        for object in ObjectList:
            for event in EventList:
                bases = _ext3969ron__inspect.getmro(type(object))    
                for cls in bases:
                    if event in cls.__dict__:
                        a = cls.__dict__[event]
                        if not isinstance(a, property):
                            raise AttributeError("'" + type(object).__name__ + "' does not support event construct")
                        a.__set__(object, func)
                        break       
                else:
                    raise AttributeError("'" + type(object).__name__ + "' object has no attribute '" + event + "'")

        def wrapper(*args, **kwds):
            return func(*args, **kwds)
        return wrapper
    return decorator



def cleanErrLog(errLog):
    if not isinstance(errLog,str):
        errLog = str(errLog)

    try:
        newLog = re.sub(r'\(.*?\)','', errLog) # remove (...)
        errLog = re.sub(r'\[.*?\]','', newLog) # remove [...]

        #clear the error log as it was passed from open-ssl
        errLog = errLog.split( )
        for n, e in enumerate(errLog):
            tmp = e.lower()
            if ".c" in tmp:
                errLog[n] = tmp.replace(e, '')
            if "sslv" in tmp:
                errLog[n] = tmp.replace('sslv', '')
            if "unknown" in tmp:
                errLog[n] = tmp.replace('unknown', 'SSL')

        errLog = ' '.join(errLog)
    except Exception as e:
        _ext3969ron__logging.error(str(e))

    return errLog



# This is a dummy module for unit testing extron control script code files

## METHOD DEFINITIONS ----------------------------------------------------------

def event(obj, EventName):
    def event_wrapper(func):
        func(obj, EventName)
    return event_wrapper

def Version() -> str:
    return "1.3r8"

def Platform() -> str:
    return "Pro xi"

## -----------------------------------------------------------------------------
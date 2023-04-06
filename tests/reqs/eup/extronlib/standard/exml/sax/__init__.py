"""Extron wrapper of xml.sax package"""

__all__ = ['parse', 'parseString', 'make_parser',
           'SAXException', 'SAXNotRecognizedException', 'SAXParseException', 
           'SAXNotSufpportedException', 'SAXReaderNotAvailable']

from xml.sax.xmlreader import InputSource
from xml.sax.handler import ContentHandler, ErrorHandler
from xml.sax._exceptions import SAXException, SAXNotRecognizedException, \
                                SAXParseException, SAXNotSupportedException, \
                                SAXReaderNotAvailable

__file__ = '/extronlib/standard/exml/sax/__init__.py'

def parse(source, handler, errorHandler=ErrorHandler()):
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)
    parser.parse(source)

def parseString(string, handler, errorHandler=ErrorHandler()):
    from io import BytesIO

    if errorHandler is None:
        errorHandler = ErrorHandler()
    parser = make_parser()
    parser.setContentHandler(handler)
    parser.setErrorHandler(errorHandler)

    inpsrc = InputSource()
    inpsrc.setByteStream(BytesIO(string))
    parser.parse(inpsrc)

# this is the parser list used by the make_parser function if no
# alternatives are given as parameters to the function
default_parser_list = ["Extron.exml.sax.expatreader"]

def make_parser(parser_list = []):
    """Creates and returns a SAX parser.

    Creates the first parser it is able to instantiate of the ones
    given in the list created by doing parser_list +
    default_parser_list.  The lists must contain the names of Python
    modules containing both a SAX parser and a create_parser function."""

    for parser_name in parser_list + default_parser_list:
        try:
            drv_module = __import__(parser_name,{},{},['create_parser'])
            return drv_module.create_parser()
        except ImportError as e:
            import sys
            if parser_name in sys.modules:
                # The parser module was found, but importing it
                # failed unexpectedly, pass this exception through
                raise
        except SAXReaderNotAvailable:
            # The parser module detected that it won't work properly,
            # so try the next one
            pass

    raise SAXReaderNotAvailable("No parsers found", None)
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
def xmlreader_init():
	return extron_impl.xmlreader()

def handler_init():
	return extron_impl.handler()

def expatreader_init():
	return extron_impl.expatreader()

def saxutils_init():
	return extron_impl.saxutils()

init_dict={ "Extron.xmlreader" : xmlreader_init,
"Extron.exml.xmlreader" : xmlreader_init,
"Extron.exml.sax.xmlreader" : xmlreader_init,
"Extron.handler" : handler_init,
"Extron.exml.handler" : handler_init,
"Extron.exml.sax.handler" : handler_init,
"Extron.expatreader" : expatreader_init,
"Extron.exml.expatreader" : expatreader_init,
"Extron.exml.sax.expatreader" : expatreader_init,
"Extron.saxutils" : saxutils_init,
"Extron.exml.saxutils" : saxutils_init,
"Extron.exml.sax.saxutils" : saxutils_init,
"extronlib.xmlreader" : xmlreader_init,
"extronlib.standard.xmlreader" : xmlreader_init,
"extronlib.standard.exml.xmlreader" : xmlreader_init,
"extronlib.standard.exml.sax.xmlreader" : xmlreader_init,
"extronlib.handler" : handler_init,
"extronlib.standard.handler" : handler_init,
"extronlib.standard.exml.handler" : handler_init,
"extronlib.standard.exml.sax.handler" : handler_init,
"extronlib.expatreader" : expatreader_init,
"extronlib.standard.expatreader" : expatreader_init,
"extronlib.standard.exml.expatreader" : expatreader_init,
"extronlib.standard.exml.sax.expatreader" : expatreader_init,
"extronlib.saxutils" : saxutils_init,
"extronlib.standard.saxutils" : saxutils_init,
"extronlib.standard.exml.saxutils" : saxutils_init,
"extronlib.standard.exml.sax.saxutils" : saxutils_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


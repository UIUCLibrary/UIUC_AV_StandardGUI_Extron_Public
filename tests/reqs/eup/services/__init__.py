#
# Copyright (c) 2012. Extron Electronics. All rights reserved.
#ssssss
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

import services_impl
def queue2_init():
	return services_impl.queue2()

def Eupd_init():
	return services_impl.Eupd()

def Extronrpdb2_init():
	return services_impl.Extronrpdb2()

def Trace_init():
	return services_impl.Trace()

def EndUserPrograms_impl_init():
	return services_impl.EndUserPrograms_impl()

def Threads_init():
	return services_impl.Threads()

def RIPC_client_init():
	return services_impl.RIPC_client()

def parser_init():
	return services_impl.parser()

def Const_init():
	return services_impl.Const()

def RPC_service_init():
	return services_impl.RPC_service()

def Logger_init():
	return services_impl.Logger()

def ExtronPdb_init():
	return services_impl.ExtronPdb()

def TimerService_init():
	return services_impl.TimerService()

def _ximport_init():
	return services_impl._ximport()

def WaitService_init():
	return services_impl.WaitService()

def PortListener_init():
	return services_impl.PortListener()

def URI_init():
	return services_impl.URI()

def safe_delattr_init():
	m1 = services_impl.safe_delattr()
	r1 = m1.safe_delattr
	return r1

def DspcListener_init():
	return services_impl.DspcListener()

def MsgListener_init():
	return services_impl.MsgListener()

def FileParser_init():
	return services_impl.FileParser()

def Table_init():
	return services_impl.Table()

init_dict={ "services.queue2" : queue2_init,
"services.Eupd" : Eupd_init,
"services.Extronrpdb2" : Extronrpdb2_init,
"services.Trace" : Trace_init,
"services.EndUserPrograms_impl" : EndUserPrograms_impl_init,
"services.Threads" : Threads_init,
"services.RIPC_client" : RIPC_client_init,
"services.parser" : parser_init,
"services.Const" : Const_init,
"services.RPC_service" : RPC_service_init,
"services.Logger" : Logger_init,
"services.ExtronPdb" : ExtronPdb_init,
"services.TimerService" : TimerService_init,
"services._ximport" : _ximport_init,
"services.WaitService" : WaitService_init,
"services.PortListener" : PortListener_init,
"services.URI" : URI_init,
"services.safe_delattr" : safe_delattr_init,
"services.DspcListener" : DspcListener_init,
"services.MsgListener" : MsgListener_init,
"services.FileParser" : FileParser_init,
"services.Table" : Table_init}
sys.meta_path.append(CythonPackageMetaPathFinder(init_dict))


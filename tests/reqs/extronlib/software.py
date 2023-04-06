# This is a dummy module for unit testing extron control script code files

from typing import Dict, Tuple, List, Union

## CLASS DEFINITIONS +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class DanteDomainManager:
    def __init__(self, Hostname: str, Credentials: Tuple=None) -> None:
        """This class provides a re-usable Dante Domain Manager definition that can be supplied to a DanteInterface.

        Parameters: 
            Hostname (string) - IP address or DNS Hostname of the Dante Domain Manager.\n
            Credentials (tuple) - Username and password for connection.
        """
        self.Hostname = Hostname
        self.Credentials = Credentials
    
class SummitConnect:
    _default_ListeningPort = [10000, 10001, 10002, 10003, 10004, 10005, 10007, 10008, 10009, 10010, 10011, 10012, 10013, 10014]
    _available_ListeningPort = _default_ListeningPort
    _inuse_ListeningPort = []
    def __init__(self, Hostname: str, IPPort: int) -> None:
        """This class provides an interface to Extron Unified Communications solutions.

        Note - System limits 15 SummitConnect clients per system.

        Parameters: 
            Hostname (string) - Hostname of the host computer. Can be an IP Address.\n
            IPPort (int) - IP Port the software is listening on (default is 5000)
        
        Note - Only one object can be instantiated for a given Hostname or IP Address.
        """
        ## Untracked Events
        # Connected
        # Disconnected
        # ReceiveData
        
        self.Hostname = Hostname
        ## self.IPAddress TODO: get IP from hostname
        self.IPPort = IPPort
        self.ListeningPort = None
        for lp in self._available_ListeningPort:
            if lp not in self._inuse_ListeningPort:
                self.ListeningPort = lp
                self._inuse_ListeningPort.append(lp)
                break
        if not self.ListeningPort:
            raise Exception("No listening ports avaiable")
        self._connected = False
        
    @classmethod
    def SetListeningPorts(cls, portList: List=None) -> None:
        """Set the ports to listen for received data.

        Parameters: portList (list of ints) - list of ports (e.g. [10000, 10001, 10002]). None will set to default range.
        
        Returns: 'Listening' or a reason for failure (e.g. 'PortUnavailable:<port>, ...')
        """
        if not portList:
            cls._available_ListeningPort = cls._default_ListeningPort
        elif len(portList) <= 15:
            cls._available_ListeningPort = portList
        else:
            raise ValueError("Port list may contain a maximum of 15 values")
        
    def Connect(self, timeout: float=None) -> str:
        """Connect to the software

        Parameters: timeout (float) - time in seconds to attempt connection before giving up.
            Returns: 'Connected' or reason for failure ('TimedOut', 'HostError', 'PortUnavailable:<port>, ...').\n
            Return type: string
        """
        if self._connected:
            # return 'ConnectedAlready'
            return 'Connected'
        else:
            self._connected = True
            return 'Connected'
        
    def Disconnect(self) -> None:
        """Disconnect the socket"""
        self._connected = False
        
    def Send(self, data: Union[bytes, str]) -> None:
        """Send string to licensed software

        Parameters: data (bytes, string) - string to send out
        """
        pass
    
## +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import config
import PyDAQmx as daq
import ctypes as C
import time
from daqmx_threadsafe import Task
from .. import AbstractHardware
class NIPCI6602(AbstractHardware):
    """
    Class to handle National Instruments PCI-6602. 
    As PyDAQmx is mostly just a wrapper this doesn't 
    do very much due to the library having a poor OO 
    interface. Still required though

    Configuration requires:
    ==========================  ================== ========
    Key                         Description        Example
    ==========================  ================== ========
    normal hardware parameters  As seen in 
                                `AbstractHardware`
        
    path                        String path to     '/Dev1/'
                                device
    ==========================  ================== ========
    """
    code = "NIPCI6602"
    name = "Ni-Daq 8-channel counter"
    description = "PCI card"
    
    def __init__(self,path,ID,name=name,description=description):
        self._path = path
        self._name = name
        self._id = ID
        self._description = description

    @property
    def path(self):
        """
        Get path to device

        Returns
        -------
        str: path to device
        """
        return self._path
    
    def make_task(self):
        """
        Create a new task

        Returns 
        -------
        `daqmx_threadsafe.Task`
        """
        return Task()

    def disconnect(self):
        pass

    @classmethod
    def create(cls,configuration,data_handler):
        ID = configuration[config.ID]        
        d = configuration.get(config.DESCRIPTION,cls.description)
        n = configuration.get(config.NAME,cls.name)
        path = configuration['path']        
        
        #hardware._file.debug = True
        return NIPCI6602(path,ID,n,d)

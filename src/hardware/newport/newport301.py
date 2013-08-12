import config
import PyDAQmx as daq
import ctypes as C
import time

class NPPCI6602(AbstractHardware,NewportESP301):
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
    
    

    def disconnect(self):
        pass

    @classmethod
    def create(cls,configuration,data_handler):
        ID = configuration[config.ID]        
        d = configuration.get(config.DESCRIPTION,cls.description)
        n = configuration.get(config.NAME,cls.name)
        path = configuration['path']        
        
        #hardware._file.debug = True
        return hardware

                    








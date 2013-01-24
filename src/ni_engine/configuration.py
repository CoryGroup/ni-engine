#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# configuration.py: Stores configuration information for ni-engine.
##

## IMPORTS #####################################################################

import os
from itertools import count

from . import hardware

## FUNCTIONS ###################################################################

def type_name(typ):
    return typ.__module__ + "." + typ.__name__

## CLASSES #####################################################################

# We define the Configuration class differently under Windows and everything else.
if os.name == "nt":
    
    import _winreg
    
    BASE_KEY_NAME = r"Software\Corylab\NI Engine"
    
    def open_or_create(parent, key):
        try:
            return _winreg.OpenKey(parent, key, 0, _winreg.KEY_ALL_ACCESS)
        except:
            return _winreg.CreateKey(parent, key)
            
    def iter_subkeys(key):
        try:
            for idx in count():
                yield _winreg.EnumKey(key, idx)
        except WindowsError:
            # A WindowsError indicates we have run out of keys to enumerate.
            return
    
    def iter_values(key):
        try:
            for idx in count():
                yield _winreg.EnumValue(key, idx)
        except WindowsError:
            # A WindowsError indicates we have run out of values to enumerate.
            return
    
    class Configuration(object):
        def __init__(self):
            self.key = open_or_create(_winreg.HKEY_LOCAL_MACHINE, BASE_KEY_NAME)
                
        def _subkey_for_class(self, cls):
            return open_or_create(self.key, type_name(cls))
                
        def get_devices_by_class(self, device_class):
            subkey = open_or_create(self._subkey_for_class(device_class), r"known_devices")
            for val_name, val_data, val_type in iter_values(subkey):
                yield (val_name, val_data) # <- (Device description, device location)
                
        def add_device(self, device_class, device_description, device_location):
            subkey = open_or_create(self._subkey_for_class(device_class), r"known_devices")
            _winreg.SetValueEx(subkey, device_description, None, device_location)
        
else:
    
    import ConfigParser

    class Configuration(object):
        def __init__(self):
            # TODO: find the right INI-file.
            
        def get_devices_by_class(self, device_class):
            # TODO!
            pass
            
        def add_device(self, device_class, device_description, device_location):
            # TODO!
            pass


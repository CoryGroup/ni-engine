#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# configuration.py: Stores configuration information for ni-engine.
##

## IMPORTS #####################################################################

import os
import sys
from itertools import count

from . import hardware

## FUNCTIONS ###################################################################

def type_name(typ):
    return typ.__module__ + "." + typ.__name__
    
def ensuredir(filename):
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)

def preffilename():
    if sys.platform.startswith('linux') or sys.platform.startswith('darwin') or sys.platform.startswith('cygwin'):	    
        # Unix-y
        configfile = os.path.expanduser('~/.config/ni-engine.conf')
    elif sys.platform.startswith('win'):
        # Windows-y
        configfile = os.path.join(os.path.expandvars('%APPDATA%'), 'ni-engine.conf')
    else:
        return NotImplemented

    ensuredir(configfile)
    return configfile

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
            self.key = open_or_create(_winreg.HKEY_CURRENT_USER, BASE_KEY_NAME)
                
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
    
    PREF_FILE_NAME = preffilename()
    
    class Configuration(object):
        def __init__(self):
            # TODO: find the right INI-file.
            self.parser = ConfigParser.SafeConfigParser()
            self.parser.read(PREF_FILE_NAME)
            
        def __del__(self):
            self.flush()
            
        def flush(self):
            with open(PREF_FILE_NAME, 'w') as f:
                self.parser.write(f)
            
        def get_devices_by_class(self, device_class):
            section = "{}/known_devices".format(type_name(device_class))
            if self.parser.has_section(section):
                return iter(self.parser.items(section))
            else:
                return iter([])
            
        def add_device(self, device_class, device_description, device_location):
            section = "{}/known_devices".format(type_name(device_class))
            if not self.parser.has_section(section):
                self.parser.add_section(section)
            self.parser.set(section, device_description, device_location)
            self.flush()
            
            

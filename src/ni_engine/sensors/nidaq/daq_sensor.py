#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# daq_sensor.py: Sensor class for NI-DAQ devices, backed by the PyDAQmx library.
##
# Part of the NI Engine project.
##

## ALL #########################################################################

__all__ = [
    ## SINGLETONS ##
    'Continuous',
    ## CLASSES ##
    'DAQCounterSensor'
]

## IMPORTS #####################################################################

## NI Engine Imports ##
import ni_engine.config as config
from ..abstract_sensors import AbstractCounterSensor
from ni_engine.util_fns import assume_units
from ni_engine.storage import DataContainer, data
from ni_engine.hardware.nidaq import daqmx_threadsafe as daq

if daq is None:
    raise ImportError("Threadsafe DAQmx wrapper did not import properly.")

## Other Libraries ##
import quantities as pq
import time
## Standard Library Imports ##
from itertools import izip
import ctypes as C
import threading
import datetime

## Other Libraries ##
from flufl.enum import IntEnum

## GLOBALS #####################################################################

__daq_lock = threading.Lock()


## SINGLETONS ##################################################################

## METACLASS ##
# The following metaclass is borrowed from:
# http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
        
## SINGLETON CLASSES ##

class SingletonBase(object):    
    def __copy__(self): return self
    def __deepcopy__(self, memo): return self

class ContinuousType(SingletonBase):
    """
    Represents that a process that is to be repeated continuously.
    """
    __metaclass__ = Singleton
    
    def __repr__(self):
        return "Continuous"
    
Continuous = ContinuousType()

## CONSTANTS ##################################################################

#: Defines the default sample clock rate to use for gating pulses and other
#: such applications.
SAMPLE_CLOCK_RATE = pq.Quantity(10000.0, daq.samples / pq.s)

## CLASSES #####################################################################


class DAQCounterSensor(AbstractCounterSensor):
    """
    Sensor implementing communication with a NI-DAQ counter card or device.
    
    Parameters
    ----------
    ID : str
        TODO
    channels : list of `str`s
        DAQmx channel names for each channel to be counted from.
    gate_channel : str
        DAQmx channel name for a channel to use as a gate for the counter
        channels, or `None` to disable gating. Note that this channel should
        be *electrically* connected to the input gate lines for each of the
        counter input channels that is to be gated, as this cannot be done in
        software.
    gate_delay : pq.Quantity [default units: s]
        Time before the first pulse starts.
    gate_lowtime : pq.Quantity [default units: s]
        Time that the pulse is low (counting disabled) in each cycle.
    gate_hightime : pq.Quantity [default units: s]
        Time that the pulse is high (counting enabled) in each cycle.
    gate_repeat : int or Continuous
        Number of times to repeat the gate pulse each time the DAQ tasks are
        started, or Continuous to indicate that the gate pulses should repeat
        indefinitely.
    """
    
    ## NI ENGINE SPECIAL PROPERTIES ##
    code = 'DAQCOUNTER'
    name = 'NI-DAQ Counter'
    description = 'Sensor for NI-DAQ counting devices.'
    
    ## INITIALIZER ##
    def __init__(self, ID,hardware,
            channels=('/Dev1/ctr1',),
            gate_channel=None,
            gate_delay=pq.Quantity(0.0, "s"),
            gate_lowtime=pq.Quantity(0.1, "s"),
            gate_hightime=pq.Quantity(0.1, "s"),
            gate_repeat=1,count_time=pq.Quantity(1,'s'),
            name=name, description=description,max_stored_data=100
        ):
        self._id = ID 
        self._name = name
        self._description = description
        self._hardware = hardware
        self._channel_names = channels
        self._gate_channel = gate_channel
        self._gate_delay = gate_delay
        self._gate_hightime = gate_hightime
        self._gate_lowtime = gate_lowtime
        self._gate_repeat = gate_repeat
        self._name = name
        self._description = description
        self._max_stored_data = max_stored_data
        self._n_channels = len(self._channel_names)
        self._count_time = count_time
        super(AbstractCounterSensor,self).__init__() 

        
    ## TASK CREATION AND MANAGEMENT ##
    
    def __init_tasks(self):
        """
        Creates input and output tasks for each of the channels that will be
        counted or used as a gate.
        """
        # Do we need to gate?

        self._input_tasks = [self._hardware.make_task() for chan in self._channel_names]
        if self._gate_channel is not None:
            self._gate_task = self._hardware.make_task()

        for idx, (task, chan_name) in enumerate(izip(self._input_tasks, self._channel_names)):
            task.create_ci_count_edges_chan(
                chan_name, "ch{}".format(idx),
                daq.Edge.rising,
                pq.Quantity(0, pq.counts),
                daq.CountDirection.up
            )
        if self._gate_channel is not None:            
            self._gate_task.create_co_pulse_channel_time(
                    self._gate_channel,
                    "gate",
                    daq.DigitalLevel.low,
                    self._gate_delay,
                    self._gate_lowtime,
                    self._gate_hightime
                )

            # We want to make the pulse repeat indefinitely or for a finite
            # number of samples, depending on the value of self._gate_repeat.
            # That only works if the timing type is Implicit for some reason.
            
            if self._gate_repeat is Continuous:
            
                args = (daq.SampleMode.continuous_samples, 0)
            else:
                args = (daq.SampleMode.finite_samples, self._gate_repeat)

            self._gate_task.config_sample_clock_timing(
                "OnboardClock", SAMPLE_CLOCK_RATE, daq.Edge.rising,
                *args
            )
            self._gate_task.sample_timing_type = daq.SampleTimingType.implicit
            
        # OK, now create the input tasks.
        for idx, (task, chan_name) in enumerate(izip(self._input_tasks, self._channel_names)):
            # Do we need to gate the channel?
            if self._gate_channel is not None:
                # TODO: make an enum for this and move into Task().
                task.pause_trigger_type = daq.PauseTriggerType.digital_level
                assert task.pause_trigger_type == daq.PauseTriggerType.digital_level, \
                    "Pause trigger type for channel {} not changed!".format(chan_name)
                task.diglvl_pause_trigger_when = daq.DigitalLevel.low
            
    def __start_tasks(self):
        # TODO: add error handling so that as many tasks as possible are
        #       started.
        
        # We want to make sure that the inputs start *before* the gate.
        # This allows us to work around the limit of not having a software
        # trigger.
        for chan_task in self._input_tasks:
            chan_task.start()
            
        if self._gate_channel is not None:
            self._gate_task.start()
            
    def __stop_tasks(self):
        # We need to do things in the opposite order of __start_tasks, so
        # first, stop the gate pulses.
        if self._gate_channel is not None:
            self._gate_task.stop()
            
        for chan_task in self._input_tasks:
            chan_task.stop()
        
    ## SENSOR CONTRACT ##
        
    def connect(self):
        """
        Called to connect NI-6602 channels
        """
        self.__init_tasks()
        
    def disconnect(self):
        # TODO: write the __destroy_tasks method.
        self.__destroy_tasks()
        
    def delete(self):
        try:
            self.disconnect()
        finally:
            del self
        
    def measure(self):
        """
        Get a measurement from the device, consisting of a count from each of
        the channels.

        Returns
        -------
        measurement : DataContainer
        """
        # TODO: write this method.
        #       Roughly, need to stop the gate, read the inputs, stop the inputs,
        #       then restart the inputs and restart the inputs.
        # Tasks now support context manager protocols.
        con = DataContainer(self.id,self._max_stored_data)
        self.__start_tasks()
        if self._gate_repeat is not Continuous and self._gate_channel is not None:        
            self._gate_task.wait_until_done((self._gate_hightime+self._gate_lowtime)+self._gate_delay+pq.Quantity(1,'s'))
        else : 
            time.sleep(self._count_time)
        if self._gate_channel is not None:
            self._gate_task.stop()
        #store same time for all measurements
        now = datetime.datetime.now()
        quantities = []
        for task in self._input_tasks:
            #generate list of counts
            quantities.append(task.counter_value)       
            task.stop()
        #store counts in DataQuantity
        q = pq.Quantity(quantities,'counts')            
        con[self.id+" channel counts"] = data(self.id,self.code,self.id+" channel counts",q,now)        
        return con  
    
    @property
    def n_channels(self):
        """
        Returns
        -------
        n_channels : int
            Number of channels admitted by this sensor.
        """
        return self._n_channels

    @property
    def threadsafe(self):
        """
        Must be overwritten to be made true. 
        If is threadsafe return True and can 
        be used with futures.
        Returns
        -------
        bool
        """
        return True
    

    @classmethod 
    def create(cls,configuration,data_handler,hardware):
        """
        Create method called by sensor manager

        """
        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        path = hardware.path        
        channels = map(lambda x: path+x,configuration.get("channels",('ctr1',)))
        max_stored_data = configuration.get(config.MAX_DATA)
        count_time = pq.Quantity(configuration.get('count_time',1),"s")
        if 'gate' in configuration:
            gate_configuration = configuration['gate']
            gate_channel_name = path+gate_configuration['channel_name']            
            gate_delay = pq.Quantity(gate_configuration['delay'],'s')
            gate_hightime = pq.Quantity(gate_configuration['hightime'],'s')
            gate_lowtime = pq.Quantity(gate_configuration['lowtime'],'s')
            gate_repeat = gate_configuration['repeat']
            if gate_repeat == 'continuous':
                gate_repeat = Continuous
                print "--Warning: continuous count_time are governed by software clock,\
                and not NI-6602 hardware clock. Accuracy is not guranteed."
            elif not isinstance(gate_repeat,int):
                raise ValueError("Repeat must either be int or string of value 'continuous'")
            elif gate_repeat != 1:
                raise ValueError("Ni-6602 currently only supports repeat value of 1. Sorry :(")
            return DAQCounterSensor(ID,hardware,channels,gate_channel_name,gate_delay,gate_lowtime,gate_hightime,
                gate_repeat,count_time=count_time,name=n,description=d)
        else:
            return DAQCounterSensor(ID,hardware,channels,count_time =count_time,name=n,description=d,
                max_stored_data=max_stored_data)

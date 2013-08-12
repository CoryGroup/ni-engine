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
import config
from ..abstract_sensors import AbstractCounterSensor
from util_fns import assume_units
from storage import DataContainer, data
from ..hardware.nidaq import daqmx_threadsafe as daq

## Other Libraries ##
import quantities as pq

## Standard Library Imports ##
from itertools import izip
import ctypes as C

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
    def __init__(self, ID,
            channels=('/Dev1/ctr1',),
            gate_channel=None,
            gate_delay=pq.Quantity(0.0, "s"),
            gate_lowtime=pq.Quantity(0.1, "s"),
            gate_hightime=pq.Quantity(0.1, "s"),
            gate_repeat=1,
            name=name, description=description
        ):
        
        self._channel_names = channels
        self._gate_channel = gate_channel
        self._gate_delay = gate_delay
        self._gate_hightime = gate_hightime
        self._gate_lowtime = gate_lowtime
        self._gate_repeat = gate_repeat
        self._name = name
        self._description = description
        super(CTCThermistor,self).__init__() 

        
    ## TASK CREATION AND MANAGEMENT ##
    
    def __init_tasks(self):
        """
        Creates input and output tasks for each of the channels that will be
        counted or used as a gate.
        """
        # Do we need to gate?
        if self._gate_channel is not None:
            self._gate_task = daq.Task()
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
            self._gate_task.sample_timing_type = SampleTimingType.implicit
            
        # OK, now create the input tasks.
        self._input_tasks = [Task() for chan in self._channel_names]
        for idx, (task, chan_name) in enumerate(izip(self._input_tasks, self._channel_names)):
            task.create_ci_count_edges_chan(
                chan_name, "ch{}".format(idx),
                daq.Edge.rising,
                pq.Quantity(0, pq.counts),
                daq.CountDirection.up
            )
            # Do we need to gate the channel?
            if self._gate_channel is not None:
                # TODO: make an enum for this and move into Task().
                task.pause_trigger_type = PauseTriggerType.digital_level
                assert task.pause_trigger_type == PauseTriggerType.digital_level, \
                    "Pause trigger type for channel {} not changed!".format(chan_name)
                task.diglvl_pause_trigger_when = DigitalLevel.low
            
    def __start_tasks(self):
        # TODO: add error handling so that as many tasks as possible are
        #       started.
        
        # We want to make sure that the inputs start *before* the gate.
        # This allows us to work around the limit of not having a software
        # trigger.
        for chan_task in self._input_tasks:
            chan_task.start()
            
        if self._gate_channel is not None:
            self._gate_channel.start()
            
    def __stop_tasks(self):
        # We need to do things in the opposite order of __start_tasks, so
        # first, stop the gate pulses.
        if self._gate_channel is not None:
            self._gate_channel.stop()
            
        for chan_task in self._input_tasks:
            chan_task.stop()
        
    ## SENSOR CONTRACT ##
        
    def connect(self):
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
        measurement : CountContainer
        """
        # TODO: write this method.
        #       Roughly, need to stop the gate, read the inputs, stop the inputs,
        #       then restart the inputs and restart the inputs.
        with self._gate_task: # Tasks now support context manager protocols.
            pass
        return container

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
    ## ENUMS ##
    'PauseTriggerType',
    'DigitalLevel',
    'SampleTimingType',
    ## CLASSES ##
    'DAQCounterSensor'
]

## IMPORTS #####################################################################

## NI Engine Imports ##
import config
from ..abstract_sensors import AbstractCounterSensor
from util_fns import assume_units
from storage import DataContainer, data

## Hardware Support Imports ##
import PyDAQmx as daq

## Standard Library Imports ##
from itertools import izip
import ctypes as C

## Other Libraries ##
from flufl.enum import IntEnum

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
    Represents that a process is to be repeated continuously.
    """
    __metaclass__ = Singleton
    
    def __repr__(self):
        return "Continuous"
    
Continuous = ContinuousType()

## ENUMS #######################################################################

class PauseTriggerType(IntEnum):
    """
    Allowed values for the Pause Trigger Type attribute of a DAQmx Task.
    Documentation on the meaning of each value can be found in the
    `C API Reference`_.
    
    .. _C API Reference: http://zone.ni.com/reference/en-XX/help/370471Y-01/mxcprop/attr1366/
    """
    analog_level = daq.DAQmx_Val_AnlgLvl
    analog_window = daq.DAQmx_Val_AnlgWin
    digital_level = daq.DAQmx_Val_DigLvl
    digital_pattern = daq.DAQmx_Val_DigPattern
    none = daq.DAQmx_Val_None
    
class DigitalLevel(IntEnum):
    """
    Allowed values for properties that can take on one of two digital levels,
    high and low.
    """
    low = daq.DAQmx_Val_Low
    high = daq.DAQmx_Val_High
    
class SampleTimingType(IntEnum):
    """
    Allowed values for the sample timing type attribute of a DAQmx Task.
    Documentation on the meaning of each value can be found in the
    `C API Reference`_.
    
    .. _C API Reference: http://zone.ni.com/reference/en-XX/help/370471Y-01/mxcprop/attr1347/
    """
    sample_clock = daq.DAQmx_Val_SampClk
    burst_handshake = daq.DAQmx_Val_BurstHandshake
    handshake = daq.DAQmx_Val_Handshake
    implicit = daq.DAQmx_Val_Implicit
    on_demand = daq.DAQmx_Val_OnDemand
    change_detection = daq.DAQmx_Val_ChangeDetection
    pipelined_sample_clock = daq.DAQmx_Val_PipelinedSampClk

## CLASSES #####################################################################

class Task(daq.Task):
    """
    Used to add some nice logic to `PyDAQmx.Task` for when we are frustrated
    by the limitations of that class.
    """
    
    ## TASK STATE PROPERTIES ##
    
    @property
    def is_done(self):
        ret_val = C.c_uint32(0)
        self.IsTaskDone(C.byref(ret_val))
        return bool(ret_val.value)
    
    ## READ PROPERTIES ##
    # These properties implement reading of scalar values from the task.
    
    @property
    def counter_value(self):
        """
        Returns the current value of the counter scalar associated with this 
        task.
        
        .. seealso::
            PyDAQmx.Task.ReadCounterScalarU32
        """
        counter_val = C.c_uint32(0)
        self.ReadCounterScalarU32(1.0, C.byref(counter_val), None)
        return counter_val.value
        
    ## SAMPLE TIMING PROPERTIES ##
        
    @property
    def sample_timing_type(self):
        ret_val = C.c_uint32(0)
        self.GetSampTimingType(C.byref(ret_val))
        return SampleTimingType(ret_val.value)
    @sample_timing_type.setter
    def sample_timing_type(self, newval):
        self.SetSampTimingType(C.c_uint32(newval))
        
    ## TRIGGER PROPERTIES ##
    
    @property
    def diglvl_pause_trigger_src(self):
        """
        Returns the current source for the digital level pause trigger.
        """
        # TODO: TEST!
        buf = C.create_string_buffer(100)
        self.GetTrigAttribute(daq.DAQmx_DigLvl_pause_trigger_Src, buf)
        return buf.value
    @diglvl_pause_trigger_src.setter
    def diglvl_pause_trigger_src(self, newval):
        # TODO: TEST!
        self.SetDigLvlpause_triggerSrc(newval)
        
    @property
    def pause_trigger_type(self):
        """
        Gets/sets the type of pause trigger for this task, or
        `PauseTriggerType.none` if no pause trigger currently exists.
        """
        ret_val = C.c_uint32(0)
        self.Getpause_triggerType(C.byref(ret_val))
        return PauseTriggerType(ret_val.value)
    @pause_trigger_type.setter
    def pause_trigger_type(self, newval):
        task.Setpause_triggerType(C.c_uint32(newval))
        
    @property
    def diglvl_pause_trigger_when(self):
        ret_val = C.c_uint32(0)
        self.GetDigLvlpause_triggerWhen(C.byref(ret_val))
        return DigitalLevel(ret_val.value)
    @diglvl_pause_trigger_when.setter
    def diglvl_pause_trigger_when(self, newval):
        self.SetDigLvlpause_triggerWhen(C.c_uint32(newval))

    @property
    def start_retriggerable(self):
        ret_val = C.c_uint32(0)
        self.GetStartTrigRetriggerable(C.byref(ret_val))
        return bool(ret_val.value)
    @start_retriggerable.setter
    def start_retriggerable(self, newval):
        self.SetStartTrigRetriggerable(C.c_uint32(1 if newval else 0))

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
            self._gate_task = Task()
            self._gate_task.CreateCOPulseChanTime(
                    self._gate_channel,
                    "gate",
                    daq.DAQmx_Val_Seconds,
                    daq.DAQmx_Val_Low,
                    assume_units(self._gate_delay, "s"), 
                    assume_units(self._gate_lowtime, "s"), 
                    assume_units(self._gate_hightime, "s")
                )
            # We want to make the pulse repeat indefinitely or for a finite
            # number of samples, depending on the value of self._gate_repeat.
            # That only works if the timing type is Implicit for some reason.
            if self._gate_repeat is Continuous:
                self._gate_task.CfgSampClkTiming("OnboardClock", 10000.0, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 0)
            else:
                self._gate_task.CfgSampClkTiming("OnboardClock", 10000.0, daq.DAQmx_Val_Rising, daq.DAQmx_Val_FiniteSamps, self._gate_repeat)
            self._gate_task.sample_timing_type = SampleTimingType.implicit
            
        # OK, now create the input tasks.
        self._input_tasks = [Task() for chan in self._channel_names]
        for idx, (task, chan_name) in enumerate(izip(self._input_tasks, self._channel_names)):
            task.CreateCICountEdgesChan(
                chan_name, "ch{}".format(idx),
                daq.DAQmx_Val_Rising, 0, daq.DAQmx_Val_CountUp
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
            chan_task.StartTask()
            
        if self._gate_channel is not None:
            self._gate_channel.StartTask()
            
    def __stop_tasks(self):
        # We need to do things in the opposite order of __start_tasks, so
        # first, stop the gate pulses.
        if self._gate_channel is not None:
            self._gate_channel.StopTask()
            
        for chan_task in self._input_tasks:
            chan_task.StopTask()
        
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
        return container

#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# daqmx_threadsafe.py: Replacement for PyDAQmx with
#      threadsafe wrappers for DAQmx calls and classes.
##
# Part of the NI Engine project.
##

## ALL ########################################################################

__all__ = [
    ## ENUMS ##
    'PauseTriggerType',
    'Edge',
    'SampleMode',
    'DigitalLevel',
    'SampleTimingType',
    'CountDirection'
    ## CLASSES ##
    'Task',
    ## UNITS ##
    'samples'
]

## NI Engine Imports ##
from util_fns import assume_units, rescale_with_default

## Hardware Support Imports ##
import PyDAQmx as daq

## Other Libraries ##
import quantities as pq
from flufl.enum import IntEnum
import ctypes as C

## Standard Library Imports ##
import threading
import functools
import logging

## GLOBALS ####################################################################

# We use a reenterant lock so that if we accidently lock twice from within
# the same thread, nothing goes wrong. We only really care that DAQmx is always
# called from one thread at a time.
__daqmx_lock = threading.RLock()

# Make or get a logger instance that we'll use for debugging.
__logger = logging.getLogger('ni_engine.hardware.daqmx_threadsafe')

## UNITS ######################################################################

samples = pq.UnitQuantity('sample', 1.0 * pq.dimensionless, 'sample')

## ENUMS ######################################################################

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
    
class Edge(IntEnum):
    """
    Allowed values for properties that correspond to kinds of edges.
    """
    rising = daq.DAQmx_Val_Rising
    falling = daq.DAQmx_Val_Falling

class DigitalLevel(IntEnum):
    """
    Allowed values for properties that can take on one of two digital levels,
    high and low.
    """
    low = daq.DAQmx_Val_Low
    high = daq.DAQmx_Val_High
    
class SampleMode(IntEnum):
    """
    Allowed values for types of sample clock timings, as listed in the
    `C API Reference`_.

    .. _C API Reference: http://zone.ni.com/reference/en-XX/help/370471Y-01/daqmxcfunc/daqmxcfgsampclktiming/
    """
    finite_samples = daq.DAQmx_Val_FiniteSamps
    continuous_samples = daq.DAQmx_Val_ContSamps
    hw_timed_single_point = daq.DAQmx_Val_HWTimedSinglePoint

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

class CountDirection(IntEnum):
    up = daq.DAQmx_Val_CountUp
    down = daq.DAQmx_Val_CountDown

## DECORATORS ##################################################################

def locks_daq(fn):
    """
    Causes the decorated function or method to lock the DAQmx library when
    called and release that lock upon returning or an exception.
    """
    @functools.wraps(fn)
    def locking_fn(*args, **kwargs):
        global __daqmx_lock
        with __daqmx_lock:
            return fn(*args, **kwargs)
    return locking_fn

def log_calls(fn):
    """
    Causes all calls to the decorated function to be logged.
    """
    name = getattr(fn, '__name__', '<unnamed>')
    @functools.wraps(fn)
    def logging_fn(*args, **kwargs):
        global __logger
        __logger.debug("{name}({args}, {kwargs})".format(
            name=name,
            args=", ".join(map(repr, args)),
            kwargs=", ".join("{}={}".format(key, val) for key, val in kwargs.iteritems())
        ))
        return fn(*args, **kwargs)
    return logging_fn

## CLASSES #####################################################################

class Task(object):
    """
    Used to add some nice logic to `PyDAQmx.Task` for when we are frustrated
    by the limitations of that class. In particular, all calls to PyDAQmx from
    this class lock the DAQmx library such that this class is threadsafe.
    """
    def __init__(self):
        self._task = daq.Task()
        print "[DEBUG] Created new task {}.".format(self.name)
    
    ## TASK METADATA ##

    @property
    @locks_daq
    def name(self):
        buf = C.create_string_buffer(100)
        self._task.GetTaskAttribute(daq.DAQmx_Task_Name, buf)
        return buf.value
        
    def __repr__(self):
        return "<Task object at {} with name {}>".format(id(self), self.name)
    
    ## TASK STATE PROPERTIES AND METHODS ##
    @locks_daq
    @log_calls
    def wait_until_done(timeout=pq.Quantity(1, "s")):
        # TODO: catch for timeout error.
        self._task.WaitUntilTaskDone(assume_units(timeout, 's').rescale('s').magnitude)
    
    @property
    @locks_daq
    def is_done(self):
        ret_val = C.c_int32(0)

        self._task.IsTaskDone(C.byref(ret_val))
        return bool(ret_val.value)

    @locks_daq
    @log_calls
    def start(self):
        self._task.StartTask()
    @locks_daq
    @log_calls
    def stop(self):
        self._task.StopTask()

    # We implement the context manager protocol by aliasing __enter__
    # and __exit__ to start and stop, respectively.
    __enter__ = start
    __exit__ = stop
    
    ## READ PROPERTIES ##
    # These properties implement reading of scalar values from the task.
    
    @property
    @locks_daq    
    def counter_value(self):
        """
        Returns the current value of the counter scalar associated with this 
        task.
        
        .. seealso::
            PyDAQmx.Task.ReadCounterScalarU32
        """
        counter_val = C.c_int32(0)
        self._task.ReadCounterScalarU32(1.0, C.byref(counter_val), None)
        return counter_val.value
        
    ## SAMPLE TIMING PROPERTIES ##
        
    @property
    @locks_daq
    def sample_timing_type(self):
        ret_val = C.c_int32(0)
        self._task.GetSampTimingType(C.byref(ret_val))
        return SampleTimingType(ret_val.value)
    @sample_timing_type.setter
    @locks_daq
    @log_calls
    def sample_timing_type(self, newval):
        self._task.SetSampTimingType(newval)
        
    ## TRIGGER PROPERTIES ##
    
    @property
    @locks_daq
    def diglvl_pause_trigger_src(self):
        """
        Returns the current source for the digital level pause trigger.
        """
        # TODO: TEST!
        buf = C.create_string_buffer(100)
        self._task.GetTrigAttribute(daq.DAQmx_DigLvl_PauseTrig_Src, buf)
        return buf.value
    @diglvl_pause_trigger_src.setter
    @locks_daq
    @log_calls
    def diglvl_pause_trigger_src(self, newval):
        # TODO: TEST!
        self._task.SetDigLvlPauseTrigSrc(newval)
        
    @property
    @locks_daq
    def pause_trigger_type(self):
        """
        Gets/sets the type of pause trigger for this task, or
        `PauseTriggerType.none` if no pause trigger currently exists.
        """
        ret_val = C.c_int32(0)
        self._task.GetPauseTrigType(C.byref(ret_val))
        return PauseTriggerType(ret_val.value)
    @pause_trigger_type.setter
    @locks_daq
    @log_calls
    def pause_trigger_type(self, newval):
        self._task.SetPauseTrigType(C.c_int32(newval))
        
    @property
    @locks_daq
    def diglvl_pause_trigger_when(self):
        ret_val = C.c_int32(0)
        self._task.GetDigLvlpause_triggerWhen(C.byref(ret_val))
        return DigitalLevel(ret_val.value)
    @diglvl_pause_trigger_when.setter
    @locks_daq
    @log_calls
    def diglvl_pause_trigger_when(self, newval):
        self._task.SetDigLvlPauseTrigWhen(C.c_int32(newval))

    @property
    @locks_daq
    def start_retriggerable(self):
        ret_val = C.c_int32(0)
        self._task.GetStartTrigRetriggerable(C.byref(ret_val))
        return bool(ret_val.value)
    @start_retriggerable.setter
    @locks_daq
    @log_calls
    def start_retriggerable(self, newval):
        self._task.SetStartTrigRetriggerable(C.c_int32(1 if newval else 0))

    ## CHANNEL LIST PROPERTIES ##

    @property
    @locks_daq
    def channels(self):
        n_channels = C.c_uint32(0)
        self._task.GetTaskAttribute(daq.DAQmx_Task_NumChans, C.byref(n_channels))

        chan_names = [C.create_string_buffer(100) for idx in xrange(n_channels.value)]
        for idx, chan_buf in enumerate(chan_names):
            self._task.GetNthTaskChannel(1 + idx, chan_buf, 100)

        return [chan_buf.value for chan_buf in chan_names]

    ## CHANNEL CREATION FUNCTIONS ##

    @locks_daq
    @log_calls
    def create_co_pulse_channel_time(self,
            counter,
            name,
            idle_state,
            initital_delay,
            low_time, high_time
    ):
        initital_delay = rescale_with_default(initital_delay, 's')
        low_time = rescale_with_default(low_time, 's')
        high_time = rescale_with_default(high_time, 's')
        self._task.CreateCOPulseChanTime(
                counter,
                name,
                daq.DAQmx_Val_Seconds,
                C.c_int32(idle_state),
                initital_delay,
                low_time, high_time
        )

    @locks_daq
    @log_calls
    def create_ci_count_edges_chan(self,
            counter,
            name,
            edge,
            initial_count,
            count_direction
    ):
        self._task.CreateCICountEdgesChan(
            counter, name,
            C.c_int32(edge),
            rescale_with_default(initial_count, pq.counts),
            C.c_int32(count_direction)
        )

    ## TIMING FUNCTIONS ##

    @locks_daq
    @log_calls
    def config_sample_clock_timing(self,
            source, rate, active_edge, sample_mode,
            samples_per_chan
    ):
        self._task.CfgSampClkTiming(
            source,
            assume_units(rate,1/pq.s).rescale(samples / pq.s).magnitude,
            C.c_int32(active_edge),
            C.c_int32(sample_mode),
            C.c_uint64(samples_per_chan)
        )
        

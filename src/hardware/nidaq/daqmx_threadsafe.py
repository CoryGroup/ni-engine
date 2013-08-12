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

## Standard Library Imports ##
import threading
import functools

## GLOBALS ####################################################################

# We use a reenterant lock so that if we accidently lock twice from within
# the same thread, nothing goes wrong. We only really care that DAQmx is always
# called from one thread at a time.
__daqmx_lock = threading.RLock()

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
	up = DAQmx_Val_CountUp
	down = DAQmx_Val_CountDown

## DECORATORS ##################################################################

def locks_daq(fn):
	"""
	Causes the decorated function or method to lock the DAQmx library when
	called and release that lock upon returning or an exception.
	"""
	@wraps(fn)
	def locking_fn(*args, **kwargs):
		global __daqmx_lock
		with __daqmx_lock:
			return fn(*args, **kwargs)
	return locking_fn

## CLASSES #####################################################################

class Task(daq.Task):
    """
    Used to add some nice logic to `PyDAQmx.Task` for when we are frustrated
    by the limitations of that class. In particular, all calls to PyDAQmx from
    this class lock the DAQmx library such that this class is threadsafe.
    """
    
    ## TASK STATE PROPERTIES AND METHODS ##
    @locks_daq
    def wait_until_done(timeout=pq.Quantity(1, "s")):
        # TODO: catch for timeout error.
        self.WaitUntilTaskDone(assume_units(timeout, 's').rescale('s').value)
    
    @locks_daq
    @property
    def is_done(self):
    	global __daqmx_lock
        ret_val = C.c_uint32(0)

        self.IsTaskDone(C.byref(ret_val))
        return bool(ret_val.value)

    @locks_daq
    def start(self):
    	self.StartTask()
    @locks_daq
    def stop(self):
    	self.StopTask()

    # We implement the context manager protocol by aliasing __enter__
    # and __exit__ to start and stop, respectively.
    __enter__ = start
    __exit__ = stop
    
    ## READ PROPERTIES ##
    # These properties implement reading of scalar values from the task.
    
    @locks_daq
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
    @locks_daq
    def sample_timing_type(self):
        ret_val = C.c_uint32(0)
        self.GetSampTimingType(C.byref(ret_val))
        return SampleTimingType(ret_val.value)
    @sample_timing_type.setter
    @locks_daq
    def sample_timing_type(self, newval):
        self.SetSampTimingType(C.c_uint32(newval))
        
    ## TRIGGER PROPERTIES ##
    
    @property
    @locks_daq
    def diglvl_pause_trigger_src(self):
        """
        Returns the current source for the digital level pause trigger.
        """
        # TODO: TEST!
        buf = C.create_string_buffer(100)
        self.GetTrigAttribute(daq.DAQmx_DigLvl_PauseTrig_Src, buf)
        return buf.value
    @diglvl_pause_trigger_src.setter
    @locks_daq
    def diglvl_pause_trigger_src(self, newval):
        # TODO: TEST!
        self.SetDigLvlPauseTrigSrc(newval)
        
    @property
    @locks_daq
    def pause_trigger_type(self):
        """
        Gets/sets the type of pause trigger for this task, or
        `PauseTriggerType.none` if no pause trigger currently exists.
        """
        ret_val = C.c_uint32(0)
        self.Getpause_triggerType(C.byref(ret_val))
        return PauseTriggerType(ret_val.value)
    @pause_trigger_type.setter
    @locks_daq
    def pause_trigger_type(self, newval):
        task.Setpause_triggerType(C.c_uint32(newval))
        
    @property
    @locks_daq
    def diglvl_pause_trigger_when(self):
        ret_val = C.c_uint32(0)
        self.GetDigLvlpause_triggerWhen(C.byref(ret_val))
        return DigitalLevel(ret_val.value)
    @diglvl_pause_trigger_when.setter
    @locks_daq
    def diglvl_pause_trigger_when(self, newval):
        self.SetDigLvlpause_triggerWhen(C.c_uint32(newval))

    @property
    @locks_daq
    def start_retriggerable(self):
        ret_val = C.c_uint32(0)
        self.GetStartTrigRetriggerable(C.byref(ret_val))
        return bool(ret_val.value)
    @start_retriggerable.setter
    @locks_daq
    def start_retriggerable(self, newval):
        self.SetStartTrigRetriggerable(C.c_uint32(1 if newval else 0))

    ## CHANNEL CREATION FUNCTIONS ##

    @locks_daq
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
    	self.CreateCOPulseChanTime(
    			counter,
    			name,
    			daq.DAQmx_Val_Seconds,
    			C.c_int32(idle_state),
    			initital_delay,
    			low_time, high_time
    	)

	@locks_daq
	def create_ci_count_edges_chan(self,
			counter,
			name,
			edge,
			initial_count,
			count_direction
	):
		self.CreateCICountEdgesChan(
            counter, name,
            C.c_uint32(edge),
            rescale_with_default(initial_count, pq.counts),
            C.c_uint32(count_direction)
        )

    ## TIMING FUNCTIONS ##

    @locks_daq
    def config_sample_clock_timing(self,
    		source, rate, active_edge, sample_mode,
    		samples_per_chan
	):
		self.CfgSampClkTiming(
			source,
			assume_units(rate).rescale(samples / pq.s).value,
			C.c_uint32(active_edge),
			C.c_uint32(sample_mode),
			C.c_uint64(samples_per_chan)
		)

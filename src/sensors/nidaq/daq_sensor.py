##
# daq_sensor.py: Sensor class for NI-DAQ devices, backed by the PyDAQmx library.
##
# Part of the NI Engine project.
##

## IMPORTS #####################################################################

import config 
import PyDAQmx as daq

from ..abstract_sensors import AbstractCounterSensor
from util_fns import assume_units

from storage import DataContainer, data

from itertools import izip
import ctypes as C

from flufl.enum import IntEnum

## ENUMS #######################################################################

class pause_triggergerType(IntEnum):
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
        `pause_triggergerType.none` if no pause trigger currently exists.
        """
        ret_val = C.c_uint32(0)
        self.Getpause_triggerType(C.byref(ret_val))
        return pause_triggergerType(ret_val.value)
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
            name=name, description=description
        ):
        
        self._channel_names = channels
        self._gate_channel = gate_channel
        self._gate_delay = gate_delay
        self._gate_hightime = gate_hightime
        self._gate_lowtime = gate_lowtime
        self._name = name
        self._description = description
        super(CTCThermistor,self).__init__() 

        self.__init_tasks()
        
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
            # We want to make the pulse repeat indefinitely.
            # That only works if the timing type is Implicit for some reason.
            # TODO: Oops... http://forums.ni.com/t5/Multifunction-DAQ/How-do-I-use-the-daqmx-send-software-trigger-vi/td-p/111867
            #       Looks like we may have to start and stop the tasks instead.
            #       If so, then this needs to change to run a finite number of
            #       times instead of continuously.
            self._gate_task.CfgSampClkTiming("OnboardClock", 10000.0, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 0)
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
                task.pause_trigger_type = pause_triggergerType.digital_level
                assert task.pause_trigger_type == pause_triggergerType.digital_level, \
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
        

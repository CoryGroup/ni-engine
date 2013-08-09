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

## CLASSES #####################################################################

class Task(daq.Task):
    """
    Used to add some nice logic to `PyDAQmx.Task` for when we are frustrated
    by the limitations of that class.
    """
    
    @property
    def counter_scalar(self):
        """
        Returns the current value of the counter scalar associated with this 
        task.
        
        .. seealso::
            PyDAQmx.Task.ReadCounterScalarU32
        """
        counter_val = C.c_uint32(0)
        self.ReadCounterScalarU32(1.0, C.byref(counter_val), None)
        return counter_val.value
        
    @property
    def diglvl_pausetrig_src(self):
        """
        Returns the current source for the digital level pause trigger.
        """
        # TODO: TEST!
        buf = C.create_string_buffer(100)
        self.GetTrigAttribute(daq.DAQmx_DigLvl_PauseTrig_Src, buf)
        return buf.value
    @diglvl_pausetrig_src.setter
    def diglvl_pausetrig_src(self, newval):
        # TODO: TEST!
        self.SetDigLvlPauseTrigSrc(newval)


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
            # TODO: add software triggering for the pulse output instead of
            #       repeating indefinitely; the current mode is only useful for
            #       testing.
            self._gate_task.CfgSampClkTiming("OnboardClock", 10000.0, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 0)
            self._gate_task.SetSampTimingType(daq.DAQmx_Val_Implicit)
            
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
                task.SetPauseTrigType(daq.DAQmx_Val_DigLvl)
                task.GetTrigAttribute(daq.DAQmx_PauseTrig_Type, C.byref(ret_val))
                task.SetDigLvlPauseTrigWhen(daq.DAQmx_Val_Low)
            
    def __start_tasks(self):
        # TODO: add error handling so that as many tasks as possible are
        #       started.
        if self._gate_channel is not None:
            self._gate_channel.StartTask()
        for chan_task in self._input_tasks:
            chan_task.StartTask()
        

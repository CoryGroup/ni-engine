import ni_engine.config as config 
from instruments.faulhaber import FaulhaberMCLM3002
from ..abstract_controller import AbstractController
from ni_engine.hardware.faulhaber import FaulhaberMCLM3002Hardware
from ni_engine.storage import DataContainer,data
import os.path
import numpy as np
import quantities as pq
from os import listdir
from os.path import isfile, join,abspath
from time import sleep 


class LM1247(AbstractController):
    """
    LM1247 motor controller. This is the main way to interact 
    with the FaulhaberMCLM3002Hardware. 

    **Required Parameters:**
    
    * 'axis_id'(int)
    * 'past_position_file'(str) Is a name of file where past_positions 
        are stored so that the Newport does not go out of sync

    **Optional Parameters:**
        
        * 'default_position' if not set is current position (U) 
        * 'configuration_parameters' (all are optional)
            * 'motor_type' type of motor see 'QM' in Newport documentation
            * 'current' motor maximum current (A)
            * 'voltage' motor voltage (V)
            * 'units' set units (see NewportESP301Units)(U)
            * 'resolution' value of encoder step in terms of (U)
            * 'max_velocity' maximum velocity (U/s)
            * 'max_working_velocity'  maximum working velocity (U/s)
            * 'homing_velocity' homing speed (U/s)
            * 'jog_high_velocity' jog high speed (U/s)
            * 'jog_low_velocity' jog low speed (U/s)
            * 'max_acceleration' maximum acceleration (U/s^2)
            * 'acceleration' acceleration (U/s^2)
            * 'deceleration' set deceleration (U/s^2)
            * 'error_threshold' set error threshold (U)
            * 'proportional_gain' PID proportional gain (optional)
            * 'derivative_gain' PID derivative gain (optional)
            * 'interal_gain' PID internal gain (optional)
            * 'integral_saturation_gain' PID integral saturation (optional)
            * 'trajectory' trajectory mode (optional)
            * 'position_display_resolution' (U per step)
            * 'feedback_configuration'
            * 'full_step_resolution'  (U per step)
            * 'home' (U)
            * 'acceleration_feed_forward' bewtween 0 to 2e9
            * 'reduce_motor_torque'  (time(ms),percentage)

    """
    code = 'LM1247'
    name = 'Faulhaber LM1247 Linear Motor'
    description = 'LM1247 linear motor for Faulhaber MCLM3002'    
    def __init__(self,ID,hardware,start_activated=True,default_position=0,motor_mode=FaulhaberMCLM3002.Mode.CONTMOD,
                        home_position=0,position_limits_enabled=False,position_limits=None,                       
                        max_stored_data=100,name=name,description=description):
        """
        Initialize the lm1247 motor 

        Parameters
        ----------

        ID : str 
        hardware : AbstractHardware 
        default_position : int
        motor_mode : FaulhaberMCLM3002.Mode 
        home_position : int 
        position_limits_enabled : bool 
        position_limits : int 
            Position limits to move too 
        max_stored_data : int
        name : str 
        description : str

        """
        if not isinstance(hardware, FaulhaberMCLM3002Hardware):
            raise TypeError("Motor must be controlled by a Faulhaber MCLM3002 motor hardware.")

                  
        self._MCLM3002 = self._hardware = hardware
        self._start_activated = start_activated
        self._default_position = default_position                   
        self._motor_mode = motor_mode
        self._home_position = 0 
        self._position_limits_enabled = position_limits_enabled
        self._position_limits = position_limits  
        
        super(LM1247,self).__init__(ID,LM1247.code,name,description,max_stored_data)

    def __del__(self): 
        # stops motion on axis
        # saves last position
        # deletes mem-mapping which 
        # will store it to disk
        self._hardware.stop_movement()
       
        

    def connect(self):
        """
        Connect to axis
        """

        

        
        if self._default_position is not None:
            self._hardware.activated = True
            self.move_absolute(self._default_position)

        
        self.activated = True if self._start_activated else False
    
    

    def move_absolute(self,position,block=True,timeout=0.5*pq.s,t_int=0.03*pq.s,tolerance=1):
        """
        Move relative to zero position.

        Parameters
        ----------
        position : int
        block : bool
            Block code until movement is done
        timeout : pq.Quantity 
            Time to wait before timing out and raising exception
        t_int : pq.Quantity
            time to wait between checking if position reached 
        tolerance : int 
            relative error to target position at which blocking will terminate 
        
        """
        time = 0*pq.s
        
        try:            
            self._hardware.absolute_position = position 
            self._hardware.activate_motion()
            if block:
                motion_done = False
                while not motion_done:
                    time += t_int 
                    sleep(t_int)
                    if abs(position-self._hardware.absolute_position)<=tolerance:
                        motion_done = True 

                    elif time > timeout:
                        raise Exception('Movement has timed out')


        except Exception, e :
            raise
        finally:
            pass
        

    def move_relative(self,distance,block=True,timeout=0.5*pq.s,t_int=0.03*pq.s,tolerance=1):
        """
        Move relative to current

        Parameters
        ----------
        position : int
        block : bool
            Block code until movement is done
        timeout : pq.Quantity 
            Time to wait before timing out and raising exception
        t_int : pq.Quantity
            time to wait between checking if position reached 
        tolerance : int 
            relative error to target position at which blocking will terminate 
        
        """
        time = 0*pq.s
        t_pos = self._hardware.absolute_position + distance
        self._hardware.activate_motion()
        try:            
            self._hardware.relative_position = distance  
            if block:
                motion_done = False
                while not motion_done:
                    time += t_int 
                    sleep(t_int)
                    if abs(t_pos-self._hardware.absolute_position)<=tolerance:
                        motion_done = True 
                    elif time > timeout:
                        raise Exception('Movement has timed out')

        except Exception, e :
            raise
        finally:
            pass
    
    def stop(self):
        """
        Stop the motor motion 
        """
        self._hardware.stop_movement()

    @property
    def activated(self):
        """
        Activates the motor drive 

        Parameters
        ----------
        activated : bool 

        Returns 
        -------
        activated : QuantityData
        """
        return data(self.id,self.code,'activated',self._activated)
    @activated.setter
    def activated(self, activated):        
        self._hardware.activated = activated
        self._activated = activated

    

    @property
    def position(self):
        """
        Get the current position

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'position',self._hardware.absolute_position)
    
    @property
    def temperature(self):
        """
        Get the motor temperature

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'temperature',self._hardware.temperature)

    @property
    def current(self):
        """
        Get the motor current

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'current',self._hardware.current)
    

    @property
    def pwm_voltage(self):
        """
        Get the motor pwm_voltage

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'pwm_voltage',self._hardware.pwm_voltage)

    @property
    def target_position(self):
        """
        Get the motor target position 

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'target_position',self._hardware.target_position)
    
    @property
    def target_velocity(self):
        """
        Get the motor target volocity 

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'target_velocity',self._hardware.target_velocity)
    
    
    
    

    def get_status(self):
        """
        Gets status of axis. 
        Returns a DataContainer of data elements:
        * "position"
        * "units"
        * "desired_position"
        * "desired_velocity"
        * "velocity"
        * "is_motion_done"
        * "current"
        * "pwm_voltage"
        * "temperature"


        Returns 
        -------
        DataContainer
            contains data items
        """
        
        status = DataContainer(self.id,self._max_stored_data)
        
        status['position'] = self.position
        status['activated'] = self.activated 
        status['temperature'] = self.temperature
        status['current'] = self.current 
        status['pwm_voltage'] = self.pwm_voltage
        status['target_position'] = self.target_position
        status['target_velocity'] = self.target_velocity

        return status 


    
    def disconnect(self):
        raise NotImplementedError('Abstract method has not been implemented')  
    
    
        

    @classmethod 
    def create(cls,configuration,data_handler,hardware,sensors):

        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        activated = configuration.get('start_activated',True)
        default_position = configuration.get("default_position",None)               
        motor_mode = FaulhaberMCLM3002.Mode[configuration.get('motor_mode','CONTMOD')]        
        position_limits_enabled = configuration.get('position_limits_enabled',False)
        position_limits = configuration.get('position_limits',None)
        home_position = configuration.get('home_position',0)


        
                
        return LM1247(ID,hardware,start_activated=activated,default_position=default_position,motor_mode=motor_mode,home_position=home_position,
                        position_limits_enabled=position_limits_enabled,position_limits=position_limits,
                        name=n,description=d)



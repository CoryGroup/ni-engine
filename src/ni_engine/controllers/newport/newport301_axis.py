import ni_engine.config as config 
from instruments.other import NewportESP301,NewportESP301Axis, NewportError
from ..abstract_controller import AbstractController
from ni_engine.hardware.newport import Newport301
from ni_engine.storage import DataContainer,data
from . import axis_positions
import os.path
import numpy as np
import quantities as pq
from os import listdir
from os.path import isfile, join,abspath



class Newport301Axis(AbstractController):
    """
    NewportESP301Axis controller. This is the main way to interact 
    with the NewportESP301. 

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
    code = 'NEWPORTAXIS'
    name = 'NewportESP 301 Axis'
    description = 'Axis of NewportESP 301 Axis Controller '    
    _default_position = 0
    TOLERANCE = 0.1
    absolute_path = os.path.abspath(axis_positions.__file__)
    def __init__(self,ID,hardware,axis, past_position_file,default_position = None,configuration_parameters=None,
        max_stored_data=100,name=name,description=description):
        """
        Initialize the newport axis 

        Parameters
        ----------

        ID : str 
        hardware : AbstractHardware 
        axis : NewportESP301Axis
        past_position_file : str 
            Path to file of previous positions
        default_position : quantities.Quantity or float
            position to move to initially 
        configuration_parameters : dict 
            Dictionary containing the configuration parameters required by :class:`.Newport301Axis`
        max_stored_data : int
        name : str 
        description : str

        """
        if not isinstance(hardware, Newport301):
            raise TypeError("Axis must be controlled by a Newport ESP-301 motor hardware.")

        if not isinstance(axis, NewportESP301Axis):
            raise TypeError("Axis must be a Newport ESP-301 Axis.")

        self._axis = axis
        self._axis.disable()           
        self._newport301 = self._hardware = hardware
        self._default_position = default_position                   
        self._past_position_file = past_position_file        
        self.configuration_parameters = configuration_parameters 
        super(Newport301Axis,self).__init__(ID,Newport301Axis.code,name,description,max_stored_data)

    def __del__(self): 
        # stops motion on axis
        # saves last position
        # deletes mem-mapping which 
        # will store it to disk

        self._axis.abort_motion()
        self.append_last_position()      
        del self._past_position

    def connect(self):
        """
        Connect to axis
        """
        self._axis.disable()
        self.initialize_defaults()

       

        self._past_position = self._get_last_position_file(Newport301Axis.absolute_path.
            replace('__init__.pyc',"{}.npy".format(self._past_position_file)).\
            replace('__init__.py',"{}.npy".format(self._past_position_file)))
        
        self.setup_last_position()
        self._axis.enable()        
        if self._default_position is not None:
            self.move_absolute(self._default_position,wait=True,block=True)

    def initialize_defaults(self):
        """
        Setup axis configuration values
        """
        if self.configuration_parameters is not None:
            self._axis.setup_axis(**self.configuration_parameters)

    def _get_last_position_file(self,file_path):        
        if os.path.isfile(file_path):
            return np.load(file_path, mmap_mode='r+') 
        else:
            temp = data(self.id,self.code,'position',0*self._axis.units)
            empty_array = np.zeros(10000,dtype=float)            
            np.save(file_path,empty_array)            
            return np.load(file_path, mmap_mode='r+')



    def setup_last_position(self):
        
        last_position = self._past_position[0]*self.units
        curr_position = self.position           

        if last_position - curr_position > self.TOLERANCE:
            self._axis.home = last_position           
        elif curr_position -last_position > self.TOLERANCE:
            self._axis.home = last_position
        self.append_last_position()
    def append_last_position(self,position=None):
        rolled = np.roll(self._past_position,1)
        rolled[0] = self.position if position is None else position
        self._past_position[:] = rolled
    def move_absolute(self,position,wait=False,block=False):
        """
        Move relative to zero position.

        Parameters
        ----------
        position : quantities.Quantity or float
        wait : bool
            Tell Newport not to execute other commands until done moving
        block : bool
            Block code until movement is done
        
        """
        try:
            self.append_last_position(position)
            self._axis.move(position,absolute = True,wait=wait,block=block)
        except NewportError, e :
            raise
        finally:
            self.append_last_position()
        

    def move_relative(self,distance,wait=False,block=False):
        """
        Move relative to current position.

        Parameters
        ----------
        distance : quantities.Quantity or float
        wait : bool
            Tell Newport not to execute other commands until done moving
        block : bool
            Block code until movement is done
        timeout : float 
            If blocking how, long to wait for movement before throwing error
        """
        try:
            self.append_last_position(self.position+distance)
            self._axis.move(position,absolute = False,wait=wait,block=block)
        except NewportError, e :
            raise
        finally:
            self.append_last_position()
        
    @property
    def position(self):
        """
        Get the current position

        Returns
        -------
        position : QuantityData
        """
        return data(self.id,self.code,'position',self._axis.position)
    
    @property
    def units(self):
        """
        Returns
        -------
        quantities.Quantity
            Units being used
        """
        return self._axis.units
    
    
    

    def get_status(self):
        """
        Gets status of axis. 
        Returns a DataContainer of data elements:
        * "position"
        * "units"
        * "desired_position"
        * "desired_velocity"
        * "is_motion_done"

        Returns 
        -------
        DataContainer
            contains data items
        """
        status_dict = self._axis.get_status()
        status = DataContainer(self.id,self._max_stored_data)
        for k,v in status_dict.iteritems():
            status[k] = data(self.id,Newport301Axis.code,k,v)

        return status 

    def get_configuration(self):
        """
        Gets status of axis. 
        Returns a DataContainer of data elements:
        * 'units'
        * 'motor_type'
        * 'feedback_configuration'
        * 'full_step_resolution'
        * 'position_display_resolution'
        * 'current'
        * 'max_velocity'
        * 'encoder_resolution'
        * 'acceleration'
        * 'deceleration'
        * 'velocity'
        * 'max_acceleration'
        * 'homing_velocity'
        * 'jog_high_velocity'
        * 'jog_low_velocity'
        * 'estop_deceleration'
        * 'jerk'
        * 'error_threshold'
        * 'proportional_gain'
        * 'derivative_gain'
        * 'integral_gain'
        * 'integral_saturation_gain'
        * 'home'
        * 'microstep_factor'
        * 'acceleration_feed_forward'
        * 'trajectory'
        * 'hardware_limit_configuration'

        Returns 
        -------
        DataContainer
            contains data items
        """
        conf_dict = self._axis.get_status()
        conf = DataContainer(self.id,self._max_stored_data)
        for k,v in conf_dict.iteritems():
            conf[k] = data(self.id,Newport301Axis.code,k,v)

        return conf


    @property
    def axis(self):
        """
        Returns
        -------
        newportesp301.NewportESP301Axis
        """
        return self._axis
    
    def disconnect(self):
        raise NotImplementedError('Abstract method has not been implemented')  
    
    
        

    @classmethod 
    def create(cls,configuration,data_handler,hardware,sensors):

        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        past_position_file = configuration['past_position_file']
        default_position = configuration.get("default_position",None)        
        configuration_parameters = configuration.get("configuration_parameters",None)        
        axis_id = configuration['axis_id']
        axis = hardware.axis[axis_id]
        
                
        return Newport301Axis(ID,hardware,axis,past_position_file,default_position,configuration_parameters,name=n,description=d)



import ni_engine.config as config 
from instruments.other import NewportESP301,NewportESP301Axis
from ..abstract_controller import AbstractController
from ni_engine.hardware.newport import Newport301
from ni_engine.storage import DataContainer,data
class Newport301Axis(AbstractController):
    code = 'NEWPORTAXIS'
    name = 'NewportESP 301 Axis'
    description = 'Axis of NewportESP 301 Axis Controller '    
    _default_position = 0
    

    def __init__(self,ID,hardware,axis, default_position,configuration_parameters=None,max_stored_data=100,name=name,description=description):
        """
        Initialize the newport axis 
        """
        if not isinstance(hardware, Newport301):
            raise TypeError("Axis must be controlled by a Newport ESP-301 motor hardware.")

        if not isinstance(axis, NewportESP301Axis):
            raise TypeError("Axis must be a Newport ESP-301 Axis.")

        self._axis = axis
        self._axis.disable()
        self._id = ID 
        
        self._newport301 = self._hardware = hardware
        self._default_position = default_position                       
        self._name = name
        self._description = description
        self._max_stored_data = max_stored_data
        self.configuration_parameters = configuration_parameters 

    def connect(self):
        """
        Connect to axis
        """
        self._axis.disable()
        self.initialize_defaults()
        self._axis.enable()
        self.move_absolute(self._default_position,wait=True,block=True)

    def initialize_defaults(self):
        """
        Setup axis configuration values
        """
        if self.configuration_parameters is not None:
            self._axis.setup_axis(**self.configuration_parameters)



    def move_absolute(self,position,wait=False,block=False):
        """
        Move relative to zero position.

        Parameters
        ----------
        distance : quantities.Quantity or float
        """
        self._axis.move(position,absolute = True,wait=wait,block=block)

    def move_relative(self,distance,wait=False,block=False):
        """
        Move relative to current position.

        Parameters
        ----------
        distance : quantities.Quantity or float
        """
        self._axis.move(distance,absolute=False,wait=wait,block=block)

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
        pass  
    

    @classmethod 
    def create(cls,configuration,data_handler,hardware,sensors):

        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        default_position = configuration.get("default_position",cls._default_position)        
        configuration_parameters = configuration.get("configuration_parameters",None)        
        axis_id = configuration['axis_id']
        axis = hardware.axis[axis_id]
        
                
        return Newport301Axis(ID,hardware,axis,default_position,configuration_parameters,name=n,description=d)


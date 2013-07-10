import config 
from instruments.other import NewportESP301,NewportESP301Axis
from abstractController import AbstractController
from .hardware.newport301 import Newport301

class Newport301Axis(AbstractController):
    code = 'NEWPORTAXIS'
    name = 'NewportESP 301 Axis'
    description = 'Axis of NewportESP 301 Axis Controller '    
    _default_position = 0
    _default_velocity = 5
    _default_acceleration = 3 
    _default_deceleration = 3
    _max_velocity = 40
    _max_acceleration = 20 

    def __init__(self,ID,hardware,axis,home=_default_position,default_velocity=_default_velocity,default_acceleration=default_acceleration,
                            default_deceleration=_default_deceleration,max_velocity=_max_velocity,max_acceleration=_max_acceleration,
                            units,name=name,description=description,**optional_args):
        if not isinstance(controller, Newport301):
            raise TypeError("Axis must be controlled by a Newport ESP-301 motor hardware.")

        if not isinstance(axis, NewportESP301Axis):
            raise TypeError("Axis must be a Newport ESP-301 Axis.")

        self.axis = axis
        self.id = ID 
        self.hardware = hardware
        self._default_position = default_position
        self._default_velocity = default_velocity
        self._default_acceleration = default_acceleration
        self._default_deceleration = default_deceleration
        self._max_velocity = max_velocity
        self._max_acceleration = max_acceleration          
        self.name = name
        self.description = description
        self.optional_args = optional_args

    def connect(self):
        self.initialize_defaults()

    def initialize_defaults(self):
        with self.axis.execute_bulk_command(self):
            self.axis.max_acceleration = self._max_acceleration
            self.axis.max_velocity = self._max_velocity
            self.axis.acceleration = self._default_acceleration
            self.axis.deceleration = self._default_deceleration
            self.axis.velocity = self._default_velocity
            self.axis.home = self.home
        
            for key,value in self.optional_args.iteritems():
                setattr(self.axis,key,value)


 

    @classmethod 
    def create(cls,configuration,hardware,sensors):
        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        home = configuration.get("home",cls._default_position)
        default_velocity = configuration.get("default_velocity",cls._default_velocity)
        default_acceleration = configuration.get("default_acceleration",cls._default_acceleration)
        default_deceleration = configuration.get("default_deceleration",cls._default_deceleration)
        max_velocity = configuration.get("max_velocity",cls._max_velocity)
        max_acceleration = configuration.get("max_acceleration",cls._max_acceleration)
        optional_args = configuration.get("optional_args",dict())

        
        axis_id = configuration['axis_id']
        
                
        return Newport301Axis(ID,hardware,axis,home,default_velocity,default_acceleration,default_deceleration,
                            max_velocity,max_acceleration,units=name=n,description=d,**optional_args)


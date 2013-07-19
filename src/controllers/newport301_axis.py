import config 
from instruments.other import NewportESP301,NewportESP301Axis
from abstractController import AbstractController
from hardware.newport301 import Newport301

class Newport301Axis(AbstractController):
    code = 'NEWPORTAXIS'
    name = 'NewportESP 301 Axis'
    description = 'Axis of NewportESP 301 Axis Controller '    
    _default_position = 0
    

    def __init__(self,ID,hardware,axis, default_position,home,name=name,description=description,**optional_args):
        if not isinstance(controller, Newport301):
            raise TypeError("Axis must be controlled by a Newport ESP-301 motor hardware.")

        if not isinstance(axis, NewportESP301Axis):
            raise TypeError("Axis must be a Newport ESP-301 Axis.")

        
        self._id = ID 
        self._axis = self.axis
        self._newport301 = self._hardware = hardware
        self._default_position = default_position    
        self._home = home             
        self._name = name
        self._description = description
        self._optional_args = optional_args

    def connect(self):
        self.initialize_defaults()
        self.move(self._default_position)

    def initialize_defaults(self):
        with self._axis.execute_bulk_command(self):            
            self._axis.home = self._home
        
            for key,value in self.optional_args.iteritems():
                setattr(self._axis,key,value)



    def move_absolute(self,position):
        self._axis.move(position,absolute = True)

    def move_relative(self,distance):
        self._axis.move(distance)

 

    @classmethod 
    def create(cls,configuration,hardware,sensors):
        ID = configuration[config.ID]
        n = configuration.get(config.NAME,cls.name)
        d = configuration.get(config.DESCRIPTION,cls.description)
        default_position = configuration.get("default_position",cls._default_position)
        home = configuration.get("home",cls._home)
        default_velocity = configuration.get("default_velocity",cls._default_velocity)
        default_acceleration = configuration.get("default_acceleration",cls._default_acceleration)
        default_deceleration = configuration.get("default_deceleration",cls._default_deceleration)
        max_velocity = configuration.get("max_velocity",cls._max_velocity)
        max_acceleration = configuration.get("max_acceleration",cls._max_acceleration)
        optional_args = configuration.get("optional_args",dict())

        
        axis_id = configuration['axis_id']
        
                
        return Newport301Axis(ID,hardware,axis,default_position,home,name=n,description=d,**optional_args)


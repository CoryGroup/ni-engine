import config

class ControllerFactory(object):
    """
    Used for the manufacturing of controllers
    """
    _controller_builders = dict()

    def __init__(self,data_handler,hardware_manager,sensor_manager):
        self.hardware_manager = hardware_manager
        self.sensor_manager = sensor_manager
        self._data_handler = data_handler

    def create_controller(self,config):  
        """
        Creates a controller from configuration file.

        Parameters
        ----------
        config : Configuration

        Returns 
        -------
        AbstractController
        """      
        controllerCode = self.get_code(config)        
        hardware = self.get_hardware(config)
        sensors = self.get_sensors(config)        
        if controllerCode in ControllerFactory._controller_builders:
            return ControllerFactory._controller_builders[controllerCode].create(config,self._data_handler,hardware,sensors)        

        else:
            raise Exception("Controller Type: {0} not recognised".format(controllerCode))    

    def get_code(self,configuration):
        """
        Parameters
        ----------
        dictionary
            configuration dictionary
        Returns
        -------
        str
            Controller Code
        """
        return configuration[config.CODE]

    def get_hardware(self,configuration):
        """
        Parameters
        ----------
        dictionary
            configuration dictionary
        Returns
        -------
        AbstractHardware
            Hardware for controller
        """
        hardwareId = configuration[config.HARDWARE_ID]
        return self.hardware_manager.get_hardware(hardwareId)

    def get_sensors(self,configuration):
        """
        Parameters
        ----------
        dictionary
            configuration dictionary
        Returns
        -------
        AbstractSensor
            Sensors for controller
        """
        if config.SENSORSS_FOR_PLATFORM in configuration:
            sensorIDs = map(lambda x: x[config.SENSORS_ID],configuration[config.SENSORSS_FOR_PLATFORM])
            return dict(zip(sensorIDs,map(lambda x : self.sensor_manager.get_sensor(x),sensorIDs)))
        
        return dict()

    @classmethod
    def register_controller(cls,controller):
        """
        Register the controller for controller factory
        Example use in __init__.py:
        >>> ControllerFactory.register_controller(AbstractController)
        Parameters
        ----------
        AbstractController
        """
        code = controller.code
        cls._controller_builders[code]= controller
import config

class ControllerFactory(object):
    
    _controller_builders = dict()

    def __init__(self,hardware_manager,sensor_manager):
        self.hardware_manager = hardware_manager
        self.sensor_manager = sensor_manager

    def create_controller(self,config):        
        controllerCode = self.get_code(config)        
        hardware = self.get_hardware(config)
        sensors = self.get_sensors(config)        
        if controllerCode in ControllerFactory._controller_builders:
            return ControllerFactory._controller_builders[controllerCode].create(config,hardware,sensors)        

        else:
            raise Exception("Controller Type: {0} not recognised".format(controllerCode))    

    def get_code(self,configuration):
        return configuration[config.CODE]

    def get_hardware(self,configuration):
        hardwareId = configuration[config.HARDWARE_ID]
        return self.hardware_manager.get_hardware(hardwareId)

    def get_sensors(self,configuration):
        if config.SENSORSS_FOR_PLATFORM in configuration:
            sensorIDs = map(lambda x: x[config.SENSORS_ID],configuration[config.SENSORSS_FOR_PLATFORM])
            return dict(zip(sensorIDs,map(lambda x : self.sensor_manager.get_sensor(x),sensorIDs)))
        
        return dict()

    @classmethod
    def register_controller(cls,controller):
        code = controller.code
        cls._controller_builders[code]= controller
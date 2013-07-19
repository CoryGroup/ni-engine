import config


class SensorFactory(object):
    
    _sensorBuilders = dict()

    def __init__(self,hardware_manager):
        self.hardware_manager = hardware_manager        

    def create_sensor(self,config):        
        sensorCode = self.get_code(config)        
        hardware = self.get_hardware(config)        
        if sensorCode in SensorFactory._sensorBuilders:
            return SensorFactory._sensorBuilders[sensorCode].create(config,hardware)        

        else:
            raise Exception("Sensor Type not recognised")    

    def get_code(self,configuration):
        return configuration[config.CODE]

    def get_hardware(self,configuration):
        hardwareId = configuration[config.HARDWARE_ID]
        return self.hardware_manager.get_hardware(hardwareId)

    @classmethod
    def register_sensor(cls,sensor):
        code = sensor.code
        cls._sensorBuilders[code]= sensor
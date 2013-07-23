import config


class SensorFactory(object):
    
    _sensorBuilders = dict()

    def __init__(self,hardware_manager,data_handler):
        self.hardware_manager = hardware_manager    
        self._data_handler = data_handler    

    def create_sensor(self,config):        
        sensorCode = self.get_code(config)        
        hardware = self.get_hardware(config)        
        if sensorCode in SensorFactory._sensorBuilders:
            return SensorFactory._sensorBuilders[sensorCode].create(config,self._data_handler,hardware)        

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
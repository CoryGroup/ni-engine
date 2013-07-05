import config
class HardwareFactory(object):
    _hardwareBuilders = dict()
    

    def create_hardware(self,config):
        hardwareCode = self.get_code(config)                
        if hardwareCode in HardwareFactory._hardwareBuilders:
            return HardwareFactory._hardwareBuilders[hardwareCode].create(config)        

        else:
            raise Exception("hardware Type: {0} not recognised".format(hardwareCode))             

    def get_code(self,configuration):
        return configuration[config.CODE]
    
    @classmethod
    def register_hardware(cls,hardware):
        code = hardware.code
        HardwareFactory._hardwareBuilders[code]= hardware
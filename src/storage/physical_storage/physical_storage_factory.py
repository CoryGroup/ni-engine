import config


class StorageFactory(object):
    
    _storageBuilders = dict()
         

    def create_storage(self,configuration):        
        storageCode = self.get_code(configuration)               
        if storageCode in StorageFactory._sensorBuilders:
            return StorageFactory._storageBuilders[storageCode].create(configuration)        

        else:
            raise Exception("Storage Type not recognised")    

    def get_code(self,configuration):
        return configuration[config.CODE]    

    @classmethod
    def register_storage(cls,storage):
        code = storage.code
        cls._sensorBuilders[code]= sensor
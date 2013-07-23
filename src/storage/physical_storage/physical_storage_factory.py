import config
from abstract_physical_storage import AbstractPhysicalStorage

class StorageFactory(object):
    """
    Storage factory used to setup storage engine
    """
    _storageBuilders = dict()
         

    def create_storage(self,configuration):  
        """
        Sets up a storage engine from a configuration file

        Parameters
        ----------
        configuration : dictionary
        """      
        storageCode = self.get_code(configuration)        

        if storageCode in StorageFactory._storageBuilders:
            store = StorageFactory._storageBuilders[storageCode].create(configuration)    
            return store  

        else:
            raise Exception("Storage Type not recognised")    

    def get_code(self,configuration):
        """
        From configuration gets code of storage engine

        Parameters
        ----------
        configuration : dictionary
        """
        return configuration[config.CODE]    

    @classmethod
    def register_storage(cls,storage):
        """
        Used to register instances of `AbstractPhysicalStorage` with this factory class

        Parameters
        ----------
        storage : AbstractPhysicalStorage
        """
        code = storage.code
        cls._storageBuilders[code]= storage
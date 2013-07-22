
from physical_storage import StorageFactory

class data_handler(object):
    """
    Class that handles storage/retrieval of data in memory and in physical storage

    """

    def __init__(self,configuration):
        """
        Parameters
        ----------
        configuration : Configuration
            configuration file
        """

        self._storage_factory = StorageFactory(hardware_manager)
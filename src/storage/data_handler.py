
from physical_storage import StorageFactory

class DataHandler(object):
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
        self._hardware_data = DataDict()
        self._sensor_data = DataDict()
        self._controller_data = DataDict()
        self._data = {"hardware":self._hardware_data, "sensor" : self._sensor_data, "controller" : self._controller_data}

    def add_storage(self,storage_config):
        """
        Adds a physical storage manager
        
        Parameters
        ----------
        storage_config : dictionary
            Dictionary of configuration information for sensor
        """
        storage = self._storage_factory.create_storage(storage_config)

        if not isinstance(sensor,AbstractStorage):
            raise TypeError("Is not a physical-storage: {0}".format(type(sensor)))

        self._storage = storage
        

    def get_data(self,sensor):
        """
        Get data from a `AbstractSensor` object

        Parameters 
        ----------
        sensor : AbstractSensor
            Sensor object to retrieve data from

        Returns
        -------
        dictionary
            dictionary containing lists of `Measurement` objects
        """
        if sensor.id in self.measurements:
            return self.measurements[sensor.id]
        else: raise Exception("Sensor has no measurements available")
    
    def get_all_data(self,storage_type):
        """
        Gets all current measurement data

        Returns 
        -------
        dictionary
            Keys are device IDs at first level and measurement type at second level. 
            Data is list of measurement objects
        """
        if storage_type in self._data:
            return self._data[storage_type]
        else:
            ValueError("storage type: {0} does not exist".format(storage_type))

    

    def get_all_recent_data(self,storage_type):
        """
        Gets the most recent measurements of all sensors
        Parameters
        ----------
        storage_type : str or DataDict

        Returns
        -------
        dictionary
            Keys are sensor IDs and values are DataContainer. 
            Data are measurement objects.
        """

        if isinstance(storage_type,str):
            if storage_type in self._data:  
                storage_type= self._data[storage_type]        
        
        if isinstance(sensor_type,DataDict):
                data = storage_type
            
                curr = dict()
                for k,v in data:
                    curr[k] = v.all_recent_data()
                return curr
        else:
            ValueError("storage type: {0} does not exist".format(storage_type))
        
   
    

    def add_data(self,storage_type,ID,measurement_container):
        """
        Adds a measurement to proper `DataDict` based on it's ID. Also adds 
        it to be written to physical storage. 

        Parameters
        ----------
        storage_type : str
        ID : str
        measurement_container : AbstractDataContainer
        """
        if storage_type not in self._data:
            raise ValueError("storage type: {0} is not valid".format(storage_type))
        else:
            self._storage.store_measurement(storage_type,measurement_container)
            data_dict = self._data[storage_type]

    
    @classmethod
    def register_storage(cls,storage):
        """
        Class method called to register a physical storage engine with the storage factory. 
        This is than used for initialization based off configuration files.
        Should be called from __init__.py. 
        For example:
        >>> DataHandler.register_storage(AbstractPhysicalStorage)
        Will register the class so it can be used with storage engine
        """

        StorageFactory.register_storage(storage)
    
    @property     
    def hardware_data(self):
        """
        Returns
        -------
        DataDict
            hardware data object
        """
        return self._hardware_data

    @property 
    def sensor_data(self):
        """
        Returns
        -------
        DataDict
            sensor data object
        """
        return self._sensor_data

    @property 
    def controller_data(self):
        """
        Returns
        -------
        DataDict
            controller data object
        """
        return self._controller_data

    @property 
    def data(self):
        """
        Returns 
        -------
        dict{str : DataDict}


        """
        return self._data

    @property 
    def storage(self):
        """
        Returns 
        -------
        AbstractPhysicalStorage
        """
    @property 
    def recent_controller_data(self):
        """
        Get most recent controller data

        Returns 
        -------
        dictionary
            keys are device controller id and datacontainers are values
        """
        return self.get_all_recent_data(self.controller_data)

    @property 
    def recent_sensor_data(self):
        """
        Get most recent sensor data

        Returns 
        -------
        dictionary
            keys are device sensor id and datacontainers are values
        """
        return self.get_all_recent_data(self.sensor_data)

    @property 
    def recent_hardware_data(self):
        """
        Get most recent hardware data

        Returns 
        -------
        dictionary
            keys are device hardware id and datacontainers are values
        """
        return self.get_all_recent_data(self.hardware_data)



class DataDict(dict):
    """
    Holder for in-memory storage of measurements
    """
    def __init__(self,source,*arg,**kw):
        """
        Parameters
        ----------
        source : str 
            String for source of storage, ie. controller,sensor hardware
        """
        self._source = source
        super(DataDict,self).__init__(*arg,**kw)

    def add_data(self,ID,measurement_container):
        assert isinstance(measurement_container,AbstractDataContainer)

        if ID in self:
            self[ID] = self[ID] + measurement_container
        else:
            self[ID] = measurement_container
    @property
    def source(self):
        """
        Getter/setter for source parameter
        """
        return self._source
    @source.setter
    def source(self, source):
        self._source = source
    
    
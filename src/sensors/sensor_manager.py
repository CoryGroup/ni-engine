from sensor_factory import SensorFactory
from abstract_sensor import AbstractSensor

class SensorManager(object):
    """
    Class to manage all sensors. Initializes
    and stores sensors as well as handles measurements from them.
    All from configuration files given to it
    """
    def __init__(self,configuration,data_handler,hardware_manager): 
        """
        Parameters
        ----------
        configuration : configuration
            Object containing all configuration information for project
        hardware_manager : HardwareManager 
            Contains all hardware created from configuration file

        """               
        self.configuration = configuration
        self.sensors = dict()
        self._data_handler = data_handler
        self.sensor_factory = SensorFactory(hardware_manager,self._data_handler)
        self.measurements = dict()
        self.store_measurements = self.configuration.store_measurements
        

    def add_sensor(self,sensor_config):
        """
        Adds a sensor based on config and stores it in the sensor manager
        
        Parameters
        ----------
        sensor_config : dictionary
            Dictionary of configuration information for sensor
        """
        sensor = self.sensor_factory.create_sensor(sensor_config)

        if not isinstance(sensor,AbstractSensor):
            raise TypeError("Is not a sensor: {0}".format(type(sensor)))

        self.sensors[sensor.id] = sensor
        sensor.connect()

    def remove_sensor(self,sensor):
        """
        Removes a sensor from manager

        Parameters
        ----------
        sensor : AbstractSensor or str
            a class implementing `AbstractSensor` or a string_id
        """
        if isinstance(sensor,AbstractSensor): 
            del self.sensors[sensor.id]
            sensor.disconnect()
        elif isinstance(sensor,str):
            sensor = self.sensors[sensor]
            del self.sensors[sensor]
            sensor.disconnect()
        else: raise ValueError("Must give valid object")      

    def remove_all(self):
        """
        Removes all sensors
        """
        for k,v in self.sensors.iteritems():
            v.disconnect()
        self.sensors = dict()

    def parse_factory_yaml(self,config_yaml):
        """
        Returns relevent yaml for `SensorFactory`
        """
        return config_yaml

    def add_all_sensors(self):
        """
        Adds all sensors in configuration
        """
        for x in self.configuration.sensors:
            self.add_sensor(x)

    
        

    def get_data(self,sensor):
        """
        Get data from a `AbstractSensor` object

        Parameters 
        ----------
        sensor : AbstractSensor or str
            Sensor object to retrieve data from

        Returns
        -------
        dictionary
            dictionary containing lists of `Data` objects
        """
        if isinstance(sensor,AbstractSensor):
            sensor = sensor.id
        return self._data_handler.sensor_data[sensor]
    
    def get_all_data(self):
        """
        Gets all current measurement data

        Returns 
        -------
        dictionary
            Keys are sensor IDs at first level and measurement type at second level. 
            Data is list of measurement objects
        """
        self._data_handler.sensor_data

    def get_all_current_data(self):
        """
        Gets the most recent measurements of all sensors

        Returns
        -------
        dictionary
            Keys are sensor IDs at first level and measurement type at second level. 
            Data are measurement objects.
        """
        return self._data_handler.recent_sensor_data

    def get_most_recent_data(self,sensor):
        """
        Gets the current data of a sensor

        Parameters
        ----------
        sensor : str or AbstractSensor

        Returns 
        -------
        dictionary
            Current data by measurement
        """
        if isinstance(sensor,AbstractSensor):
            sensor = sensor.id
        return self._data_handler.sensor_data[sensor].all_recent_data()

    def measure(self,sensor):
        """
        Measures a sensor

        Parameters
        ----------
        sensor : AbstractSensor or str 

        Returns
        -------
        AbstractMeasurementContainer

        """

        if isinstance(sensor,str):
            sensor = self.get_sensor(sensor)        
        elif not isinstance(sensor,AbstractSensor):
            raise TypeError ("Sensor: {0} is not subclass of AbstractSensor".format(type(sensor)))

        

        
        
        measurement = sensor.measure()
        if self.store_measurements:                      
            self._data_handler.add_sensor_data(sensor.id,measurement)   

                
        return measurement
    
    def measure_all(self):
        """
        Measure all sensors 

        Returns
        -------
        DataDict
            Contains all AbstractMeasurementContainers for measurements. Dictionary keys by sensor ids. 
        """
        for k,v in self.sensors.iteritems():            
            self.measure(v)
        return self._data_handler.sensor_data


    def get_sensor(self,sensor_id):
        """
        Gets a sensor based on its ID string_id

        Parameters
        ----------
        ID : str
            ID string of sensor

        Returns 
        -------
        AbstractSensor

        """
        if ID in self.sensors:
            return self.sensors[ID]
        else: raise ValueError("No Sensor exists for id: {0}".format(ID))


    @classmethod
    def register_sensor(cls,sensor):
        SensorFactory.register_sensor(sensor)
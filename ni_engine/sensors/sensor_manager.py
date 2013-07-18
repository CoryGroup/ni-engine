from sensor_factory import SensorFactory
from abstract_sensor import AbstractSensor

class SensorManager(object):
    """
    Class to manage all sensors. Initializes
    and stores sensors as well as handles measurements from them.
    All from configuration files given to it
    """
    def __init__(self,configuration,hardware_manager): 
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
        self.sensor_factory = SensorFactory(hardware_manager)
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

    def get_sensor_by_id(self,ID):
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
    
    def get_all_data(self):
        """
        Gets all current measurement data

        Returns 
        -------
        dictionary
            Keys are sensor IDs at first level and measurement type at second level. 
            Data is list of measurement objects
        """
        return self.measurements

    def get_all_current_data(self):
        """
        Gets the most recent measurements of all sensors

        Returns
        -------
        dictionary
            Keys are sensor IDs at first level and measurement type at second level. 
            Data are measurement objects.
        """
        curr = dict()
        for k in self.measurements:
            sen = self.get_sensor_by_id(k)
            curr[k] = self.get_most_recent_data(sen)

    def get_most_recent_data(self,sensor):
        if sensor.id in self.measurements:
            data =  self.measurements[sensor.id]
            recentData = dict()
            for k,v in data.items():
                recentData[k]= v[-1]
            return recentData
        else: raise Exception("Sensor has no measurements available")

    def measure(self,sensor):
        if sensor.id not in self.measurements:
            sensorMeasurement = dict()
            self.measurements[sensor.id]= sensorMeasurement
        else:
            sensorMeasurement = self.measurements[sensor.id]

        if self.store_measurements:
            measurement = sensor.measure()
            for k,v in measurement.items():
                if k in sensorMeasurement:
                    sensorMeasurement[k].append(v)
                else:
                    if not isinstance(v,list):
                        sensorMeasurement[k] = [v]
                    else:
                        sensorsMeasurement[k] = v
        else:
            measurement = sensor.measure()
            sensorMeasurement = dict()
            for k,v in measurement.items():
                if not isinstance(v,list):
                    sensorMeasurement[k] = [v]
                else:
                    sensorMeasurement[k] = v
                    
        return self.get_data(sensor)
    def measure_all(self):
        for k,v in self.sensors.items():
            self.measure(v)
        return self.get_all_data()


    def get_sensor(self,sensor_id):
        if sensor_id in self.sensors:            
            return self.sensors[sensor_id]
        else: raise ValueError("{0} is not a valid sensor id".format(sensor_id))


    @classmethod
    def register_sensor(cls,sensor):
        SensorFactory.register_sensor(sensor)
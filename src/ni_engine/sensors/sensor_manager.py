from sensor_factory import SensorFactory
from abstract_sensor import AbstractSensor
from concurrent import futures
import inspect


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
        self._store_measurements = self.configuration.store_data
        self._max_workers = self.configuration.max_workers

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
            dictionary containing lists of `data` objects
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
            data is list of measurement objects
        """
        self._data_handler.sensor_data

    def get_all_current_data(self):
        """
        Gets the most recent measurements of all sensors

        Returns
        -------
        dictionary
            Keys are sensor IDs at first level and measurement type at second level. 
            data are measurement objects.
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

    def measure(self,sensors,compound=False):
        """
        Measures a list of sensors or single sensor

        Parameters
        ----------
        sensor : AbstractSensor or str 

        Returns
        -------
        [`DataContainer`] or singleton `DataContainer` if only single sensor

        """
        is_list = True
        if not isinstance(sensors,list):
            is_list = False
            sensors = [sensors]
        for idx,sen in enumerate(sensors):
            if isinstance(sen,str):
                sensors[idx] = self.get_sensor(sen)        
            elif not isinstance(sen,AbstractSensor):
                raise TypeError ("Sensor: {0} is not subclass of AbstractSensor".format(type(sen)))
        # generate list of measurement functions to be executed
        function_list = map(lambda x: (x.measure,x.threadsafe),sensors)  
        # execute the functions
        results = self.execute_functions(function_list,compound)
        # return singleton if only 1 object
        if len(results)==1 and not is_list:            
            key, value = results.popitem()
            results = value
        return results
    
    def measure_all(self,compound=False):
        """
        Measure all sensors 

        Returns
        -------
        DataDict
            Contains all AbstractMeasurementContainers for measurements. Dictionary keys by sensor ids. 
        """
        result = self.measure(self.sensors.values(),compound)

        return result

    def execute_functions(self,fns,compound=False):
        """
        Execute a series as functions passed as lambda expressions and store there results.
        The functions must either return a DataContainer or a future that will eventually return
        a data container. All data containers will than be stored

        Parameters
        ----------
        fns : list (tuple(function,threadsafe))

        Returns 
        -------
        dict[id] = `DataContainer`
        """
        # make sure is list
        if not isinstance(fns,list):
            fns = [fns]
        # store methods
        methods = []
        # store methods to be futures
        fut = []
        for (func,threadsafe) in fns:
            #make sure is a function
            
            assert inspect.ismethod(func) or inspect.isfunction(func)
            # if threadsafe add to futures
            if threadsafe: fut.append(func)
            # if not threadsafe add to normal methods
            else: methods.append(func)

        executor = futures.ThreadPoolExecutor(max_workers=self._max_workers)
        #execute all futures and store in list
        future_list = map(lambda x : executor.submit(x),fut) 
        # execute all methods
        method_results = map(lambda x : x(),methods) 
        # wait for all futures to finish 
        futures.wait(future_list,)
        #get all results of futures
        future_results = map(lambda x : x.result(),future_list)
        results = future_results + method_results

        #store measurements if turned on 
        if self._store_measurements:
            for mes in results:

                self._data_handler.add_sensor_data(mes.id,mes,compound=compound)

        return dict((v.id, v) for v in results)

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
        if sensor_id in self.sensors:
            return self.sensors[sensor_id]
        else: raise ValueError("No Sensor exists for id: {0}".format(sensor_id))


    @classmethod
    def register_sensor(cls,sensor):
        SensorFactory.register_sensor(sensor)
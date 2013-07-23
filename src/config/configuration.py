import yaml 
import os 
import sys
import config_variables as config
class Configuration(object):
    """
    Class to read configuration file and handle 
    offloading of configuration information to other
    classes as required.

    *Sample available interfaces file:*

    .. literalinclude:: ../examples/conf/available_interfaces.yml
        :language: YAML

    *Sample interfaces file:*

    .. literalinclude:: ../examples/conf/test.yml
        :language: YAML

    """

    
    def __init__(self,availableInterfaces,**kwargs):
        """
        Initializes configuration. 



        Parameters
        ----------

        availableInterfaces : str
            File path to string containing available hardware,controllers and sensors

        kwargs : dict
            Optional argument of "configFile" to pass a configuration file now
        """
        self.availableInterfaces = availableInterfaces
        if 'configFile' in kwargs:
            self.configFile = kwargs['configFile']
        inter = open(self.availableInterfaces,'r')
        interfaces = yaml.load(inter)        
        self.availableSensors = interfaces[config.SENSORS]
        self.availableHardware = interfaces[config.HARDWARE] 
        self.availableControllers = interfaces[config.CONTROLLERS]

    def read_config(self,configFile=None):
        """
        Read in a configuration file and validate/extract information

        Parameters
        ----------
        configFile : str         
            A string containing path to a yaml configuration file

        """
        if configFile:
            self.configFile = configFile
        if not self.configFile:
            raise ValueError("ConfigFile must be set")

        file = open(self.configFile,'r')

        self.yamlConfig = yaml.load(file)

        self._sensors = self.yamlConfig[config.SENSORS]

        self._hardware = self.yamlConfig[config.HARDWARE]

        self._controllers = self.yamlConfig[config.CONTROLLERS]

        self._configuration = self.yamlConfig[config.CONFIGURATION]

        if self.validate_config():
            return True
        else:
            raise ValueError("Configuration files submitted are not valid. Cannot continue. Exiting...")
            sys.exit(1)

    @property
    def sensors(self):
        """
        Returns dictionary of sensors in configuration file

        Returns 
        -------
        dict
        """
        return self._sensors

    @property 
    def hardware(self):
        """
        Returns dictionary of hardware in configuration file

        Returns 
        -------
        dict
        """
        return self._hardware

    @property 
    def controllers(self):
        """
        Returns dictionary of controllers in configuration file

        Returns 
        -------
        dict
        """
        return self._controllers

    @property 
    def required_sensors(self): 
        hard =[]
        for x in self._sensors:
            if config.CODE in x:
                hard.append(x[config.CODE])
            else:  
                raise ValueError("All sensors must have sensor code in configuration")
        return hard

    @property 
    def required_hardware(self): 
        hard =[]
        for x in self._hardware:
            if config.CODE in x:
                hard.append(x[config.CODE])
            else:  
                raise ValueError("All hardware must have sensor code in configuration")
        return hard

    @property
    def required_controllers(self): 
        hard =[]
        for x in self._controllers:
            if config.CODE in x:
                hard.append(x[config.CODE])
            else:  
                raise ValueError("All controllers must have sensor code in configuration")
        return hard
    


    def are_valid_sensor_referenced(self,required_sensors):        

        for x in required_sensors:
            if x not in self.availableSensors:
                raise ValueError("Not all sensor references are valid")
                return False
            elif not self.availableSensors[x][config.IS_ON]:
                raise ValueError("Sensor not enabled")
                return False
        return True

    def are_valid_controllers_referenced(self,required_controllers):        

        for x in required_controllers:
            if x not in self.availableControllers:
                raise ValueError("Not all controller references are valid")
                return False
            elif not self.availableControllers[x][config.IS_ON]:
                raise ValueError("Controller not enabled")
                return False
        return True

    def is_valid_hardware_referenced(self,required_hardware):        

        for x in required_hardware:
            if  x not in self.availableHardware:
                raise ValueError("Not all hardware references are valid")
                return False
            elif not self.availableHardware[x][config.IS_ON]:
                raise ValueError("Hardware not enabled")
                return False
        return True

    # Takes a configuration to reference hardware by token: hardwareID
    def are_sensor_reference_to_hardware_valid(self,referenceConfig):
        idDict = dict()
        for x in self._hardware:            
            idDict[x[config.ID]] = x
        for y in referenceConfig:            
            if config.HARDWARE_ID not in y:
                print y
                print config.HARDWARE_ID
                raise ValueError("Sensor: {0} does not have hardware_id parameter".format(y[config.ID] ))
                return False                  
            elif y[config.HARDWARE_ID] not in idDict:
                raise ValueError("Sensor: {0} reference id does not have hardware match".format(y[config.HARDWARE_ID] ))
                return False
            elif y[config.CODE] not in self.availableHardware[idDict[y[config.HARDWARE_ID]][config.CODE]][config.SENSORSS_FOR_PLATFORM]:
                raise ValueError("Sensor: {0} not available for platform".format(y[config.HARDWARE_ID] ))
                return False
            elif  not self.availableHardware[idDict[y[config.HARDWARE_ID]][config.CODE]][config.SENSORSS_FOR_PLATFORM][y[config.CODE]][config.IS_ON]:
                raise ValueError("Sensor: {0} not enabled for platform".format(y[config.HARDWARE_ID] ))
                return False

        return True

    def are_controller_reference_to_hardware_valid(self,referenceConfig):
        idDict = dict()
        for x in self._hardware:            
            idDict[x[config.ID]] = x
        for y in referenceConfig:   
            if config.HARDWARE_ID not in y:
                raise ValueError("Controller: {0} does not have hardware_id parameter".format(y[config.ID] ))
                return False        
            elif y[config.HARDWARE_ID] not in idDict:
                raise ValueError("Controller: {0} reference id does not have hardware match".format(y[config.HARDWARE_ID] ))
                return False
            elif y[config.CODE] not in self.availableHardware[idDict[y[config.HARDWARE_ID]][config.CODE]][config.CONTROLLERS_FOR_PLATFORM]:
                raise ValueError("Controller: {0} not available for platform".format(y[config.HARDWARE_ID] ))
                return False
            elif  not self.availableHardware[idDict[y[config.HARDWARE_ID]][config.CODE]][config.CONTROLLERS_FOR_PLATFORM][y[config.CODE]][config.IS_ON]:
                raise ValueError("Controller: {0} not enabled for platform".format(y[config.HARDWARE_ID] ))
                return False

        return True

    def are__reference_to_sensor_valid(self,referenceConfig):
        idDict = dict()
        for x in self._sensors:            
            idDict[x[config.ID]] = x

        for x in referenceConfig:
            if config.SENSORSS_FOR_PLATFORM in x:        
                for y in x[config.SENSORSS_FOR_PLATFORM]:        
                    if y[config.SENSORS_ID] not in idDict:
                        raise ValueError("Sensor reference id does not have hardware match")
                        return False
                

        return True

    def validate_config(self):
        sensorVal = self.are_valid_sensor_referenced(self.required_sensors)
        hardwareVal = self.is_valid_hardware_referenced(self.required_hardware)
        controllerVal = self.are_valid_controllers_referenced(self.required_controllers)
        crossRefSensorHardwareVal = self.are_sensor_reference_to_hardware_valid(self._sensors)
        crossRefControllerHardwareVal = self.are_controller_reference_to_hardware_valid(self._controllers)
        refToSensors = self.are__reference_to_sensor_valid(self._controllers)
        
        if sensorVal and hardwareVal and controllerVal and crossRefSensorHardwareVal and \
        crossRefControllerHardwareVal and refToSensors:
            return True
        
        return False


    @property
    def store_measurements(self):
        """
        Check to see if measurements should be stored in a storage engine

        Returns
        -------
        bool
        """
        if config.STORE_MEASUREMENTS in self._configuration:
            return self._configuration[config.STORE_MEASUREMENTS]
        else: 
            return False

    @property
    def storage_config(self):
        """
        Returns the storage engine configuration. If none is in configuration file uses a `TestPhysicalStorage` storage manager

        Returns 
        -------
        dictionary
        """

        if config.STORAGE in self._configuration:
            return self._configuration[config.STORE_MEASUREMENTS]
        else:
            print "No storage engine defined in configuration file. Using TestPhysicalStorage storage manager"
            return {config.CODE : "TESTSTORAGE"}

    


from sensor_factory import SensorFactory


class SensorManager(object):
    
    def __init__(self,configuration,hardware_manager):                
        self.configuration = configuration
        self.sensors = dict()
        self.sensor_factory = SensorFactory(hardware_manager)
        self.measurements = dict()
        self.store_measurements = self.configuration.store_measurements
        
    def add_sensor(self,sensor_config):
        sensor = self.sensor_factory.create_sensor(sensor_config)
        self.sensors[sensor.id] = sensor
        sensor.connect()

    def remove_sensor(self,sensor):
        if sensor: 
            del self.sensors[sensor.id]
            sensor.disconnect()

        else: raise ValueError("Must give valid object")
    
    def remove_sensor_by_name(self,sensor_name):
        if sensor_name: 
            sensor = self.sensors[sensor_name]
            del self.sensors[sensor_name]
            sensor.disconnect()

        else: raise ValueError("Must give valid name")

    def remove_all(self):
        for k,v in self.sensors.iteritems():
            v.disconnect()
        self.sensors = dict()

    def parse_factory_yaml(self,config_yaml):
        return config_yaml

    def add_all_sensors(self):
        for x in self.configuration.sensors:
            self.add_sensor(x)

    def get_sensor_by_id(self,ID):
        if ID in self.sensors:
            return self.sensors[ID]
        else: raise ValueError("No Sensor exists for id: {0}".format(ID))

    def get_data(self,sensor):
        if sensor.id in self.measurements:
            return self.measurements[sensor.id]
        else: raise Exception("Sensor has no measurements available")
    
    def get_all_data(self):
        return self.measurements

    def get_all_current_data(self):
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
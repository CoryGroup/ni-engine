from datetime import datetime
import quantities as pq
class Measurement(object):
    """
    Measurement class for storing measurements taken from sensors. 
    Passed around by the ni-engine system
    """
    def __init__(self,sensor_id,sensor_code,measurement_name,value,time=datetime.now()):
        """
        :param str sensor_id: The ID of sensor from which measurement was taken
        :param str sensor_code: The code for sensor type which measurement comes from
        :param str measurement_name: Description of the measurement
        :param quantity.Quantity value: The value measured 
        :param datetime.datetime time: The time at which the measurement was taken
        """
        # Value must be of type pq.quantity
        assert type(value) is pq.Quantity

        self.sensor_id = sensor_id
        self.sensor_code = sensor_code
        self.measurement_came = measurement_name
        self.value = value 
        self.time = time

    def __lt__(self,other):
        """
        Allow ordering based on time of measurements
        """
        return self.time < other.time
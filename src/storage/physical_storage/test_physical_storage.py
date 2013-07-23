import config 
from abstract_physical_storage import AbstractPhysicalStorage

class TestPhysicalStorage(AbstractPhysicalStorage):
    """
    Abstract physical storage class that must be implemented by all 
    physical storage mediums. 
    """
    code = "TESTSTORAGE"
    def init(self):
        self._measurements= list()

    

    
    

    
    def write_measurement(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter
        """

        data_to_write = queue.get_all()
        print data_to_write
        self.append(data_to_write)
        
   





    @classmethod
    def create(cls,configuration):
        """
        Takes configuration, generates object of storage engine and returns it.

        Parameters
        ----------
        configuration : dictionary
            Configuration dictionary

        Returns 
        -------
        TestPhysicalStorage
            Object of class with correct configuration information
        """
        return TestPhysicalStorage()

  
      

    @property 
    def storage_code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        return TestPhysicalStorage.code
        



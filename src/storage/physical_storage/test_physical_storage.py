
import config 
from abstract_physical_storage import AbstractPhysicalStorage

class TestPhysicalStorage(AbstractPhysicalStorage):
    """
    Abstract physical storage class that must be implemented by all 
    physical storage mediums. 
    """
    code = "TESTSTORAGE"
    
    def __init__(self,buffer_size):
        super(TestPhysicalStorage,self).__init__()
        self._measurements= []
        self.buffer_size = buffer_size
    

    
    

    
    def write_data(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """

        data_to_write = queue.get_all()  
        print "writing"
        print data_to_write      
        self._measurements.append(data_to_write)
        
    def write_compound(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """
        data_to_write = queue.get_all()
        data_to_write = map(lambda x:x.compound(),data_to_write)  
        print "writing"
        print data_to_write      
        self._compound.append(data_to_write)




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
        buffer_size = configuration.get('buffer_size',10)
        return TestPhysicalStorage(buffer_size)

  
      

    @property 
    def storage_code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        return TestPhysicalStorage.code
        



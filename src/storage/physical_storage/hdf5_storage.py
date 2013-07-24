
from abstract_physical_storage import AbstractPhysicalStorage
import tables 
import numpy as np
import config
import quantities as pq




class HDF5Storage(AbstractPhysicalStorage):

    """
    HDF5 data storage engine. 
    """
    code = "HDF5"

    def __init__(self,file_path,title="Ni-Engine Data",buffer_size=100):
        self._measurements= []
        self.buffer_size = buffer_size
        self._file = tables.open_file(file_path,mode='a',title= title)
        self._root = self._file.root
        self._hardware = self.get_or_create_group(self._root,"hardware","Hardware Data Acquired")
        self._sensors = self.get_or_create_group(self._root,"sensors","Sensor Data Acquired")
        self._controllers = self.get_or_create_group(self._root,"controllers","Controllers Data Acquired")
        self._groups = {"hardware": self._hardware,"sensors" : self._sensors,
                        "controllers":self._controllers}
        
    
    def get_or_create_group(self,parent,group_name,title=None):
        """
        From the HDF5 file, get a group as tables group if it exists
        otherwise create a new one.

        Parameters
        ----------
        parent : tables.group.Group
            Parent where to look for group underneath 
        group_name : str
            Name of group to search or create
        title : str
            title of group to be created

        Returns 
        -------
        tables.group.Group , bool
            boolean signifies whether the group had to be created
        """
        if title is None:
            title = group_name

        if hasattr(parent,group_name):
            return getattr(parent,group_name) , False
        else:
            return self._file.create_group(parent,group_name,title) , True

    def get_or_create_table(self,parent,table_name,description,title=None):
        """
        From the HDF5 file, get a group as tables group if it exists
        otherwise create a new one.

        Parameters
        ----------
        parent : tables.group.Group
            Parent where to look for group underneath 
        table_name : str
            Name of table to search or create
        title : str
            title of table to be created
        description : str 

        Returns 
        -------
        tables.group.Group , bool
            boolean signifies whether the group had to be created
        """
        if title is None:
            title = table_name

        if hasattr(parent,table_name):
            return getattr(parent,table_name) , False
        else:
            print description
            return self._file.create_table(parent,table_name,description,title=title) , True
        
    def write_measurement(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """

        data_to_write = queue.get_all()  
        print data_to_write
        for data in data_to_write:
            group = self._groups[data[0]]
            data_container = data[1]
            for k,v in data_container.iteritems():                
                table = self.generate_table_from_measurement(group,k,v[0])
                for x in np.nditer(v):
                    self.create_measurement(table,x)
                table.flush()




        
    def create_measurement(self,table,measurement):
        """
        Create a pytables entry and append it to be written

        Parameters
        ----------
        table : tables.Table
        measurement : Measurement
        """
        table["time"] = measurement.time
        if isinstance(measurement.value,pq.Quantity):
            table["value"] = float(measurement.value)
        else:
            table["value"] = measurement.value

        table.append()

    def generate_table_from_measurement(self,group,name,measurement):
        # is shallow copy, this way we don't mess up for other objects
        table_dict = {}
        table_dict["time"] = tables.Time64Col()
        if isinstance(measurement.value,pq.Quantity):
            table_dict["value"] = tables.Float64Col()
            table_dict["units"] = tables.StringCol(20)
        elif isinstance(measurement.value,bool):
            table_dict["value"] = tables.BoolCol()
        elif isinstance(measurement.value,str):
            table_dict["value"] = tables.StringCol(50)
        elif isinstance(measurement.value,float):
            table_dict["value"] = tables.Float64Col()
        elif isinstance(measurement.value,int):
            table_dict["vlaue"] = tables.Int32Col()

        table = self.get_or_create_table(group,name,table_dict,name)
        table.attrs.name = measurement.name
        table.attrs.id = measurement.id
        table.attrs.code = measurement.code 
        if isinstance(measurement.value,pq.Quantity):
            table.attrs.units = measurement.value.units
        return table

    def close(self):
        self._file.close()

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
        HDF5Storage
            Object of class with correct configuration information
        """
        buffer_size = configuration.get('buffer_size',10)
        file_path = configuration.get('file_path')
        name = configuration.get('name',"Ni-Engine Data")
        return HDF5Storage(file_path,name,buffer_size)

  
      

    @property 
    def storage_code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        return HDF5Storage.code
        



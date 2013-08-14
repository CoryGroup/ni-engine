import tables 
import numpy as np
import quantities as pq
import time
import datetime
import config
from flufl.enum import IntEnum
from abstract_physical_storage import AbstractPhysicalStorage
from ..data_dict import DataDict
from ..data_container import DataContainer
from ..data_value import Data,data


class UnitType(IntEnum):
    """
    Types of units supported
    """
    base_unit = 5
    quantity = 10


class HDF5Storage(AbstractPhysicalStorage):

    """
    HDF5 data storage engine. 
    """
    code = "HDF5"
    REMOVE = set("""/!@#$%^&*()+=`~,.\\|:"'; '""")
    def __init__(self,file_path,title="Ni-Engine Data",buffer_size=100,new_file=False,past_data_file=None):
        super(AbstractPhysicalStorage,self).__init__()
        self._measurements= []
        self.buffer_size = buffer_size
        write_code = 'w' if new_file else 'a' 

        self._file = tables.open_file(file_path,mode=write_code,title= title)
        self._root = self._file.root
        self._hardware, h_created = self.get_or_create_group(self._root,"hardware","Hardware Data Acquired")
        self._sensors, s_created = self.get_or_create_group(self._root,"sensors","Sensor Data Acquired")        
        self._controllers, c_created = self.get_or_create_group(self._root,"controllers","Controllers Data Acquired")
        self._compound , com_created = self.get_or_create_group(self._root,"compound", "Compound data")
        self._groups = {"hardware": self._hardware,"sensors" : self._sensors,
                        "controllers":self._controllers,"compound":self._compound}

        self._past_data_file = past_data_file

    def retrieve_data(self,number_elems):
        if self._past_data_file is None:
            raise AttributeError("The olf file path was not set. It appears there is an issue with \
                the configuration file")
        return self.build_data_from_file(self._past_data_file,number_elems)

    @classmethod 
    def build_data_from_file(self,file_path,number_elems=None):
        """
        Builds dictionary of data data containers from HDF5 file.
        
        Note: there is definitely lots of room for improvement for 
        efficency, uses way to much reflection and probably unecessary 
        loops.

        Example of returned dictionary:
        >>> {"sensors":{"temp1":DataContainer},"hardware":{},"controllers":{}}

        Parameters
        ----------
        file_path : str
            path to file
        number_elems: int
            number of elements to grab from file

        Returns
        -------
        dict
            

        """
        data_file = tables.open_file(file_path,mode='r')
        root = data_file.root
        try:
            sensors = root.sensors
            controllers = root.controllers
            hardware = root.hardware
            compound = root.compound
            g = {'sensors': sensors,'controllers': controllers,'hardware':hardware,"compound":compound}
        except Exception,e: 
            print "Does not appear to be valid ni-engine file"
            raise 

        old_data = {}
        for k,v in g.iteritems():
            old_data[k] = DataDict(k)
            #go through groups of devices
            for devices in data_file.listNodes(v):
                #go through tables of devices
                container = DataContainer("",number_elems)

                for table in data_file.listNodes(devices):
                    
                    title = table.attrs.TITLE
                    ID = table.attrs.id
                    code = table.attrs.code
                    name = table.attrs.name
                    quant = table.attrs.quantities
                    metadata = table.attrs.metadata
                    temp_con = DataContainer(ID,number_elems)
                    compound = table.attrs.compound
                    #cycle through last number_elems in data set
                    if number_elems is None or number_elems<0:
                        to_cycle = table
                    else :
                        to_cycle = table[-number_elems:]
                    for data_dict in to_cycle:
                        #cycle through meta data of table
                        for data_name,type_data in metadata.iteritems():                            
                            if type_data is UnitType.quantity:
                                arr = []

                                for x in range(quant[data_name]):
                                    arr.append(data_dict[data_name+"_"+str(x)])
                                value = pq.Quantity(arr,data_dict[data_name+'_units'])
                            elif type_data is UnitType.base_unit:
                                value = data_dict[data_name]
                            else:
                                raise ValueError("Not valid UnitType")
                            if compound:
                                time_seconds = data_dict[data_name+"_time"]
                            else:
                                time_seconds = data_dict['time']
                            time = datetime.datetime.fromtimestamp(time_seconds)                  

                            temp_con.add_measurement(title,data(ID,code,name,value,time))

                    container = temp_con + container

                old_data[k][container.id] = container

        return old_data


    
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
        (tables.group.Group , bool)
            boolean signifies whether the group had to be created
        """
        if title is None:
            title = group_name
        string_to_modify = 'this is a string'

        group_name= ''.join(x for x in group_name if x not in self.REMOVE)

        if hasattr(parent,group_name):
            a= getattr(parent,group_name)            
            return a , False
        else:                        
            return self._file.create_group(parent,group_name,title),True

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
        table_name= ''.join(x for x in table_name if x not in self.REMOVE)
        if hasattr(parent,table_name):
            return getattr(parent,table_name) , False
        else:               
            return  self._file.create_table(parent,table_name,description,title), True
    

    def write_data(self,queue):
        """
        Is called when the number of measurements in measurement queue
        is greater than the bulk_write parameter

        Parameters
        ----------
        queue : ItemStore
        """

        data_to_write = queue.get_all()  

        for data in data_to_write:            
            data_class = self._groups[data[0]]   
            data_container = data[1]
            group , was_created = self.get_or_create_group(data_class,data_container.id) 
            
            for k,v in data_container.iteritems():                
                table, table_created = self.generate_table_from_measurement(group,k,v[0])    
                row = table.row            
                for x in v.flat:                    
                    self.create_measurement(row,x)
                table.flush()


    def write_compound(self,queue):
        data_to_write = queue.get_all()
        
        compound = map(lambda x: x[1].compound(),data_to_write)        
        for x in zip(data_to_write,compound):
            data_class = self._groups[x[0][0]]
            data_container = x[0][1] 
                      
            compound_data = x[1]
            
            group , was_created = self.get_or_create_group(data_class,data_container.id)
            table , table_created = self.generate_table_from_compound(group,data_container.id,compound_data)
            row = table.row
                           
                
                
            self.create_compound(row,compound_data)
            table.flush()

    def write_quantity(self,row,quantity,index=""):
        for idx,x in enumerate(quantity.magnitude):
            row[index+str(idx)] = float(x)
        row[index+"units"] = quantity.dimensionality.string
        return row

    def _quantity_dict(self,table_dict,quantity,index=""):
        for idx,x in enumerate(quantity.magnitude):
            table_dict[index+str(idx)] = tables.Float64Col()
        table_dict[index+"units"] = tables.StringCol(20)
        return table_dict
    
        
    def create_measurement(self,row,measurement):
        """
        Create a pytables entry and append it to be written

        Parameters
        ----------
        row : tables.Table.row
        measurement : Data
        """
        
        # gets the time since Jan 1, 1970 in floating point seconds
        row["time"] = time.mktime(measurement.time.timetuple())+measurement.time.microsecond/1000000.
        if isinstance(measurement.value,pq.Quantity):
            self.write_quantity(row,measurement.value,measurement.name+"_")
        else:
            row[measurement.name] = measurement.value

        row.append()

    def create_compound(self,row,compound):
        """
        Creates a pytables entry and appends it to be written
        from a list of measurements 

        Parameters
        ----------
        row : tables.Table.row
        compound: list(Data)
        """

        for x in compound:
            row["{0}_time".format(x.name)] = time.mktime(x.time.timetuple())+x.time.microsecond/1000000.
            if isinstance(x.value,pq.Quantity):
                write_quantity(row,measurement.value,x.name+"_")
            else:
                row["{0}".format(x.name)] = x.value

        row.append()

    def generate_table_from_measurement(self,group,name,measurement):
        """
        Generates a hdf5 table from a measurement object

        Parameters
        ----------
        group : tables.Group or str
        name : str
            name of the table
        measurement : Data 

        Returns
        (tables.Table,bool)
            returns the table and a boolean to signify if it was found to
            already exist or created.
        """
        # is shallow copy, this way we don't mess up for other objects
        
        assert isinstance(measurement,Data)        
        table_dict = {}   
        quant = {}  
        data = {}
        if isinstance(measurement.value,pq.Quantity):
            self._quantity_dict(table_dict,measurement.value,measurement.name+"_")
            quant[measurement.name] = len(measurement.value.magnitude)
            data[measurement.name]= UnitType.quantity
        elif isinstance(measurement.value,bool):
            table_dict[measurement.name] = tables.BoolCol()
            data[measurement.name]= UnitType.base_unit
        elif isinstance(measurement.value,str):
            table_dict[measurement.name] = tables.StringCol(50)
            data[measurement.name]= UnitType.base_unit
        elif isinstance(measurement.value,float):
            table_dict[measurement.name] = tables.Float64Col()
            data[measurement.name]= UnitType.base_unit
        elif isinstance(measurement.value,int):
            table_dict[measurement.name] = tables.Int32Col()
            data[measurement.name]= UnitType.base_unit 
        table_dict["time"] = tables.Float64Col()     
        table, created = self.get_or_create_table(group,name,table_dict,name)
        table.attrs.name = measurement.name
        table.attrs.id = measurement.id
        table.attrs.code = measurement.code 
        table.attrs.compound = False
        table.attrs.quantities = quant
        table.attrs.metadata = data
        if isinstance(measurement.value,pq.Quantity):
            table.attrs.units = measurement.value.units        
        return table , created

    def generate_table_from_compound(self,group,name,compound):
        table_dict = {}
        quant = {}
        data = {}
        for x in compound :            
            if isinstance(x.value,pq.Quantity):
                 self._quantity_dict(table_dict,measurement.value,index=str(x.name)+"_")
                 quant[x.name] = len(x.value.magnitude)
                 data[measurement.name]= UnitType.quantity
            elif isinstance(x.value,bool):
                table_dict["{0}".format(x.name)] = tables.BoolCol()
                data[measurement.name]= UnitType.base_unit
            elif isinstance(x.value,str):
                table_dict["{0}".format(x.name)] = tables.StringCol(50)
                data[measurement.name]= UnitType.base_unit
            elif isinstance(x.value,float):
                table_dict["{0}".format(x.name)] = tables.Float64Col()
                data[measurement.name]= UnitType.base_unit
            elif isinstance(x.value,int):
                table_dict["{0}".format(x.name)] = tables.Int32Col()
                data[measurement.name]= UnitType.base_unit  
            table_dict["{0}_time".format(x.name)] = tables.Float64Col()     
    
        table, created = self.get_or_create_table(group,name,table_dict,name)
        table.attrs.name = name
        table.attrs.compound = True
        table.attrs.quantities = quant
        table.attrs.metadata = data
        for x in compound:
            setattr(table.attrs,x.name,x.id)

        return table,created
    
    


    def close(self):
        print "closing"
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
        new_file = configuration.get('new_file',False)
        old_file = None
        if 'load_previous_entries' in configuration:
            old_file = configuration['load_previous_entries'].get('file_path',None)
        return HDF5Storage(file_path,name,buffer_size,new_file,old_file)

  
      

    @property 
    def storage_code(self):
        """
        Should return the storage engine code
        
        Returns
        -------
        str
        """
        return HDF5Storage.code
        



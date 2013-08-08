from abc import ABCMeta, abstractmethod , abstractproperty
import numpy as np
import quantities as pq
from . import QuantityData
class DataContainer(dict):
    """
    Abstract class to hold all measurements. 
    Must be implemented for passing of measurements    
    """

    

    def __init__(self,ID,max_stored_data=-1,sort_after_n_joins=-1,*arg,**kw):
        self._id = ID
        self._max_stored_data = max_stored_data
        self.update(*arg, **kw)
        self._sort_after_n_joins = sort_after_n_joins
        self._since_last_sort = 0

    def __len__(self):
        """
        Override the len argument to give the length of the number of measurements in 
        the container. Otherwise it would give the number of lists of measurements
        """
        
        return len(self.values())
    

    def __setitem__(self, key, value):
        """
        Overrides setitem to make sure that value is stored as 
        list so they can be joined
        """
        
        if not isinstance(value,np.ndarray) : 
            
            value = np.array([value])

        if isinstance(value,QuantityData):
            value = np.array([value],dtype=QuantityData)
            
        super(DataContainer, self).__setitem__(key, value)

    def update(self, *args, **kwargs):
        """
        from : http://stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem
        """
        if args:
            if len(args) > 1:
                raise TypeError("update expected at most 1 arguments, "
                                "got %d" % len(args))
            other = dict(args[0])
            for key in other:
                self[key] = other[key]
        for key in kwargs:
            self[key] = kwargs[key]

    def setdefault(self, key, value=None):
        """
        from : http://stackoverflow.com/questions/2060972/subclassing-python-dictionary-to-override-setitem
        """
        if key not in self:
            self[key] = value
        return self[key]

    def add_measurement(self,key,measurement):
        """
        Add a measurement to the container

        Parameters
        ----------
        key : str
        measurement : Data
        """

        if key in self:            
            self[key] = np.append(self[key],measurement)            
        else:             
            self[key] = measurement


    def all_recent_data(self):
        """
        Get most recent measurements

        Returns
        -------
        dictionary 
            Containing measurements based on measurement type string key
        """
        recent = self.deepcopy()
        for k,v in recent.iteritems():
            recent[k] = v[-1]
        return recent

    
    def _join(self,container):
        """
        Joins two measurement containers into one. 

        Parameters
        ----------
        container : DataContainer

        Returns
        -------
        DataContainer
            New Holder object

        """
        assert isinstance(container,type(self))
        for k,v in container.iteritems():
            if k in self:
                           
                a= np.append(self[k],v,axis=0)
                self[k] = a
                
            else:
                self[k] = v

        return self


    def sortChronologically(self):
        """
        Sorts container chronologically
        """
        for k,v in self.iteritems():
            v.sort(key=lambda x: x.time, reverse=False)

    def join(self,container):
        """
        Asserts instances are equal, than calls user implemented join function.
        After join sorts into chronological order

        Parameters
        ----------
        container : DataContainer

        Returns
        -------    
        :class:`.DataContainer`
            New Holder object
        """
        if not isinstance(container,type(self)):
            raise TypeError("Instances must be of same type")

        newContainer = self._join(container) 
        if self._sort_after_n_joins >= 1:
            if self._since_last_sort >= self._sort_after_n_joins:       
                newContainer.sortChronologically()
                self._since_last_sort = 0

        #newContainer.sortChronologically()

        self.cull_old_measurements()
        

        return newContainer

    def cull_old_measurements(self):
        """
        Removes extra measurements if too many are stored. Takes from
        front of values list. Should never have to be called as this should be managed 
        at joining of `DataContainer`s
        """
        for k,v in self.iteritems():
            
            if self.max_stored_data != -1:
                
                if self.max_stored_data <= len(v):
                    self[k]= v[-self.max_stored_data:]
    @property
    def max_stored_data(self):
        """
        Maximum measurements to be stored before culling old ones

        Parameters
        ----------
        number : int 
            Maximum number of measurements to store per measurement type

        Returns
        -------
        int 
        """
        return self._max_stored_data
    @max_stored_data.setter
    def max_stored_data(self, number):
        self._max_stored_data = number
    

    @property 
    def id(self):
        """
        Returns
        -------
        str
            ID of the device for which data is being stored
        """
        return self._id


    def __add__ (self,b):
        """
        defines an add function for + operator
        """
        return self.join(b)


    def compound (self):
        
        return reduce(lambda x,y: zip(x,y),self.values())


from abc import ABCMeta, abstractmethod , abstractproperty
import numpy as np
class AbstractDataContainer(dict):
    """
    Abstract class to hold all measurements. 
    Must be implemented for passing of measurements    
    """

    __metaclass__ = ABCMeta

    def __init__(self,ID,max_stored_measurements=-1,*arg,**kw):
        self._id = ID
        self._max_stored_measurements = max_stored_measurements
        self.update(*arg, **kw)

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
        if not isinstance(value,np.ndarray):
            value = np.array([value])
        super(AbstractDataContainer, self).__setitem__(key, value)

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
        container : AbstractDataContainer

        Returns
        -------
        AbstractDataContainer
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
            v.sort()

    def join(self,container):
        """
        Asserts instances are equal, than calls user implemented join function.
        After join sorts into chronological order

        Parameters
        ----------
        container : AbstractDataContainer

        Returns
        -------    
        :class:`.AbstractDataContainer`
            New Holder object
        """
        if not isinstance(container,type(self)):
            raise TypeError("Instances must be of same type")

        newContainer = self._join(container)        
        newContainer.sortChronologically()
        self.cull_old_measurements()
        

        return newContainer

    def cull_old_measurements(self):
        """
        Removes extra measurements if too many are stored. Takes from
        front of values list. Should never have to be called as this should be managed 
        at joining of `AbstractDataContainer`s
        """
        for k,v in self.iteritems():
            
            if self.max_stored_measurements != -1:
                
                if self.max_stored_measurements <= len(v):
                    del v[0:len(v)-self.max_stored_measurements]
    @property
    def max_stored_measurements(self):
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
        return self._max_stored_measurements
    @max_stored_measurements.setter
    def max_stored_measurements(self, number):
        self._max_stored_measurements = number
    

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


from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractDataContainer(dict):
    """
    Abstract class to hold all measurements. 
    Must be implemented for passing of measurements    
    """

    __metaclass__ = ABCMeta

    def __init__(self,max_stored_measurements=-1,*arg,**kw):
        self._max_stored_measurements = max_stored_measurements
        super(AbstractDataContainer,self).__init__(*arg,**kw)

    def __len__(self):
        """
        Override the len argument to give the length of the number of measurements in 
        the container. Otherwise it would give the number of lists of measurements
        """

        return reduce(lambda x,y: len(x)+len(y),self.values())


    def all_recent_data(self):
        """
        Get most recent measurements

        Returns
        -------
        dictionary 
            Containing measurements based on measurement type string key
        """
        recent = dict()
        for k,v in self.iteritems():
            recent[k] = v[-1]
        return recent

    @abstractmethod
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

        return newContainer

    def cull_old_measurements(self):
        for k,v in self.iteritems():
            if self.max_stored_measurements is not None:
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
    




    def __add__ (self,b):
        return self.join(b)


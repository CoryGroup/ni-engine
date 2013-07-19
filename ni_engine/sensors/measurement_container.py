from abc import ABCMeta, abstractmethod , abstractproperty

class AbstractMeasurementContainer(dict):
    """
    Abstract class to hold all measurements. 
    Must be implemented for passing of measurements    
    """

    __metaclass__ = ABCMeta

    def __init__(self,*arg,**kw):
        super(AbstractMeasurementContainer,self).__init__(*arg,**kw)

    def all_recent_measurement(self):
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
        container : AbstractMeasurementContainer

        Returns
        -------
        AbstractMeasurementContainer
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
        container : AbstractMeasurementContainer

        Returns
        -------    
        :class:`.AbstractMeasurementContainer`
            New Holder object
        """
        if not isinstance(container,type(self)):
            raise TypeError("Instances must be of same type")

        newContainer = self._join(container)
        newContainer.sortChronologically()

        return newContainer





    def __add__ (self,b):
        return self.join(b)


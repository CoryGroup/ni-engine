from data_container import AbstractDataContainer

class DataDict(dict):
    """
    Holder for in-memory storage of measurements
    """
    def __init__(self,source,*arg,**kw):
        """
        Parameters
        ----------
        source : str 
            String for source of storage, ie. controller,sensor hardware
        """
        self._source = source
        super(DataDict,self).__init__(*arg,**kw)

    def add_data(self,ID,measurement_container):
        """
        Add some data to be stored

        Parameters 
        ----------
        ID : str 
            ID of device to store

        measurement_container : AbstractDataContainer
            data to be stored
        """
        assert isinstance(measurement_container,AbstractDataContainer)

        if ID in self:
            self[ID] = self[ID] + measurement_container
        else:
            self[ID] = measurement_container
    @property
    def source(self):
        """
        Getter/setter for source parameter
        """
        return self._source
    @source.setter
    def source(self, source):
        self._source = source
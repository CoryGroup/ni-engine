import config
class HardwareFactory(object):
    """
    Handles creation of Hardware objects
    """
    _hardwareBuilders = dict()
    
    def __init__(self,data_handler):
        """
        Parameters
        ----------
        data_handler : DataHandler 
            contains all data taken and previous data from other
            runs if configured to be loaded.
        """
        self._data_handler = data_handler

    def create_hardware(self,config):
        """
        Is called by sensor manager. Finds what piece of Hardware needs to be create_hardware
        and calls it's create method with required information.

        Parameters
        ----------
        config : dict
            Contains configuration information for hardware

        Returns
        -------
        AbstractHardware
            The piece of hardware that was created        
        """
        hardwareCode = self.get_code(config)                
        if hardwareCode in HardwareFactory._hardwareBuilders:
            return HardwareFactory._hardwareBuilders[hardwareCode].create(config,self._data_handler)        

        else:
            raise Exception("hardware Type: {0} not recognised".format(hardwareCode))             

    def get_code(self,configuration):
        """
        Parameters 
        ----------
        configuration : dict 
        Returns 
        -------
        str 
            The code of the piece of hardware to be created
        """
        return configuration[config.CODE]
    
    @classmethod
    def register_hardware(cls,hardware):
        """
        Class method to register an instance of AbstractHardware 
        with the factory, so that objects can be dynamically created 
        from configuration files

        Parameters
        ----------
        hardware : AbstractHardware class 
            Provide the actual class definition not an instance of the class
            
        """
        code = hardware.code
        HardwareFactory._hardwareBuilders[code]= hardware
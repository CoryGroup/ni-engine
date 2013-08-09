class AbstractBitSetter (object):
    """
    Abstract class to handle setting of pins. Not really used right now
    """
    def set_pins(self,list):
        raise NotImplementedError

    def set_bit_dir(self,list):
        raise NotImplementedError
        
    def read_analog_pins(self,list):
        raise NotImplementedError

    def read_digital_pins(self,list):
        raise NotImplementedError

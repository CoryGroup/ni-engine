class AbstractBitSetter (object):

    def set_pins(self,list):
        raise NotImplementedError

    def set_bit_dir(self,list):
        raise NotImplementedError
        
    def read_analog_pins(self,list):
        raise NotImplementedError

    def read_digital_pins(self,list):
        raise NotImplementedError

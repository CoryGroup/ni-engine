from u3 import U3
import ni_engine.config as config
from ..abstract_bit_setter import AbstractBitSetter
from ..abstract_hardware import AbstractHardware


class U3HVBitSetter(AbstractBitSetter):

    def set_pins_to_analog(self,*pinNums):
        eioNum = 0
        fioNum = 0
        for x in pinNums:
            if x < 8:
                fioNum += 2**x
            else:
                eioNum += 2**(x-8)
        self.configIO(fio_analog=fioNum,eio_analog=eioNum)

    def set_bit_dir(self,*tuple):
        commands = map(lambda x: u3.bitDirWrite(IONumber=x[0],Direction=x[1]),tuple)
        return self.getFeedback(commands)

    def read_analog_pins(self,lst):
        return self.getFeedback(map(lambda x: u3.AIN(x),lst))

    def read_digital_pins(self,lst):
        raise self.getFeedback(map(lambda x: u3.BitDirRead(x),lst))


class U3HV(U3,AbstractHardware,U3HVBitSetter):
    """
    Labjack U3-HV hardware object.

    **Required Parameters:**

    **None**

    **Optional Parameters::**

    **None**
    

    """
    code = "U3HV"
    name = "Labjack U3-HV high volatage"
    description = ""
    def __init__(self,ID,name=name,description=description):
        super(U3HV,self).__init__()
        self.configU3()
        self._id = ID
        self._name = name 

    def delete(self):
        del self
    
    def disconnect(self):
        self.close()

    @classmethod
    def create(cls,configuration,data_handler):
        ID = configuration[config.ID]
        n = U3HV.name
        d = U3HV.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            n= configuration[config.DESCRIPTION]
        return U3HV(ID,n,d)




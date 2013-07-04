import u3 
import config
from u3lvBitSetter import U3LVBitSetter
from abstractHardware import AbstractHardware
class U3LV(u3.U3,AbstractHardware,U3LVBitSetter):
	code = "U3LV"
	name = "Labjack U3-LV low volatage"
	description = ""
	def __init__(self,ID,name=name,description=description):
		super(U3LV,self).__init__()
		self.configU3()
		self.id = ID

	def delete(self):
		del self
	
	@classmethod
	def create(cls,configuration):
		ID = configuration[config.idString]
		n = U3LV.name
		d = U3LV.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			n= configuration[config.descriptionString]
		return U3LV(ID,n,d)





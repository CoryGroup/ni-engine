import u3 
import config
class U3LV(u3.U3):
	code = "u3lv"
	name = "Labjack U3-LV low volatage"
	description = ""
	def __init__(self,id,name=name,description=description):
		super(U3LV,self).__init__()
		self.configU3()


	def delete(self):
		del self

	@classmethod
	def create(cls,config):
		ID = config[config.idString]
		n = U3LV.name
		d = U3LV.description
		if config.nameString in configuration:
			n= configuration[config.nameString]
		if config.descriptionString in configuration:
			n= configuration[config.decriptionString]
		return U3LV(ID,n,d)






from instruments.other import NewportESP301

class Newport301(NewportESP301):
    code = "NEW301"
    name = "Newport ESP301 motor controller"
    description = ""
    
    #__init__ inherited from NewportESP301 which inherits from Instrument

    ## As with instrument kit we can't use inits
    ## use this setter method to set all required 
    ## variables after intialization
    def initialize(self,ID,name=name,description=description):
        self.id = ID
        self.name = name
        self.description = description



    @classmethod
    def create(cls,configuration)
        ID = configuration[config.ID]
        n = U3LV.name
        d = U3LV.description
        if config.NAME in configuration:
            n= configuration[config.NAME]
        if config.DESCRIPTION in configuration:
            n= configuration[config.DESCRIPTION]
        


        hardware = Newport301.open_from_uri(uri)

                    








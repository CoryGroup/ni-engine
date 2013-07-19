from controller_factory import ControllerFactory


class ControllerManager(object):
    
    def __init__(self,configuration,hardware_manager,sensor_manager):
                
        self.configuration = configuration
        self.controllers= dict()
        self.controllerFactory = ControllerFactory(hardware_manager,sensor_manager)
        
    def add_controller(self,controllerConfig):
        controller = self.controllerFactory.create_controller(controllerConfig)
        self.controllers[controller.id] = controller
        controller.connect()

    def remove_sensor(self,controller):
        if controller: 
            del self.controllers[controller.id]
            controller.disconnect()

        else: raise ValueError("Must give valid object")
    
    def remove_sensor_by_name(self,controller_name):
        if controller_name: 
            controller = self.controllers[controller_name]
            del self.controllers[controller_name]
            controller.disconnect()

        else: raise ValueError("Must give valid name")

    def remove_all(self):
        for k,v in self.controllers.iteritems():
            v.disconnect()
        self.controllers = dict()

    def parse_factory_yaml(self,config_yaml):
        return config_yaml

    def add_all_controllers(self):
        for x in self.configuration.controllers:
            self.add_controller(x)

    def get_controller_by_id(self,ID):
        if ID in self.controllers:
            return self.controllers[ID]
        else: raise ValueError("No Controllerexists for id: {0}".format(ID))    

    @classmethod
    def register_controller(cls,controller):
        ControllerFactory.register_controller(controller)
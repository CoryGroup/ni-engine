from controller_factory import ControllerFactory
from abstract_controller import AbstractController
import inspect
from concurrent import futures

class ControllerManager(object):
    
    def __init__(self,configuration,data_handler,hardware_manager,consor_manager):
                
        self._configuration = configuration
        self._data_handler = data_handler
        self._controllers= dict()
        self._controllerFactory = ControllerFactory(self._data_handler,hardware_manager,consor_manager)
        self._store_data = self._configuration.store_data
        self._max_workers = self._configuration.max_workers
    
    def add_controller(self,controllerConfig):
        """
        Add a controller to the manager based on a configuration Dictionary

        Parameters
        ----------
        controllerConfig : dict
        """
        controller = self._controllerFactory.create_controller(controllerConfig)
        self._controllers[controller.id] = controller
        controller.connect()

    def remove_controller(self,controller):
        """
        Removes a controller and disconnects it 

        Parameters
        ----------
        controller : AbstractController or str 

        """
        if isinstance(controller,str):
            controller = self.get_controller(controller)
        if controller: 
            del self._controllers[controller.id]
            controller.disconnect()
        else: raise ValueError("Must give valid controller or id")   
    

    def remove_all(self):
        """
        Remove and disconnect all controllers
        """
        for k,v in self._controllers.iteritems():
            v.disconnect()
        self._controllers = dict()

    def parse_factory_yaml(self,config_yaml):
        return config_yaml

    def add_all_controllers(self):
        """
        Method to add all controllers in configuration
        """
        for x in self._configuration.controllers:
            self.add_controller(x)

    def get_controller(self,ID):
        """
        Get a controller by it's ID 

        Parameters
        ----------
        ID : str 

        Returns
        -------
        AbstractController
        """
        if ID in self._controllers:
            return self._controllers[ID]
        else: raise ValueError("No Controllerexists for id: {0}".format(ID))    

    def get_status(self,controllers,compound=False):
        """
        Measures a list of controllers or a single controller

        Parameters
        ----------
        controller : AbstractController or str 

        Returns
        -------
        [`DataContainer`] or singleton `DataContainer` if only single controller

        """
        is_list = True
        if not isinstance(controllers,list):
            is_list = False
            controllers = [controllers]
        for idx,con in enumerate(controllers):
            if isinstance(con,str):
                controllers[idx] = self.get_controller(con)        
            elif not isinstance(con,AbstractController):
                raise TypeError ("Controller: {0} is not subclass of AbstractSensor".format(type(con)))
        # generate list of measurement functions to be executed
        function_list = map(lambda x: (x.get_status,x.threadsafe),controllers)  
        # execute the functions
        results = self.execute_functions(function_list,compound)
        # return singleton if only 1 object
        if len(results)==1 and not is_list:            
            key, value = results.popitem()
            results = value
        return results
    
    def get_all_status(self,compound=False):
        """
        Measure all controllers 

        Returns
        -------
        DataDict
            Contains all AbstractMeasurementContainers for measurements. Dictionary keys by controller ids. 
        """
        result = self.get_status(self._controllers.values(),compound)

        return result

    def execute_functions(self,fns,compound=False):
        """
        Execute a series as functions passed as lambda expressions and store there results.
        The functions must either return a DataContainer or a future that will eventually return
        a data container. All data containers will than be stored

        Parameters
        ----------
        fns : list (tuple(function,threadsafe))

        Returns 
        -------
        dict[id] = `DataContainer`
        """
        # make sure is list
        if not isinstance(fns,list):
            fns = [fns]
        # store methods
        methods = []
        # store methods to be futures
        fut = []
        for (func,threadsafe) in fns:
            #make sure is a function
            
            assert inspect.ismethod(func) or inspect.isfunction(func)
            # if threadsafe add to futures
            if threadsafe: fut.append(func)
            # if not threadsafe add to normal methods
            else: methods.append(func)

        executor = futures.ThreadPoolExecutor(max_workers=self._max_workers)
        #execute all futures and store in list
        future_list = map(lambda x : executor.submit(x),fut) 
        # execute all methods
        method_results = map(lambda x : x(),methods) 
        # wait for all futures to finish 
        futures.wait(future_list,)
        #get all results of futures
        future_results = map(lambda x : x.result(),future_list)
        results = future_results + method_results

        #store measurements if turned on 
        if self._store_data:
            for mes in results:

                self._data_handler.add_controller_data(mes.id,mes,compound=compound)

        return dict((v.id, v) for v in results)

    @classmethod
    def register_controller(cls,controller):
        """
        Called to register a controller with the controller factory.
        """
        ControllerFactory.register_controller(controller)
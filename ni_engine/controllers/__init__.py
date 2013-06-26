from abstractController import AbstractController
from kepcoSupply import KepcoSupply
from controllerFactory import ControllerFactory
from ControllerManager import ControllerManager


# Register all predefined Sensors here
ControllerManager.registerController(KepcoSupply)
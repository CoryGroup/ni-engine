from abstract_controller import AbstractController
from controller_factory import ControllerFactory
from controller_manager import ControllerManager
from kepco_supply import KepcoSupply
from ljtdac import LJTDAC


# Register all predefined Sensors here
ControllerManager.register_controller(KepcoSupply)
ControllerManager.register_controller(LJTDAC)
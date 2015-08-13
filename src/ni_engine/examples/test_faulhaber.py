import sys

try:
    sys.path.append("../")
except:
    print "couldn't import"

from ni_engine import NiEngine
from memory_profiler import profile
from time import sleep 


@profile
def test():
    n = NiEngine("ni_engine/examples/example_configurations/test_lm1247.yml")
    sen = n.sensor_manager
    con = n.controller_manager 
    data = n.data_handler
    
    linear_motor = con.get_controller('lm1247')
    linear_motor.move_absolute(-3000)
    for x in range(100):
        sleep(0.1)
        linear_motor.move_absolute(60*x)
        status = linear_motor.get_status()
        data.add_controller_data(linear_motor.id,status)

    for x in range(100):
        sleep(0.1)
        linear_motor.move_relative(-60)
        status = linear_motor.get_status()
        data.add_controller_data(linear_motor.id,status)
    

    
    


test()



#cprofile.run('for x in range(1000000):sen.measure_all()')
import sys

try:
    sys.path.append("../")
except:
    print "couldn't import"

from ni_engine import NiEngine
from memory_profiler import profile


@profile
def test():
    n = NiEngine("../../conf/labjack_test.yml","../../conf/available_interfaces.yml")
    sen = n.sensor_manager
    con = n.controller_manager 
    data = n.data_handler
    dacs = [con.get_controller("testDAC1"),con.get_controller("testDAC2"),con.get_controller("testDAC3"),con.get_controller("testDAC4"),con.get_controller("testDAC5"),
            con.get_controller("testDAC6"),con.get_controller("testDAC7"),con.get_controller("testDAC8")]
    for x in xrange(0,10000000):
        compound = []
        for idx,dac in enumerate(dacs):
            dac.voltage = ((idx+1)*x*0.01)%2.0
            status = dac.get_status()
            data.add_controller_data(dac.id,status)
            compound.append(status)


test()



#cprofile.run('for x in range(1000000):sen.measure_all()')
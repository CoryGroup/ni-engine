"""
For 100 averages: 
    Sweep phase flag over settings of theta
    measure counts
"""
import sys
import numpy as np
import time
import quantities as pq
try:
    sys.path.append("../")
except:
    print "couldn't import"

from ni_engine import NiEngine

print "Loading NI Engine..."
n = NiEngine("sample_experiment.yml","../../conf/available_interfaces.yml")

sen = n.sensor_manager
con = n.controller_manager 
data = n.data_handler

motor = con.get_controller('phase_flag')
print "getting motor"

for x in xrange(100):
    print "experiment #{0}".format(x)
    for theta in np.linspace(0,10,21)*pq.degree:        
        motor.move_absolute(theta)
        print "moving to: {}".format(theta)
        time.sleep(1)
        print "measuring"
        sen.measure_all()
import sys

try:
    sys.path.append("../")
except:
    print "couldn't import"

from ni_engine import NiEngine

n = NiEngine("test_large.yml","available_interfaces.yml")
sen = n.sensor_manager

for x in range(1000000):sen.measure_all()
try:
    import daqmx_threadsafe
    from ni_pci6602 import NIPCI6602
except ImportError:
    daqmx_threadsafe = None
    NIPCI6602 = None

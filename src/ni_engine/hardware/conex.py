
from contextlib import contextmanager

import serial
import time

def strip_int(s):
    # Find where the digits end.
    for idx, char in enumerate(s):
        if not char.isdigit(): break
    sub_s = s[0:idx]
    return int(sub_s) if sub_s else 0

def enum(*sequential, **named):
    # Copied from:
    # http://stackoverflow.com/a/1695250
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

ConexCCStates = enum(
    'NOT_REFERENCED', 'CONFIGURATION', 'HOMING', 'MOVING', 'READY', 'READY_T',
    'DISABLE', 'TRACKING'
)

class StateError(EnvironmentError):
    """
    Raised when the controller state disallows a particular command.
    """
    pass
    
class PositionerError(IOError):
    """
    Raised when the positioner error of a Conex-CC device is non-zero.
    """
    def __init__(self, code):
        self._code = bytearray(code.decode("hex"))
        self.faults = self._faults()
        super(PositionerError, self).__init__("Positioner error with faults: {}.".format(", ".join(self.faults)))
        
    def _faults(self):
        """
        Returns a list of positioner faults that occured at the time of this
        Error.
        """
        faults = []
        code = self._code
        
        ## BYTE 0 ##
        if code[0] & 0b00000010:
            faults.append("80W output power exceeded")
        if code[0] & 0b00000001:
            faults.append("DC voltage too low")
            
        ## BYTE 1 ##
        if code[1] & 0b10000000:
            faults.append("wrong ESP stage")
        if code[1] & 0b01000000:
            faults.append("homing time out")
        if code[1] & 0b00100000:
            faults.append("following error")
        if code[1] & 0b00010000:
            faults.append("short circuit detection")
        if code[1] & 0b00001000:
            faults.append("RMS current limit")
        if code[1] & 0b00000100:
            faults.append("peak current limit")
        if code[1] & 0b00000010:
            faults.append("positive end of run")
        if code[1] & 0b00000001:
            faults.append("negative end of run")
            
        return faults
        
class ConexCC(object):
    BAUD_RATE = 921600
    DATA_BITS = serial.EIGHTBITS
    STOP_BITS = serial.STOPBITS_ONE
    PARITY = serial.PARITY_NONE
    
    ERROR_CODES = {
        'A': (ValueError, "Unknown message code or floating point controller address."),
        'B': (ValueError, "Controller address not correct."),
        'C': (ValueError, "Parameter missing or out of range."),
        'D': (ValueError, "Command not allowed."),
        'E': (RuntimeError, "Home sequence already started."),
        'G': (ValueError, "Displacement out of limits."),
        'H': (StateError, "Command not allowed in the NOT REFERENCED state."),
        'I': (StateError, "Command not allowed in the CONFIGURATION state."),
        'J': (StateError, "Command not allowed in the DISABLE state."),
        'K': (StateError, "Command not allowed in the READY state."),
        'L': (StateError, "Command not allowed in the HOMING state."),
        'M': (StateError, "Command not allowed in the MOVING state."),
        'N': (ValueError, "Current position out of software limit."),
        'P': (StateError, "Command not allowed in the TRACKING state."),
        'S': (serial.SerialTimeoutException, "Communication time out."),
        'U': (IOError, "Error during EEPROM access."),
        'V': (RuntimeError, "Error during command execution.")
    }
    
    STATE_MAP = {
        "0A": ConexCCStates.NOT_REFERENCED,
        "0B": ConexCCStates.NOT_REFERENCED,
        "0C": ConexCCStates.NOT_REFERENCED,
        "0D": ConexCCStates.NOT_REFERENCED,
        "0E": ConexCCStates.NOT_REFERENCED,
        "0F": ConexCCStates.NOT_REFERENCED,
        "10": ConexCCStates.NOT_REFERENCED,
        "14": ConexCCStates.CONFIGURATION,
        "1E": ConexCCStates.HOMING,
        "28": ConexCCStates.MOVING,
        "32": ConexCCStates.READY,
        "33": ConexCCStates.READY,
        "34": ConexCCStates.READY,
        "36": ConexCCStates.READY_T,
        "37": ConexCCStates.READY_T,
        "38": ConexCCStates.READY_T,
        "3C": ConexCCStates.DISABLE,
        "3D": ConexCCStates.DISABLE,
        "3E": ConexCCStates.DISABLE,
        "3F": ConexCCStates.DISABLE,
        "46": ConexCCStates.TRACKING,
        "47": ConexCCStates.TRACKING
    }

    def __init__(self, port_url, addr=1, timeout=0.02):
        self._port_url = port_url
        self._timeout = timeout
        self._addr = addr
        self._serial = serial.serial_for_url(
                port_url,
                timeout=timeout,
                baudrate=self.BAUD_RATE,
                bytesize=self.DATA_BITS,
                stopbits=self.STOP_BITS,
                parity=self.PARITY
            ) # <- This opens the port!
       
    def close(self):
        # TODO: make all other methods become invalid after this.
        try:
            self._serial.close()
        except:
            pass
       
    ## MAGIC METHODS ##
        
    def __del__(self):
        self.close()
    
    def __getitem__(self, item):
        # TODO: do type conversion here, verify the item.
        return self.__command(item, "?", _procresp=True)
        
    def __setitem__(self, item, value):
        # TODO: do type conversion here, verify the item and value.
        self.__command(item, str(value))
       
    ## PROPERTIES ##
       
    @property 
    def timeout(self):
        return self._serial.timeout
    @timeout.setter
    def timeout(self, newval):
        self._serial.timeout = newval
        self._timeout = newval
        
    @property
    def addr(self): # Read-only, so no setter.
        return self._addr
        
    @property
    def is_tracking(self):
        # FIXME: need to check that the current state allows for
        #        querying TRACKING mode.
        return bool(int(self["TK"]))
    @is_tracking.setter
    def is_tracking(self, newval):
        self["TK"] = 1 if newval else 0
        
    @property
    def is_enabled(self):
        # FIXME: need to check that the current state allows for
        #        querying MM command.
        return bool(int(self["MM"]))
    @is_enabled.setter
    def is_enabled(self, newval):
        mode["MM"] = 1 if newval else 0
        
    @property
    def encoder_increment(self):
        """
        Gets/sets the encoder increment value used to convert all other distance
        units, including the curent position, travel limits and velocities.
        """
        return float(self["SU"])
    @encoder_increment.setter
    def encoder_increment(self, newval):
        self["SU"] = newval
        
    @property
    def negative_limit(self):
        return float(self["SL"])
    @negative_limit.setter
    def negative_limit(self, newval):
        self["SL"] = newval
        
    @property
    def positive_limit(self):
        return float(self["SR"])
    @positive_limit.setter
    def positive_limit(self, newval):
        self["SR"] = newval
        
    @property
    def current_pos(self):
        # FIXME: need to check that the current state allows for
        #        querying TP.
        return float(self["TP"])
        
    @property
    def state(self):
        return self.STATE_MAP[self.__poserr_state()]
        
    # The following properties are for convienence, but duplicate functionality
    # provided by state().
    @property
    def is_homed(self): return self.state != ConexCCStates.NOT_REFERENCED
    @property
    def is_moving(self): return self.state == ConexCCStates.MOVING
    @property
    def is_ready(self): return self.state in (ConexCCStates.READY, ConexCCStates.READY_T)
    @property
    def is_tracking(self): return self.state == ConexCCStates.TRACKING
    @property
    def is_configurable(self): return self.state == ConexCCStates.CONFIGURATION
        
    ## UTILITY METHODS ##
    
    def __exception_for(self, error_code):
        cls, descript = self.ERROR_CODES[error_code]
        return cls(descript)        
        
    ## LOW-LEVEL COMMAND HANDLING ##
        
    def __raw(self, data):
        n = self._serial.write(bytearray(data, 'ascii'))
        assert n == len(data)
        return n
        
    def __command(self, cmd="", arg="", addr=None, _chkerr=True, _procresp=False):
        """
        _chkerr: if True, after completing the command execution, checks for
            the current error code.
        _procresp: if True, after completing the command execution, enforces that
            the response is one line long, strips the new line and removes the
            address and command portiosn of the response.
        """
        if addr is None:
            addr = self._addr
        self.__raw("{addr}{cmd}{arg}\r\n".format(addr=addr, cmd=cmd, arg=arg))
        resp = self._serial.readlines()
    
        if _chkerr:
            self.__checkerror()
            
        if _procresp:
            if len(resp) != 1:
                raise IOError("Expected 1 line executing {} command, got {}.".format(cmd, len(resp)))
            
            resp = self.__checkaddr(resp[0].strip()).partition(cmd)[2]
            
        return resp
        
    def __checkaddr(self, response, addr=None):
        """
        Given a response string of the format {addr}{cmd}{return},
        checks that {addr} matches the expected address and returns
        the {cmd}{return} portion of the response string.
        """
        expected_addr = addr if addr is not None else self._addr
        actual_addr = strip_int(response)
        if actual_addr != expected_addr:
            raise IOError("Expected address {}, got {}.".format(expected_addr, actual_addr))
        return response.partition(str(actual_addr))[2]
        
    def __checkerror(self, addr=None):
        # Obtain the lines of output from the TE command.
        err = self.__command("TE", addr=addr, _chkerr=False, _procresp=True)        
        
        if err != "@":
            raise self.__exception_for(result)
            
    def __poserr_state(self):
        # Wraps the TS command to get the positioner error and the current
        # state.
        resp = self.__command("TS", _procresp=True)
        poserr = resp[0:4]
        state = resp[4:]
        if poserr != "0000":
            raise PositionerError(poserr)
            
        return state
            
    ## COMMAND IMPLEMENTATIONS ##
    
    def reset(self):
        return self.__command("RS")
        
    def home(self, wait=False):
        """
        If ``wait`` is set to a float, then after the command successfully
        returns, this method will wait for the motor to complete its search for
        home.
        """
        resp = self.__command("OR")
        if not wait:
            return resp
            
        # Anthropic principle: we are waiting.
        tic = time.clock()
        while (time.clock() - tic < wait) and self.__poserr_state() != "1E":
            time.sleep(0.1)
        # FIXME: make a more specific exception.
        if self.__poserr_state != "1E":
            raise IOError("Timed out waiting for the motor to find home.")
        
    def stop(self):
        self.__command("ST")
        
    def __wait(self, t, cond, msg):
        tic = time.clock()
        while (time.clock() - tic < t) and not cond():
            time.sleep(0.1)
            
        # FIXME: make a more specific exception.
        if self.is_moving:
            raise IOError(msg)
        
    def move_absolute(self, new_pos, wait=False):
        resp = self.__command("PA", str(float(new_pos)))
        if not wait:
            return resp
        else:        
            self.__wait(wait, lambda: not self.is_moving, "Timed out waiting for an absolute move.")
            
    ## STATE TRANSITIONS ##
    
    @contextmanager
    def configure(self):
        """
        Context manager that resets the controller, transitions to the CONFIGURATION state and then writes configuration parameters upon exiting.
        """
        self.reset()
        self.__command("PW", str(1))
        self.__wait(15, lambda: self.is_configurable, "Timed out waiting for the device to become configurable.")
        yield
        self.__command("PW", str(0))
        self.__wait(15, lambda: self.is_configurable, "Timed out waiting for the device to write its configuration.")



from __future__ import print_function

import os
import sys

from .._lib import docopt

from PySide.QtCore import *
from PySide.QtGui import *

if os.name == 'nt':
    from serial.tools.list_ports_windows import comports
elif os.name == "posix":
    from serial.tools.list_ports_posix import comports
else:
    raise ImportWarning("Could not load a port lister.")
    def comports():
        return []


from ui import open_serial

class OpenSerialDialog(QDialog):
    def __init__(self, callback, label=None, parent=None):
        super(OpenSerialDialog, self).__init__(parent)
        self.ui = open_serial.Ui_Dialog()
        self.ui.setupUi(self)
        
        self.callback = callback

        if label is not None:
            # Override the default label text.
            self.ui.label.setText(label)

        self.ui.buttonBox.accepted.connect(self.on_accepted)
        self.ui.buttonBox.rejected.connect(self.on_rejected)
        
        self.populate_known_ports()
        
    def populate_known_ports(self):
        # Get a list of known ports from pyserial.
        known_ports = comports()
        
        # Clear out all combo box items already there.
        self.ui.known_ports.clear()
        
        # Add each using the port name as the userData.
        for name, desc, hw_addr in known_ports:
            self.ui.known_ports.addItem(desc, userData=name)
            
    @property
    def port_value(self):
        if self.ui.rb_from_known_port.isChecked():
            return self.ui.known_ports.itemData(self.ui.known_ports.currentIndex())
        else:
            return self.ui.port_url.text()
        
    def on_accepted(self):
        self.callback(self.port_value)
        self.close()
        
    def on_rejected(self):
        self.callback(None)
        self.close()
    
USAGE = """
Usage:
    common_dialogs -h
    common_dialogs help COMMAND
    common_dialogs open-serial [--label=LABEL]
"""
        
if __name__ == "__main__":
    # Make the dialogs usable from shell scripts.
    cmdargs = docopt.docopt(USAGE)
    
    # No matter what, we'll need a QApplication, so create one here.
    app = QApplication(sys.argv)
    
    # Process options common to all kinds of dialog.
    label = cmdargs['--label'] if '--label' in cmdargs else None
    
    # Switch which dialog to show based on cmdargs.
    if "open-serial" in cmdargs:
        win = OpenSerialDialog(callback=print, label=label)
        win.show()
        
    # Start the Qt event loop, then exit.    
    sys.exit(app.exec_())
    


from __future__ import print_function
from ..hardware import conex

import serial

import sys
from PySide.QtCore import *
from PySide.QtGui import *

from ui.conex_config import Ui_MainWindow

import common_dialogs

def spinbox_binding(control):
    return control.value, lambda val: control.setValue(float(val))

class MainWindow(QMainWindow):
    SB_NAMES = (
        "AC", "BA", "BH", "DV", "FD", "FE", "FF",
        "JR", "KD", "KI", "KP", "KV", "OH", "OT",
        "QIL", "QIR", "QIR", "SL", "SR", "SU", "VA"
    )

    def __init__(self, parent=None):
        # Call the superclass initializer and unpack the UI.
        super(MainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Start off with no device selected.
        
        self.current_device = None
        self.ui.config_area.setEnabled(False)
        
        # Add previously saved devices to the device list.
        
        self.populate_devices()
        
        # Connect signals to the four buttons.
        
        self.ui.btn_reset_params.clicked.connect(self.reset_params)
        self.ui.btn_save_params.clicked.connect(self.save_params)
        self.ui.add_device.clicked.connect(self.on_add_device)
        self.ui.device_list.activated.connect(self.on_device_activated)
        
        # Bind the various configuration parameters.
        #
        # Here, bindings is a map from config symbol names to getter/setters 
        # for the UI element for that symbol. We do it this way since not all
        # UI elements use the same methods.
        
        self.bindings = {}
        
        for sb_name in self.SB_NAMES:
            self.bindings[sb_name] = spinbox_binding(getattr(self.ui, "sb_" + sb_name))
            
        self.bindings["HT"] = (self.ui.cb_HT.currentIndex, lambda val: self.ui.cb_HT.setCurrentIndex(int(val)))
        self.bindings["ID"] = (self.ui.le_ID.text, self.ui.le_ID.setText)
        self.bindings["SC"] = (self.ui.cb_SC.currentIndex, lambda val: self.ui.cb_SC.setCurrentIndex(int(val)))
        
    def populate_devices(self):
        # TODO!
        pass
        
    def save_params(self):
        # TODO: check that the mode is set correctly and everything.
        # TODO: catch exceptions.
        if self.current_device is None: return
        
        # Ensure that the user actually wants to do this!
        dialog = QMessageBox()
        dialog.setText("Are you sure you want to save parameters?")
        dialog.setInformativeText("Newport recommends that each controller be reconfigured no more than 100 times, so please be sure before you continue.")
        dialog.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Cancel)
        ret = dialog.exec_()
        if ret == QMessageBox.Cancel:
            return
            
        # Transition the state, then write.
        dev = self.current_device
        with dev.configure(): # <- this will block for 10 seconds.
            for config_sym, (getter, setter) in self.bindings.iteritems():
                self.current_device[config_sym] = getter()
        
    def reset_params(self):
        # TODO: check that the mode is set correctly and everything.
        # TODO: catch exceptions.
        if self.current_device is None: return
        for config_sym, (getter, setter) in self.bindings.iteritems():
            print("[DEBUG] Reading parameter {}.".format(config_sym))
            setter(self.current_device[config_sym])
        
    def on_add_device(self):
        def callback(port_name):
            if port_name is not None:
                self.ui.device_list.addItem(port_name)
            
        serial_dialog = common_dialogs.OpenSerialDialog(callback=callback)
        serial_dialog.exec_() # FIXME: make non-blocking somehow?
        
    def on_device_activated(self, index):
        # FIXME: warn before discarding unsaved changes!
        
        # First and foremost, delete the old device if need be,
        # so that the port isn't kept open.
        if self.current_device is not None:
            self.current_device.close()
            self.current_device = None
        
        # FIXME: use userData instead of currentText.
        port_name = self.ui.device_list.model().itemData(
                self.ui.device_list.currentIndex())[0]
        print("Opening port: {}".format(port_name))
        try:
            # Open the device.
            self.current_device = conex.ConexCC(port_name, log=True)
            
            # Transition to NOT_REFERENCED.
            self.current_device.reset()
        
            # Read out the current configuration.
            self.reset_params()
            
        except serial.serialutil.SerialException as se:
            error_dialog = QErrorMessage()
            error_dialog.showMessage(se.message)
            error_dialog.exec_() 
            return
        
        # Finally, enable the scroll view if not already done.
        self.ui.config_area.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


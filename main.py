from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
import Interfaz
import time
from threading import Thread
import getSerial
from TK4 import Tk4

### START QtApp #####
app = QApplication([])
error_dialog = QtWidgets.QErrorMessage()
tk4Port = getSerial.get_autonics()
tk4 = Tk4(tk4Port, False)


def update():
    ui.setPointLine.setText(str(tk4.get_setvalue(1)))
    while ui.isVisible():
        if ui.update:
            tk4.set_value(1, ui.setValue[0], 0)
            tk4.set_value(2, ui.setValue[1], 0)
            ui.update = False
            ui.setPointLine.setText(str(ui.setValue[0]))

        hs1 = tk4.get_heating_side(1)
        temp1 = tk4.get_temperature(1)
        ui.chamberValue(hs1)
        ui.chamberText.setText(str(temp1) + "°C")
        QtGui.QGuiApplication.processEvents()
        time.sleep(0.1)


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        ui = Interfaz.Ui_ventConfWindow()
        t1 = Thread(target=update)
        t1.start()
        QtGui.QGuiApplication.instance().exec_()

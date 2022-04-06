from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore, QtGui
import Interfaz

### START QtApp #####
app = QApplication([])
error_dialog = QtWidgets.QErrorMessage()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QGuiApplication.instance().exec_()
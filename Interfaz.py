from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QPushButton, QMainWindow, QMenu, QAction
import pyqtgraph as pg
import numpy as np
from PyQt5.QtCore import *
import sys


def resize(value, conversion):
    return int(value * conversion / 100)


class Ui_ventConfWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        screen = app.primaryScreen()
        size = screen.size()
        self.width = size.width()
        self.height = size.height()
        self.font = QtGui.QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(15)
        self.font.setBold(True)
        self.font.setWeight(20)

        self.setValue = [0, 0]
        self.temperatureValue = [0, 0]
        self.heatingSide = [0, 0]
        self.proportional = [0, 0]
        self.derivative = [0, 0]
        self.integral = [0, 0]
        self.kellerPressure = [0, 0]
        self.kellerTemperature = [0, 0]

        self.BGCOLOR = "#05121c"

        self.setWindowTitle('SPD Monitor')
        self._createMenuBar()
        self.setupUi()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet("""QMenuBar { background-color: rgb(225, 225, 225); }""")
        qMenuStyle = """QMenu { background-color: #ABABAB; margin: 2px;}"""
        # Creating menus using a QMenu object
        self.openAction = QAction("&Open...", self)
        fileMenu = QMenu("&Archivo", self)
        fileMenu.setStyleSheet(qMenuStyle)
        fileMenu.addAction(self.openAction)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Configuración")
        self.setMenuBar(menuBar)

    def setupUi(self):
        self.setObjectName("GUIWindow")
        self.setStyleSheet("background-color:" + self.BGCOLOR + ";")
        self.showMaximized()

        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.stackedWidget = QtWidgets.QStackedWidget()

        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget.setGeometry(
            QtCore.QRect(resize(1.041, self.width), resize(1.85, self.height), resize(75, self.width),
                         resize(70, self.height)))


        # Layout 1
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        # Grid
        self.grid = QtWidgets.QWidget(self.verticalLayoutWidget)
        self.grid.setGeometry(QtCore.QRect(resize(0, self.width), resize(0, self.height), resize(15, self.width),
                                           resize(15, self.height)))
        self.grid.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.grid)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        #self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName("gridLayout")

        # Label Temperatura Horno
        self.ovenLabel = QtWidgets.QLabel(self.grid)
        self.ovenLabel.setText("Temperatura Horno  °C")
        self.ovenLabel.setStyleSheet("background-color: transparent; color: rgb(255, 255, 255);")
        self.ovenLabel.setFont(self.font)
        self.ovenLabel.setAlignment(Qt.AlignCenter)
        self.ovenLabel.setObjectName("ovenLabel")
        self.gridLayout.addWidget(self.ovenLabel, 0, 0)

        # Valor de Temperatura Horno
        self.font.setPointSize(20)
        self.ovenText = QtWidgets.QLabel(self.grid)
        self.ovenText.setText(str(self.temperatureValue[0]))
        self.ovenText.setObjectName("ovenText")
        self.ovenText.setFont(self.font)
        self.ovenText.setStyleSheet("background-color: transparent; color: rgb(255, 255, 255);")
        self.ovenText.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.ovenText, 1, 0)

        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show()


app = QtWidgets.QApplication(sys.argv)
QtWidgets.QMainWindow()
ui = Ui_ventConfWindow()

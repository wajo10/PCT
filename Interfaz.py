from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QPushButton, QMainWindow, QMenu, QAction, QLineEdit
from PyQt5.QtGui import QBrush, QColor, QPainter, QIntValidator
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.QtCore import *
import time
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
        self.update = False

        self.setValue = [0, 0]
        self.temperatureValue = [0, 0]
        self.heatingSide = [0, 0]
        self.proportional = [0, 0]
        self.derivative = [0, 0]
        self.integral = [0, 0]
        self.kellerPressure = [0, 0]
        self.kellerTemperature = [0, 0]

        # self.BGCOLOR = "#05121c"
        self.BGCOLOR = "#969595"

        self.setWindowTitle('SPD Monitor')
        self._createMenuBar()
        self.setupUi()
        self.show()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        menuBar.setStyleSheet("""QMenuBar { background-color: #F1EFF2; }""")
        qMenuStyle = """QMenu { background-color: #F1EFF2; margin: 2px;}"""
        # Adding Actions
        self.openAction = QAction("&Open...", self)
        self.portsAction = QAction("&Puertos", self)
        self.calibrationAction = QAction("&Calibración Presión", self)
        # self.openAction.triggered.connect(self.open)

        # Creating menus using a QMenu object
        fileMenu = QMenu("&Archivo", self)
        fileMenu.setStyleSheet(qMenuStyle)
        fileMenu.addAction(self.openAction)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        toolsMenu = menuBar.addMenu("&Herramientas")
        toolsMenu.setStyleSheet(qMenuStyle)
        toolsMenu.addAction(self.portsAction)
        toolsMenu.addAction(self.calibrationAction)
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
            QtCore.QRect(0, 0, 180, 250))

        # Layout 1
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")

        # Grid
        self.grid = QtWidgets.QWidget(self.centralwidget)
        self.grid.setGeometry(QtCore.QRect(250, 0, 500, 200))
        self.grid.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.grid)
        self.gridLayout.setContentsMargins(0, 80, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setRowStretch(4, 1)

        # Grafica Heating Side Horno
        self.series = QBarSeries()
        self.set0 = QBarSet('Horno')
        self.set0.append([50])
        self.series.append(self.set0)
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        axisX = QBarCategoryAxis()
        axisX.append("%")

        axisY = QValueAxis()
        axisY.setRange(0, 100)

        self.chart.setAxisX(axisX)
        self.chart.setAxisY(axisY)
        self.series.attachAxis(axisX)
        self.series.attachAxis(axisY)

        self.chart.legend().setVisible(False)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(self.chart)
        self.chart.setBackgroundBrush(QBrush(QColor(self.BGCOLOR)))
        self.verticalLayout.addWidget(self.chartView)

        # Label Temperatura Camara
        self.chamberLabel = QtWidgets.QLabel(self.grid)
        self.chamberLabel.setText("Temperatura Cámara")
        self.chamberLabel.setStyleSheet("background-color: transparent; color: rgb(0, 0, 0);")
        self.chamberLabel.setFont(self.font)
        self.chamberLabel.setAlignment(Qt.AlignCenter)
        self.chamberLabel.setObjectName("chamberLabel")
        self.gridLayout.addWidget(self.chamberLabel, 0, 1)

        # Valor de Temperatura Camara
        self.font.setPointSize(20)
        self.chamberText = QtWidgets.QLabel(self.grid)
        self.chamberText.setText(str(self.temperatureValue[0]) + "°C")
        self.chamberText.setObjectName("chamberText")
        self.chamberText.setFont(self.font)
        self.chamberText.setStyleSheet("background-color: transparent; color: rgb(0, 0, 0);")
        self.chamberText.setAlignment(Qt.AlignCenter)
        self.gridLayout.addWidget(self.chamberText, 1, 1)

        self.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(self)

        # Label SetPoint Cámara
        self.font.setPointSize(15)
        self.spChamberLabel = QtWidgets.QLabel(self.grid)
        self.spChamberLabel.setText("Set Point Cámara (°C)")
        self.spChamberLabel.setStyleSheet("background-color: transparent; color: rgb(0, 0, 0);")
        self.spChamberLabel.setFont(self.font)
        self.spChamberLabel.setAlignment(Qt.AlignCenter)
        self.spChamberLabel.setObjectName("spChamberLabel")
        self.gridLayout.addWidget(self.spChamberLabel, 0, 2)

        # Set Point Cámara
        self.font.setPointSize(20)
        self.setPointLine = QLineEdit()
        self.setPointLine.setValidator(QIntValidator())
        self.setPointLine.setMaxLength(3)
        self.setPointLine.setText(str(self.setValue[0]))
        self.setPointLine.setFont(self.font)
        self.setPointLine.setAlignment(Qt.AlignRight)
        self.setPointLine.setFixedWidth(80)
        self.gridLayout.addWidget(self.setPointLine, 1, 2, alignment=QtCore.Qt.AlignCenter)

        # Boton Ok
        styleSheet = "background-color: rgb(190, 187, 191); border-style: outset; " \
                     "border-width: 2px; border-radius: 5px; padding: 4px; " \
                     "color: black; border-color: rgb(0, 0, 0)"
        self.stableButton = QPushButton(self.centralwidget)
        self.stableButton.setStyleSheet(styleSheet)
        self.stableButton.setFont(self.font)
        self.stableButton.setText("Ok")
        self.stableButton.setGeometry(1700, 850, 80, 50)
        self.stableButton.show()
        self.stableButton.clicked.connect(lambda: self.updateParams())

    def chamberValue(self, value):
        """
        Updates Chamber Graph
        :param value: New Chamber Value
        """
        self.set0.remove(0, 1)
        self.set0.append(value)
        self.series.append(self.set0)
        self.chart.addSeries(self.series)
    
    def updateParams(self):
        self.update = True
        self.setValue[0] = int(self.setPointLine.text())
    


app = QtWidgets.QApplication(sys.argv)
QtWidgets.QMainWindow()


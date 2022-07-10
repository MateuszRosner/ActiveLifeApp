from pickle import NONE
from random import random
from select import select
import string
import sys
import time
import datetime
import serial
import serial.tools.list_ports

from ui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QLineSeries, QValueAxis, QDateTimeAxis
from PyQt5.QtCore import Qt

class MyWindow(Ui_MainWindow):
# ---------------class init functions---------------
    def __init__(self):
        super(MyWindow, self).__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.listSerialPorts()
        self.ser=serial.Serial(
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.5)
        
        self.graphTimer = QtCore.QTimer()

        self.maxValue = 0.0
        self.minValue = 0.0

        # --------------- chart settings ---------------
        self.chartData = QChart()
        self.axis_y = QValueAxis()
        self.axis_x = QDateTimeAxis()
        self.axis_x.setFormat("hh:mm:ss")
        self.axis_x.setTitleText("Time")
        self.axis_y.setTitleText("Value")
        
        self.maxData = QLineSeries(self.MainWindow)
        self.maxData.setName("EMG / BIOZ")

        self.chartData.addSeries(self.maxData)
        self.chartData.setAnimationOptions(QChart.NoAnimation)
        self.chartData.setTitle("MAX30001")
        self.chartData.legend().setVisible(True)
        self.chartData.legend().setAlignment(Qt.AlignBottom)
        self.chartData.addAxis(self.axis_y, QtCore.Qt.AlignLeft)
        self.chartData.addAxis(self.axis_x, QtCore.Qt.AlignBottom)

        self.maxData.attachAxis(self.axis_x)
        self.maxData.attachAxis(self.axis_y)

        self.Graph.setChart(self.chartData)


    # --------------- signals - slots config ---------------
        self.pushButtonConnect.clicked.connect(self.openPort)
        self.pushButtonStart.clicked.connect(self.startMeasurement)
        self.pushButtonStop.clicked.connect(self.stopMeasurement)
        self.pushButtonClearGraph.clicked.connect(self.clearGraph)
        self.pushButtonSave.clicked.connect(self.saveFile)
        self.graphTimer.timeout.connect(self.create_linechart)


    def openPort(self):
        if self.comboBoxPorts.currentText() != NONE:
            self.ser.port = self.comboBoxPorts.currentText().split(" ")[0]
            print(self.comboBoxPorts.currentText().split(" ")[0])
            try:
                self.ser.open()
            except:
                print("[ERROR] Can't open serial port...")

    def listSerialPorts(self):
        ports = serial.tools.list_ports.comports()

        for port, desc, hwid in sorted(ports):
                print("{}: {}".format(port, desc))
                self.comboBoxPorts.addItem(port+" "+desc)

    def getActualSettings(self):
        pass

    def setActualSettings(self):
        pass

    def create_linechart(self):
        timenow = QtCore.QDateTime.currentDateTime()
        value = random() * 100 - 50

        if self.maxData.count() == 0:
            self.axis_x.setMin(timenow)

        self.maxData.append(timenow.toMSecsSinceEpoch(), value)
        self.axis_x.setMax(timenow)

        if value < self.minValue:
            self.minValue = value
        if value > self.maxValue:
            self.maxValue = value

        self.axis_y.setMax(self.maxValue)
        self.axis_y.setMin(self.minValue)

    def clearGraph(self):
        self.maxData.clear()

    def startMeasurement(self):
        self.graphTimer.start(100)

    def stopMeasurement(self):
        self.graphTimer.stop()

    def saveFile(self):
        filter = ("Coma separated files (*.csv)")
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilters([filter])
        filenames = QtCore.QStringListModel()

        if dlg.exec_():
            filenames = dlg.selectedFiles()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.MainWindow.show()
    app.exec_()
    print("Finish")
from pickle import NONE
from random import random
from select import select
import threading
import string
import sys
import time
import datetime
import serial
import serial.tools.list_ports
import csv
import max_setup

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

        self.serThreadRdy = False
        
        self.serialThread = threading.Thread(target=self.getDataFromSerial)
        self.serialThread.daemon = True

        self.graphTimer = QtCore.QTimer()

        self.maxValue = 0.0
        self.minValue = 0.0
        self.rawData = []

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

        self.max30001 = max_setup.max30001()
        self.updateBIOZSettings()
        self.updateECGSettings()

    # --------------- signals - slots config ---------------
        self.pushButtonConnect.clicked.connect(self.openPort)
        self.pushButtonStart.clicked.connect(self.startMeasurement)
        self.pushButtonStop.clicked.connect(self.stopMeasurement)
        self.pushButtonClearGraph.clicked.connect(self.clearGraph)
        self.pushButtonSave.clicked.connect(self.saveFile)
        self.pushButtonSet.clicked.connect(self.setActualSettings)
        self.graphTimer.timeout.connect(self.create_linechart)
        self.comboBoxEMGGAIN.currentTextChanged.connect(self.updateECGSettings)
        self.comboBoxEMGLPF.currentTextChanged.connect(self.updateECGSettings)
        self.comboBoxEMGHPF.currentTextChanged.connect(self.updateECGSettings)
        self.comboBoxEMGRATE.currentTextChanged.connect(self.updateECGSettings)
        self.comboBoxBIOZCURRMAG.currentTextChanged.connect(self.updateBIOZSettings)
        self.comboBoxBIOZCURRFREQ.currentTextChanged.connect(self.updateBIOZSettings)
        self.comboBoxBIOZHPF.currentTextChanged.connect(self.updateBIOZSettings)
        self.comboBoxBIOZLPF.currentTextChanged.connect(self.updateBIOZSettings)
        self.comboBoxBIOZGAIN.currentTextChanged.connect(self.updateBIOZSettings)
        self.comboBoxBIOZRATE.currentTextChanged.connect(self.updateBIOZSettings)
        self.radioButtonBIOZMeasure.clicked.connect(self.updateMeasureType)
        self.radioButtonEMGMeasure.clicked.connect(self.updateMeasureType)


    def openPort(self):
        if self.comboBoxPorts.currentText() != NONE:
            self.ser.port = self.comboBoxPorts.currentText().split(" ")[0]
            print(self.comboBoxPorts.currentText().split(" ")[0])
            try:
                self.ser.open()
                #self.ser.flush()
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
        if self.ser.isOpen():
            self.ser.write(f"#M:{self.max30001.measurement_type.name}".encode('utf-8'))


    def create_linechart(self):
        str : recData 
        value = 0.0

        self.ser.flushInput()
        if self.ser.isOpen() == True:
            while True:
                try:
                    recData = self.ser.readline().decode('utf-8')
                    value = float(recData.split('#')[1])
                    print(value)
                    break
                except:
                    print("corrupted data...")
                    self.ser.flushInput()
                    return

        if (value > 200) or(value < -200):
            print("[INFO] overlimit...")
            return

        timenow = QtCore.QDateTime.currentDateTime()

        if self.maxData.count() == 0:
            self.axis_x.setMin(timenow)
            self.minValue = value
            self.maxValue = value

        self.rawData.append((timenow.time().toString("HH:mm:ss:zz"), value))
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
        self.rawData.clear()
        self.minValue = 0
        self.maxValue = 0


    def startMeasurement(self):            
        self.graphTimer.start(1)


    def stopMeasurement(self):
        self.serThreadRdy = False
        self.graphTimer.stop()


    def getDataFromSerial(self):
        pass


    def updateECGSettings(self):
        
        self.max30001.ecg.gain = max_setup.ECG_GAIN_t(self.comboBoxEMGGAIN.currentIndex()+1)
        self.max30001.ecg.lpf = max_setup.ECG_LPF_t(self.comboBoxEMGLPF.currentIndex()+1)
        self.max30001.ecg.hpf = max_setup.ECG_HPF_t(self.comboBoxEMGHPF.currentIndex()+1)
        self.max30001.ecg.rate = max_setup.ECG_RATE_t(self.comboBoxEMGRATE.currentIndex()+1)
        print(self.max30001.ecg)
        

    def updateBIOZSettings(self):
        self.max30001.bioz.inductionCurrent = max_setup.InductionCurrent_t(self.comboBoxBIOZCURRMAG.currentIndex()+1)
        self.max30001.bioz.inductionFreq = max_setup.InductionFreq_t(self.comboBoxBIOZCURRFREQ.currentIndex()+1)
        self.max30001.bioz.hpf = max_setup.BIOZ_HPF_t(self.comboBoxBIOZHPF.currentIndex()+1)
        self.max30001.bioz.lpf = max_setup.BIOZ_LPF_t(self.comboBoxBIOZLPF.currentIndex()+1)
        self.max30001.bioz.gain = max_setup.BIOZ_GAIN_t(self.comboBoxBIOZGAIN.currentIndex()+1)
        self.max30001.bioz.rate = max_setup.BIOZ_RATE_t(self.comboBoxBIOZRATE.currentIndex()+1)
        print(self.max30001.bioz)


    def updateMeasureType(self):
        if self.radioButtonEMGMeasure.isChecked():
            self.max30001.measurement_type = max_setup.Measurement_t.ECG
        elif self.radioButtonBIOZMeasure.isChecked():
            self.max30001.measurement_type = max_setup.Measurement_t.BIOZ
        else:
            self.max30001.measurement_type = max_setup.Measurement_t.UNDEFINED

        print(self.max30001.measurement_type)


    def saveFile(self):
        filter = ("Coma separated files (*.csv)")
        dlg = QtWidgets.QFileDialog()
        dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
        dlg.setNameFilters([filter])
        filenames = QtCore.QStringListModel()

        if dlg.exec_():
            filenames = dlg.selectedFiles()
        
        with open(filenames[0], 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.rawData)

        print("CSV saved")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.MainWindow.show()
    app.exec_()
    print("Finish")
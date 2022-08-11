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

        self.maxValueEMG = 0.0
        self.maxValueBIOZ = 0.0
        self.minValueEMG = 0.0
        self.minValueBIOZ = 0.0
        self.rawData = []
        self.ecgSample    = 0
        self.biozSample   = 0

        # --------------- chart settings ---------------
        self.chartDataEMG = QChart()
        self.axis_y_emg = QValueAxis()
        self.axis_y_emg.setTitleText("mV")
        

        self.chartDataBIOZ = QChart()
        self.axis_y_bioz = QValueAxis()
        self.axis_y_bioz.setTitleText('Ohm')

        #self.axis_x_emg = QDateTimeAxis()
        #self.axis_x_emg.setFormat("hh:mm:ss")
        #self.axis_x_emg.setTitleText("Time")
        self.axis_x_emg = QValueAxis()
        self.axis_x_emg.setTitleText('Sample')

        #self.axis_x_bioz = QDateTimeAxis()
        #self.axis_x_bioz.setFormat("hh:mm:ss")
        #self.axis_x_bioz.setTitleText("Time")
        self.axis_x_bioz = QValueAxis()
        self.axis_x_bioz.setTitleText('Sample')

        self.maxEMG = QLineSeries(self.MainWindow)
        self.maxEMG.setName("EMG")

        self.maxBIOZ = QLineSeries(self.MainWindow)
        self.maxBIOZ.setName("BIOZ")

        self.chartDataEMG.addSeries(self.maxEMG)
        self.chartDataEMG.setAnimationOptions(QChart.NoAnimation)
        self.chartDataEMG.setTitle("MAX30001")
        self.chartDataEMG.legend().setVisible(True)
        self.chartDataEMG.legend().setAlignment(Qt.AlignBottom)
        self.chartDataEMG.addAxis(self.axis_y_emg, QtCore.Qt.AlignLeft)
        self.chartDataEMG.addAxis(self.axis_x_emg, QtCore.Qt.AlignBottom)

        self.maxEMG.attachAxis(self.axis_x_emg)
        self.maxEMG.attachAxis(self.axis_y_emg)

        self.GraphEMG.setChart(self.chartDataEMG)

        self.chartDataBIOZ.addSeries(self.maxBIOZ)
        self.chartDataBIOZ.setAnimationOptions(QChart.NoAnimation)
        self.chartDataBIOZ.setTitle("MAX30001")
        self.chartDataBIOZ.legend().setVisible(True)
        self.chartDataBIOZ.legend().setAlignment(Qt.AlignBottom)
        self.chartDataBIOZ.addAxis(self.axis_y_bioz, QtCore.Qt.AlignLeft)
        self.chartDataBIOZ.addAxis(self.axis_x_bioz, QtCore.Qt.AlignBottom)

        self.maxBIOZ.attachAxis(self.axis_x_bioz)
        self.maxBIOZ.attachAxis(self.axis_y_bioz)

        self.GraphBIOZ.setChart(self.chartDataBIOZ)

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
        self.radioButtonEMG_BIOZ.clicked.connect(self.updateMeasureType)
        self.horizontalSliderRatio.valueChanged.connect(self.updateRatio)

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
                    cmd = recData.split('#')[1][0]
                    value = float(recData.split('#')[1][1:])
                    print(value)
                    break
                except:
                    print("corrupted data...")
                    self.ser.flushInput()
                    return

        if (value > 300) or (value < -300):
            print("[INFO] overlimit...")
            return

        timenow = QtCore.QDateTime.currentDateTime()

        if cmd == 'E':
            if self.maxEMG.count() == 0:
                self.axis_x_emg.setMin(self.ecgSample)
                self.minValueEMG = value
                self.maxValueEMG = value

            #self.rawData.append((timenow.time().toString("HH:mm:ss:zz"), value))
            self.rawData.append((self.ecgSample, value))
            #self.maxEMG.append(timenow.toMSecsSinceEpoch(), value)
            self.maxEMG.append(self.ecgSample, value)
            self.axis_x_emg.setMax(self.ecgSample)
            self.ecgSample += 1

            if value < self.minValueEMG:
                self.minValueEMG = value
            if value > self.maxValueEMG:
                self.maxValueEMG = value

            self.axis_y_emg.setMax(self.maxValueEMG)
            self.axis_y_emg.setMin(self.minValueEMG)

        elif cmd == 'B':
            if self.maxBIOZ.count() == 0:
                self.axis_x_bioz.setMin(self.ecgSample)
                self.minValueBIOZ = value
                self.maxValueBIOZ = value

            #self.rawData.append((timenow.time().toString("HH:mm:ss:zz"), value))
            self.rawData.append((self.biozSample, value))
            #self.maxBIOZ.append(timenow.toMSecsSinceEpoch(), value)
            self.maxBIOZ.append(self.biozSample, value)
            self.axis_x_bioz.setMax(self.biozSample)
            self.biozSample += 1

            if value < self.minValueBIOZ:
                self.minValueBIOZ = value
            if value > self.maxValueBIOZ:
                self.maxValueBIOZ = value

            self.axis_y_bioz.setMax(self.maxValueBIOZ)
            self.axis_y_bioz.setMin(self.minValueBIOZ)


    def clearGraph(self):
        self.maxEMG.clear()
        self.maxBIOZ.clear()
        self.rawData.clear()
        self.minValueEMG = 0
        self.maxValueEMG = 0
        self.minValueBIOZ = 0
        self.maxValueBIOZ = 0


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
        elif self.radioButtonEMG_BIOZ.isChecked():
            self.max30001.measurement_type = max_setup.Measurement_t.MIXED
        else:
            self.max30001.measurement_type = max_setup.Measurement_t.UNDEFINED

        print(self.max30001.measurement_type)

    def updateRatio(self):
        self.max30001.bioz_ecg.ratio = self.horizontalSliderRatio.value()

        print(self.max30001.bioz_ecg)


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
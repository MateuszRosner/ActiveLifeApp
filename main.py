import threading
import sys
import time
import serial
import serial.tools.list_ports
import csv
import max_setup
import winsound
import numpy as np
import scipy.signal as sig

from ui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtChart import QChart, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt

from scipy.signal import find_peaks
from scipy import integrate
#import pywt


CHART_MAX_SAMPLES = 250
SOUND_FREQ        = 4000
SOUND_DURATION    = 500

class MyWindow(Ui_MainWindow):
# ---------------class init functions---------------
    def __init__(self):
        super(MyWindow, self).__init__()
        self.MainWindow = QtWidgets.QMainWindow()
        self.setupUi(self.MainWindow)
        self.listSerialPorts()
        self.ser=serial.Serial(
            baudrate    =  115200,
            parity      =  serial.PARITY_NONE,
            stopbits    =  serial.STOPBITS_ONE,
            bytesize    =  serial.EIGHTBITS,
            timeout     =  0.5)

        self.serThreadRdy = False
        
        self.serialThread        = threading.Thread(target=self.getDataFromSerial)
        self.serialThread.daemon = True

        self.graphTimer         = QtCore.QTimer()
        self.trainingTimer      = QtCore.QTimer()

        self.trainingCounter    = 0
        self.corruptedData      = 0
        self.packets            = 0

        self.maxValueEMG_0    = 0.0
        self.maxValueBIO_0    = 0.0
        self.minValueEMG_0    = 0.0
        self.minValueBIOZ_0   = 0.0
        self.minValueMMG_0    = 0.0
        self.maxValueMMG_0    = 0.0
        self.maxValueEMG_1    = 0.0
        self.maxValueBIO_1    = 0.0
        self.minValueEMG_1    = 0.0
        self.minValueBIOZ_1   = 0.0
        self.minValueMMG_1    = 0.0
        self.maxValueMMG_1    = 0.0
        self.rawData = []
        self.rawData.append(("ecg smp", "ecg val", "bioz smp", "bioz val", "mmg smp", "mmg val"))
        self.ecgSample_0    = 0
        self.biozSample_0   = 0
        self.mmgSample_0    = 0
        self.ecgSample_1    = 0
        self.biozSample_1   = 0
        self.mmgSample_1    = 0

        self.bpmSamples     = []

        # --------------- chart settings ---------------
        self.chartDataEMG_0 = QChart()
        self.axis_y_emg_0 = QValueAxis()
        self.axis_y_emg_0.setTitleText("mV")

        self.chartDataEMG_1 = QChart()
        self.axis_y_emg_1 = QValueAxis()
        self.axis_y_emg_1.setTitleText("mV")
        
        self.chartDataBIOZ_0 = QChart()
        self.axis_y_bioz_0 = QValueAxis()
        self.axis_y_bioz_0.setTitleText('Ohm')

        self.chartDataBIOZ_1 = QChart()
        self.axis_y_bioz_1 = QValueAxis()
        self.axis_y_bioz_1.setTitleText('Ohm')

        self.chartDataMMG_0 = QChart()
        self.axis_y_mmg_0 = QValueAxis()
        self.axis_y_mmg_0.setTitleText('Value')

        self.chartDataMMG_1 = QChart()
        self.axis_y_mmg_1 = QValueAxis()
        self.axis_y_mmg_1.setTitleText('Value')

        self.axis_x_emg_0 = QValueAxis()
        self.axis_x_emg_0.setTitleText('Sample')

        self.axis_x_emg_1 = QValueAxis()
        self.axis_x_emg_1.setTitleText('Sample')

        self.axis_x_bioz_0 = QValueAxis()
        self.axis_x_bioz_0.setTitleText('Sample')

        self.axis_x_bioz_1 = QValueAxis()
        self.axis_x_bioz_1.setTitleText('Sample')

        self.axis_x_mmg_0 = QValueAxis()
        self.axis_x_mmg_0.setTitleText('Sample')

        self.axis_x_mmg_1 = QValueAxis()
        self.axis_x_mmg_1.setTitleText('Sample')

        self.maxEMG_0 = QLineSeries(self.MainWindow)
        self.maxEMG_0.setName("EMG")

        self.maxEMG_1 = QLineSeries(self.MainWindow)
        self.maxEMG_1.setName("EMG")

        self.maxBIOZ_0 = QLineSeries(self.MainWindow)
        self.maxBIOZ_0.setName("BIOZ")

        self.maxBIOZ_1 = QLineSeries(self.MainWindow)
        self.maxBIOZ_1.setName("BIOZ")

        self.maxMMG_0 = QLineSeries(self.MainWindow)
        self.maxMMG_0.setName("MMG")

        self.maxMMG_1 = QLineSeries(self.MainWindow)
        self.maxMMG_1.setName("MMG")

        self.chartDataEMG_0.addSeries(self.maxEMG_0)
        self.chartDataEMG_0.setAnimationOptions(QChart.NoAnimation)
        self.chartDataEMG_0.setTitle("MADx")
        self.chartDataEMG_0.legend().setVisible(True)
        self.chartDataEMG_0.legend().setAlignment(Qt.AlignBottom)
        self.chartDataEMG_0.addAxis(self.axis_y_emg_0, QtCore.Qt.AlignLeft)
        self.chartDataEMG_0.addAxis(self.axis_x_emg_0, QtCore.Qt.AlignBottom)

        self.chartDataEMG_1.addSeries(self.maxEMG_1)
        self.chartDataEMG_1.setAnimationOptions(QChart.NoAnimation)
        self.chartDataEMG_1.setTitle("MADx")
        self.chartDataEMG_1.legend().setVisible(True)
        self.chartDataEMG_1.legend().setAlignment(Qt.AlignBottom)
        self.chartDataEMG_1.addAxis(self.axis_y_emg_1, QtCore.Qt.AlignLeft)
        self.chartDataEMG_1.addAxis(self.axis_x_emg_1, QtCore.Qt.AlignBottom)

        self.maxEMG_0.attachAxis(self.axis_x_emg_0)
        self.maxEMG_0.attachAxis(self.axis_y_emg_0)

        self.maxEMG_1.attachAxis(self.axis_x_emg_1)
        self.maxEMG_1.attachAxis(self.axis_y_emg_1)

        self.Graph1.setChart(self.chartDataEMG_0)

        self.chartDataBIOZ_0.addSeries(self.maxBIOZ_0)
        self.chartDataBIOZ_0.setAnimationOptions(QChart.NoAnimation)
        self.chartDataBIOZ_0.setTitle("MAX30001")
        self.chartDataBIOZ_0.legend().setVisible(True)
        self.chartDataBIOZ_0.legend().setAlignment(Qt.AlignBottom)
        self.chartDataBIOZ_0.addAxis(self.axis_y_bioz_0, QtCore.Qt.AlignLeft)
        self.chartDataBIOZ_0.addAxis(self.axis_x_bioz_0, QtCore.Qt.AlignBottom)

        self.chartDataBIOZ_1.addSeries(self.maxBIOZ_1)
        self.chartDataBIOZ_1.setAnimationOptions(QChart.NoAnimation)
        self.chartDataBIOZ_1.setTitle("MAX30001")
        self.chartDataBIOZ_1.legend().setVisible(True)
        self.chartDataBIOZ_1.legend().setAlignment(Qt.AlignBottom)
        self.chartDataBIOZ_1.addAxis(self.axis_y_bioz_1, QtCore.Qt.AlignLeft)
        self.chartDataBIOZ_1.addAxis(self.axis_x_bioz_1, QtCore.Qt.AlignBottom)

        self.maxBIOZ_0.attachAxis(self.axis_x_bioz_0)
        self.maxBIOZ_0.attachAxis(self.axis_y_bioz_0)

        self.maxBIOZ_1.attachAxis(self.axis_x_bioz_1)
        self.maxBIOZ_1.attachAxis(self.axis_y_bioz_1)

        self.Graph2.setChart(self.chartDataBIOZ_0)

        self.chartDataMMG_0.addSeries(self.maxMMG_0)
        self.chartDataMMG_0.setAnimationOptions(QChart.NoAnimation)
        self.chartDataMMG_0.setTitle("MAX30001")
        self.chartDataMMG_0.legend().setVisible(True)
        self.chartDataMMG_0.legend().setAlignment(Qt.AlignBottom)
        self.chartDataMMG_0.addAxis(self.axis_y_mmg_0, QtCore.Qt.AlignLeft)
        self.chartDataMMG_0.addAxis(self.axis_x_mmg_0, QtCore.Qt.AlignBottom)

        self.chartDataMMG_1.addSeries(self.maxMMG_1)
        self.chartDataMMG_1.setAnimationOptions(QChart.NoAnimation)
        self.chartDataMMG_1.setTitle("MAX30001")
        self.chartDataMMG_1.legend().setVisible(True)
        self.chartDataMMG_1.legend().setAlignment(Qt.AlignBottom)
        self.chartDataMMG_1.addAxis(self.axis_y_mmg_1, QtCore.Qt.AlignLeft)
        self.chartDataMMG_1.addAxis(self.axis_x_mmg_1, QtCore.Qt.AlignBottom)

        self.maxMMG_0.attachAxis(self.axis_x_mmg_0)
        self.maxMMG_0.attachAxis(self.axis_y_mmg_0)

        self.maxMMG_1.attachAxis(self.axis_x_mmg_1)
        self.maxMMG_1.attachAxis(self.axis_y_mmg_1)

        self.Graph3.setChart(self.chartDataMMG_0)

        self.max30001 = max_setup.max30001()

        self.comboBoxChart1.addItems(["MAD0 EMG", "MAD0 BIOZ", "MAD0 MMG", "MAD1 EMG", "MAD1 BIOZ", "MAD1 MMG"])
        self.comboBoxChart2.addItems(["MAD0 EMG", "MAD0 BIOZ", "MAD0 MMG", "MAD1 EMG", "MAD1 BIOZ", "MAD1 MMG"])
        self.comboBoxChart3.addItems(["MAD0 EMG", "MAD0 BIOZ", "MAD0 MMG", "MAD1 EMG", "MAD1 BIOZ", "MAD1 MMG"])

        self.comboBoxDevice.addItems(["MAD0", "MAD1"])

    # --------------- signals - slots config ---------------
        self.pushButtonConnect.clicked.connect(self.openPort)
        self.pushButtonStart.clicked.connect(self.startMeasurement)
        self.pushButtonStop.clicked.connect(self.stopMeasurement)
        self.pushButtonClearGraph.clicked.connect(self.clearGraph)
        self.pushButtonSave.clicked.connect(self.saveFile)
        self.pushButtonSet.clicked.connect(self.setActualSettings)
        self.radioButtonBIOZMeasure.clicked.connect(self.updateMeasureType)
        self.radioButtonEMGMeasure.clicked.connect(self.updateMeasureType)
        self.radioButtonEMG_BIOZ.clicked.connect(self.updateMeasureType)
        self.comboBoxChart1.currentTextChanged.connect(self.setChart1)
        self.comboBoxChart2.currentTextChanged.connect(self.setChart2)
        self.comboBoxChart3.currentTextChanged.connect(self.setChart3)
        self.trainingTimer.timeout.connect(self.timerCountTick)

    def openPort(self):
        if self.comboBoxPorts.currentText() != None:
            self.ser.port = self.comboBoxPorts.currentText().split(" ")[0]
            print(self.comboBoxPorts.currentText().split(" ")[0])
            try:
                self.ser.open()
                self.serialThread.start()
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
            print(f"#M:{self.max30001.measurement_type.name}".encode('utf-8'))


    def create_linechart(self, cmd, values):
        if cmd == 'E':
            for idx, value in enumerate(values):
                value = float(value)
                if idx > 0:
                    self.rawData.append((self.ecgSample_0, value, 0, 0, 0, 0))
                    self.ecgSample_0 += 1
                    continue

                if self.maxEMG_0.count() == 0:
                    self.axis_x_emg_0.setMin(self.ecgSample_0)
                    self.minValueEMG_0 = value
                    self.maxValueEMG_0 = value

                elif self.maxEMG_0.count() == CHART_MAX_SAMPLES:
                    self.clearGraphEMG()

                self.maxEMG_0.append(self.ecgSample_0, value)
                self.rawData.append((self.ecgSample_0, value, 0, 0, 0, 0))
                self.axis_x_emg_0.setMax(self.ecgSample_0)
                self.ecgSample_0 += 1

                if value < self.minValueEMG_0:
                    self.minValueEMG_0 = value
                if value > self.maxValueEMG_0:
                    self.maxValueEMG_0 = value

                self.axis_y_emg_0.setMax(self.maxValueEMG_0)
                self.axis_y_emg_0.setMin(self.minValueEMG_0)

        elif cmd == 'B':
            for idx, value in enumerate(values):
                value = float(value)
                if idx > 0:
                    self.rawData.append((0, 0, self.biozSample_0, value, 0, 0))
                    self.biozSample_0 += 1
                    continue

                if self.maxBIOZ_0.count() == 0:
                    self.axis_x_bioz_0.setMin(self.biozSample_0)
                    self.minValueBIOZ_0 = value
                    self.maxValueBIOZ_0 = value

                elif self.maxBIOZ_0.count() == CHART_MAX_SAMPLES:
                    self.clearGraphBIOZ()

                self.maxBIOZ_0.append(self.biozSample_0, value)
                self.rawData.append((0, 0, self.biozSample_0, value, 0, 0))
                self.axis_x_bioz_0.setMax(self.biozSample_0)
                self.biozSample_0 += 1

                if value < self.minValueBIOZ_0:
                    self.minValueBIOZ_0 = value
                if value > self.maxValueBIOZ_0:
                    self.maxValueBIOZ_0 = value

                self.axis_y_bioz_0.setMax(self.maxValueBIOZ_0)
                self.axis_y_bioz_0.setMin(self.minValueBIOZ_0)

        elif cmd == 'M':
            for idx, value in enumerate(values):
                value = float(value)
                if idx > 0:
                    self.rawData.append((0, 0, 0, 0, self.mmgSample_0, value))
                    self.mmgSample_0 += 1
                    self.bpmSamples.append(value)
                    continue
                
                if self.maxMMG_0.count() == 0:
                    self.axis_x_mmg_0.setMin(self.mmgSample_0)
                    self.minValueMMG_0 = value
                    self.maxValueMMG_0 = value

                elif self.maxMMG_0.count() == CHART_MAX_SAMPLES:
                    self.clearGraphMMG()

                self.maxMMG_0.append(self.mmgSample_0, value)
                self.bpmSamples.append(value)
                self.rawData.append((0, 0, 0, 0, self.mmgSample_0, value))
                self.axis_x_mmg_0.setMax(self.mmgSample_0)
                self.mmgSample_0 += 1

                if value < self.minValueMMG_0:
                    self.minValueMMG_0 = value
                if value > self.maxValueMMG_0:
                    self.maxValueMMG_0 = value

                self.axis_y_mmg_0.setMax(self.maxValueMMG_0)
                self.axis_y_mmg_0.setMin(self.minValueMMG_0)


    def clearGraph(self):
        self.maxEMG_0.clear()
        self.maxBIOZ_0.clear()
        self.maxMMG_0.clear()
        self.rawData.clear()
        self.rawData.append(("emg smp", "emg val", "bioz smp", "bioz val", "mmg smp", "mmg val"))
        self.minValueEMG_0    = 0
        self.maxValueEMG_0    = 0
        self.minValueBIOZ_0   = 0
        self.maxValueBIOZ_0   = 0
        self.minValueMMG_0    = 0
        self.maxValueMMG_0    = 0
        self.ecgSample_0      = 0
        self.biozSample_0     = 0
        self.mmgSample_0      = 0
        self.trainingCounter  = 0
        self.labelTrainingTime.setText(f"{self.trainingCounter} s")

    def clearGraphEMG(self):
        self.maxEMG_0.clear()
        self.axis_x_emg_0.setMin(self.ecgSample_0)
        #self.minValueEMG_0    = 0
        self.maxValueEMG_0    = 0
        self.saveBckpFile()


    def clearGraphBIOZ(self):
        self.maxBIOZ_0.clear()
        self.axis_x_bioz_0.setMin(self.biozSample_0)
        self.maxValueBIOZ_0   = 0
        self.saveBckpFile()


    def clearGraphMMG(self):
        self.calcBPM()
        self.maxMMG_0.clear()
        self.bpmSamples.clear()
        self.axis_x_mmg_0.setMin(self.mmgSample_0)
        self.maxValueMMG_0    = 0
        self.saveBckpFile()
        


    def startMeasurement(self):
        if self.ser.isOpen() == True:
            self.saveBckpFile() 
            self.ser.flush()
            self.ser.flushInput()           
            self.serThreadRdy = True
            self.trainingTimer.start(1000)
        

    def stopMeasurement(self):
        self.serThreadRdy = False
        self.trainingTimer.stop()


    def getDataFromSerial(self):
        print("[INFO] Serial thread started!")
        while True:
            if self.serThreadRdy == True:
                values = []
                str: cmd
                try:
                    recData = self.ser.readline().decode('utf-8')
                    self.packets += 1
                    cmd = recData.split('#')[1][0]

                    values = (recData.split('#')[1][1:].split(',')[1:])
                    print(values)    
                    self.create_linechart(cmd, values)

                except Exception as err:
                    print("corrupted data...")
                    print(err)
                    self.ser.flushInput()
                    self.corruptedData += 1
                    winsound.Beep(duration=SOUND_DURATION, frequency=SOUND_FREQ)

                self.labelPacketLoss.setText("{:.3f} %" .format(self.corruptedData * 100.0 / self.packets))
            else:
                time.sleep(0.5)


    def updateECGSettings(self):
        self.max30001.ecg.gain = max_setup.ECG_GAIN_t(self.comboBoxEMGGAIN.currentIndex()+1)
        self.max30001.ecg.lpf  = max_setup.ECG_LPF_t(self.comboBoxEMGLPF.currentIndex()+1)
        self.max30001.ecg.hpf  = max_setup.ECG_HPF_t(self.comboBoxEMGHPF.currentIndex()+1)
        self.max30001.ecg.rate = max_setup.ECG_RATE_t(self.comboBoxEMGRATE.currentIndex()+1)
        print(self.max30001.ecg)
        

    def updateBIOZSettings(self):
        self.max30001.bioz.inductionCurrent = max_setup.InductionCurrent_t(self.comboBoxBIOZCURRMAG.currentIndex()+1)
        self.max30001.bioz.inductionFreq    = max_setup.InductionFreq_t(self.comboBoxBIOZCURRFREQ.currentIndex()+1)
        self.max30001.bioz.hpf              = max_setup.BIOZ_HPF_t(self.comboBoxBIOZHPF.currentIndex()+1)
        self.max30001.bioz.lpf              = max_setup.BIOZ_LPF_t(self.comboBoxBIOZLPF.currentIndex()+1)
        self.max30001.bioz.gain             = max_setup.BIOZ_GAIN_t(self.comboBoxBIOZGAIN.currentIndex()+1)
        self.max30001.bioz.rate             = max_setup.BIOZ_RATE_t(self.comboBoxBIOZRATE.currentIndex()+1)
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
        
        try:
            with open(filenames[0], 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.rawData)

            print("CSV saved")
        except:
            print("Failed to save CSV")

    def saveBckpFile(self):
        try:
            with open("backup.csv", 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerows(self.rawData)

            print("CSV saved")
        except:
            print("Failed to save CSV")

    def setChart1(self):
        if self.comboBoxChart1.currentText() == "MAD0 EMG":
            self.Graph1.setChart(self.chartDataEMG_0)
        elif self.comboBoxChart1.currentText() == "MAD0 BIOZ":
            self.Graph1.setChart(self.chartDataBIOZ_0)
        elif self.comboBoxChart1.currentText() == "MAD0 MMG":
            self.Graph1.setChart(self.chartDataMMG_0)

    def setChart2(self):
        if self.comboBoxChart2.currentText() == "MAD0 EMG":
            self.Graph2.setChart(self.chartDataEMG_0)
        elif self.comboBoxChart2.currentText() == "MAD0 BIOZ":
            self.Graph2.setChart(self.chartDataBIOZ_0)
        elif self.comboBoxChart2.currentText() == "MAD0 MMG":
            self.Graph2.setChart(self.chartDataMMG_0)

    def setChart3(self):
        if self.comboBoxChart3.currentText() == "MAD0 EMG":
            self.Graph3.setChart(self.chartDataEMG_0)
        elif self.comboBoxChart3.currentText() == "MAD0 BIOZ":
            self.Graph3.setChart(self.chartDataBIOZ_0)
        elif self.comboBoxChart3.currentText() == "MAD0 MMG":
            self.Graph3.setChart(self.chartDataMMG_0)

    def timerCountTick(self):
        self.trainingCounter += 1
        self.labelTrainingTime.setText(f"{self.trainingCounter} s")

    def calcBPM(self):
        fs = 150
        L = 100 # rząd filtru
        fdp = sig.firwin(L, 4, window='hamming', pass_zero=True, fs=fs)
        width = self.spinBoxWidowWidth.value()
        MMG = self.bpmSamples[-width:]
        MMG = MMG - np.mean(MMG) # usunięcie składowe DC
        MMG = MMG * -1
        MMG_int = integrate.cumtrapz(MMG, initial=0) # calkowanie sygnalu
        MMG_filtr = sig.lfilter(fdp, 1, MMG) # filtracja LP 4Hz
        MMG_filtr = sig.lfilter(fdp, 1, MMG_filtr) # filtracja LP 4Hz
        MMG_int = MMG_filtr #integrate.cumtrapz(MMG_filtr, initial=0) # calkowanie sygnalu
        MMG_corr = sig.correlate(MMG_int, MMG_int) # autokorelacja
        MMG_corr = MMG_corr[len(MMG_corr)//2:] # przesuniecie od max, ograniczenie danych
        MMG_corr = MMG_corr / MMG_corr[0] # normalizacja

        peaks_corr, _ = find_peaks(MMG_corr, distance=50)
        pulse = 60 / (peaks_corr[0] * 1/fs)

        self.labelHR.setText("{:.2f} bpm" .format(pulse))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.MainWindow.show()
    app.exec_()
    print("Finish")
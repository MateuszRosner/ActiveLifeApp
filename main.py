import threading
import sys
import time
import serial
import serial.tools.list_ports
import csv
import max_setup

from ui import Ui_MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtChart import QChart, QLineSeries, QValueAxis
from PyQt5.QtCore import Qt

CHART_MAX_SAMPLES = 500

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

        self.graphTimer          = QtCore.QTimer()

        self.maxValueEMG    = 0.0
        self.maxValueBIOZ   = 0.0
        self.minValueEMG    = 0.0
        self.minValueBIOZ   = 0.0
        self.minValueMMG    = 0.0
        self.maxValueMMG    = 0.0
        self.rawData = []
        self.rawData.append(("ecg smp", "ecg val", "bioz smp", "bioz val", "mmg smp", "mmg val"))
        self.ecgSample    = 0
        self.biozSample   = 0
        self.mmgSample    = 0

        # --------------- chart settings ---------------
        self.chartDataEMG = QChart()
        self.axis_y_emg = QValueAxis()
        self.axis_y_emg.setTitleText("mV")
        
        self.chartDataBIOZ = QChart()
        self.axis_y_bioz = QValueAxis()
        self.axis_y_bioz.setTitleText('Ohm')

        self.chartDataMMG = QChart()
        self.axis_y_mmg = QValueAxis()
        self.axis_y_mmg.setTitleText('vlaue')

        self.axis_x_emg = QValueAxis()
        self.axis_x_emg.setTitleText('Sample')

        self.axis_x_bioz = QValueAxis()
        self.axis_x_bioz.setTitleText('Sample')

        self.axis_x_mmg = QValueAxis()
        self.axis_x_mmg.setTitleText('Sample')

        self.maxEMG = QLineSeries(self.MainWindow)
        self.maxEMG.setName("EMG")

        self.maxBIOZ = QLineSeries(self.MainWindow)
        self.maxBIOZ.setName("BIOZ")

        self.maxMMG = QLineSeries(self.MainWindow)
        self.maxMMG.setName("MMG")

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

        self.chartDataMMG.addSeries(self.maxMMG)
        self.chartDataMMG.setAnimationOptions(QChart.NoAnimation)
        self.chartDataMMG.setTitle("MAX30001")
        self.chartDataMMG.legend().setVisible(True)
        self.chartDataMMG.legend().setAlignment(Qt.AlignBottom)
        self.chartDataMMG.addAxis(self.axis_y_mmg, QtCore.Qt.AlignLeft)
        self.chartDataMMG.addAxis(self.axis_x_mmg, QtCore.Qt.AlignBottom)

        self.maxMMG.attachAxis(self.axis_x_mmg)
        self.maxMMG.attachAxis(self.axis_y_mmg)

        self.GraphMMG.setChart(self.chartDataMMG)

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
        #self.graphTimer.timeout.connect(self.create_linechart)
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
                    self.rawData.append((self.ecgSample, value, 0, 0, 0, 0))
                    self.ecgSample += 1
                    continue

                if self.maxEMG.count() == 0:
                    self.axis_x_emg.setMin(self.ecgSample)
                    self.minValueEMG = value
                    self.maxValueEMG = value

                elif self.maxEMG.count() == CHART_MAX_SAMPLES:
                    self.clearGraphEMG()

                self.maxEMG.append(self.ecgSample, value)
                self.rawData.append((self.ecgSample, value, 0, 0, 0, 0))
                self.axis_x_emg.setMax(self.ecgSample)
                self.ecgSample += 1

                if value < self.minValueEMG:
                    self.minValueEMG = value
                if value > self.maxValueEMG:
                    self.maxValueEMG = value

                self.axis_y_emg.setMax(self.maxValueEMG)
                self.axis_y_emg.setMin(self.minValueEMG)

        elif cmd == 'B':
            for idx, value in enumerate(values):
                value = float(value)
                if idx > 0:
                    self.rawData.append((0, 0, self.biozSample, value, 0, 0))
                    self.biozSample += 1
                    continue

                if self.maxBIOZ.count() == 0:
                    self.axis_x_bioz.setMin(self.biozSample)
                    self.minValueBIOZ = value
                    self.maxValueBIOZ = value

                elif self.maxBIOZ.count() == CHART_MAX_SAMPLES:
                    self.clearGraphBIOZ()

                self.maxBIOZ.append(self.biozSample, value)
                self.rawData.append((0, 0, self.biozSample, value, 0, 0))
                self.axis_x_bioz.setMax(self.biozSample)
                self.biozSample += 1

                if value < self.minValueBIOZ:
                    self.minValueBIOZ = value
                if value > self.maxValueBIOZ:
                    self.maxValueBIOZ = value

                self.axis_y_bioz.setMax(self.maxValueBIOZ)
                self.axis_y_bioz.setMin(self.minValueBIOZ)

        elif cmd == 'M':
            for idx, value in enumerate(values):
                value = float(value)
                if idx > 0:
                    self.rawData.append((0, 0, 0, 0, self.mmgSample, value))
                    self.mmgSample += 1
                    continue
                
                if self.maxMMG.count() == 0:
                    self.axis_x_mmg.setMin(self.mmgSample)
                    self.minValueMMG = value
                    self.maxValueMMG = value

                elif self.maxMMG.count() == CHART_MAX_SAMPLES:
                    self.clearGraphMMG()

                self.maxMMG.append(self.mmgSample, value)
                self.rawData.append((0, 0, 0, 0, self.mmgSample, value))
                self.axis_x_mmg.setMax(self.mmgSample)
                self.mmgSample += 1

                if value < self.minValueMMG:
                    self.minValueMMG = value
                if value > self.maxValueMMG:
                    self.maxValueMMG = value

                self.axis_y_mmg.setMax(self.maxValueMMG)
                self.axis_y_mmg.setMin(self.minValueMMG)


    def clearGraph(self):
        self.maxEMG.clear()
        self.maxBIOZ.clear()
        self.maxMMG.clear()
        self.rawData.clear()
        self.rawData.append(("emg smp", "emg val", "bioz smp", "bioz val", "mmg smp", "mmg val"))
        self.minValueEMG    = 0
        self.maxValueEMG    = 0
        self.minValueBIOZ   = 0
        self.maxValueBIOZ   = 0
        self.minValueMMG    = 0
        self.maxValueMMG    = 0
        self.ecgSample      = 0
        self.biozSample     = 0
        self.mmgSample      = 0

    def clearGraphEMG(self):
        self.maxEMG.clear()
        self.axis_x_emg.setMin(self.ecgSample)
        self.minValueEMG    = 0
        self.maxValueEMG    = 0
        self.saveBckpFile()


    def clearGraphBIOZ(self):
        self.maxBIOZ.clear()
        self.axis_x_bioz.setMin(self.biozSample)
        self.minValueBIOZ   = 0
        self.maxValueBIOZ   = 0
        self.saveBckpFile()


    def clearGraphMMG(self):
        self.maxMMG.clear()
        self.axis_x_mmg.setMin(self.mmgSample)
        self.minValueMMG    = 0
        self.maxValueMMG    = 0
        self.saveBckpFile()


    def startMeasurement(self):
        self.saveBckpFile() 
        self.ser.flush()
        self.ser.flushInput()           
        self.serThreadRdy = True
        

    def stopMeasurement(self):
        self.serThreadRdy = False


    def getDataFromSerial(self):
        print("[INFO] Serial thread started!")
        while True:
            if self.serThreadRdy == True:
                values = []
                str: cmd
                try:
                    recData = self.ser.readline().decode('utf-8')
                    # recData = recData.removesuffix("\r\n")
                    cmd = recData.split('#')[1][0]

                    values = (recData.split('#')[1][1:].split(',')[1:])
                    print(values)    
                    self.create_linechart(cmd, values)                
                except Exception as err:
                    print("corrupted data...")
                    print(err)
                    self.ser.flushInput()
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



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.MainWindow.show()
    app.exec_()
    print("Finish")
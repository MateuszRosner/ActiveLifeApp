# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1055, 729)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.comboBoxPorts = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxPorts.setGeometry(QtCore.QRect(10, 580, 151, 22))
        self.comboBoxPorts.setObjectName("comboBoxPorts")
        self.pushButtonConnect = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConnect.setGeometry(QtCore.QRect(10, 610, 75, 23))
        self.pushButtonConnect.setObjectName("pushButtonConnect")
        self.groupBoxMeasurements = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMeasurements.setGeometry(QtCore.QRect(10, 0, 151, 561))
        self.groupBoxMeasurements.setObjectName("groupBoxMeasurements")
        self.radioButtonEMGMeasure = QtWidgets.QRadioButton(self.groupBoxMeasurements)
        self.radioButtonEMGMeasure.setGeometry(QtCore.QRect(10, 20, 82, 17))
        self.radioButtonEMGMeasure.setObjectName("radioButtonEMGMeasure")
        self.radioButtonBIOZMeasure = QtWidgets.QRadioButton(self.groupBoxMeasurements)
        self.radioButtonBIOZMeasure.setGeometry(QtCore.QRect(10, 240, 82, 17))
        self.radioButtonBIOZMeasure.setObjectName("radioButtonBIOZMeasure")
        self.comboBoxEMGGAIN = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxEMGGAIN.setGeometry(QtCore.QRect(10, 60, 131, 22))
        self.comboBoxEMGGAIN.setObjectName("comboBoxEMGGAIN")
        self.comboBoxEMGGAIN.addItem("")
        self.comboBoxEMGGAIN.addItem("")
        self.comboBoxEMGGAIN.addItem("")
        self.comboBoxEMGGAIN.addItem("")
        self.label = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label.setGeometry(QtCore.QRect(10, 40, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 131, 16))
        self.label_2.setObjectName("label_2")
        self.comboBoxEMGLPF = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxEMGLPF.setGeometry(QtCore.QRect(10, 110, 131, 22))
        self.comboBoxEMGLPF.setObjectName("comboBoxEMGLPF")
        self.comboBoxEMGLPF.addItem("")
        self.comboBoxEMGLPF.addItem("")
        self.comboBoxEMGLPF.addItem("")
        self.comboBoxEMGLPF.addItem("")
        self.label_3 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 131, 16))
        self.label_3.setObjectName("label_3")
        self.comboBoxEMGHPF = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxEMGHPF.setGeometry(QtCore.QRect(10, 160, 131, 22))
        self.comboBoxEMGHPF.setObjectName("comboBoxEMGHPF")
        self.comboBoxEMGHPF.addItem("")
        self.comboBoxEMGHPF.addItem("")
        self.label_4 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 121, 16))
        self.label_4.setObjectName("label_4")
        self.comboBoxEMGRATE = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxEMGRATE.setGeometry(QtCore.QRect(10, 210, 131, 22))
        self.comboBoxEMGRATE.setObjectName("comboBoxEMGRATE")
        self.comboBoxEMGRATE.addItem("")
        self.comboBoxEMGRATE.addItem("")
        self.comboBoxEMGRATE.addItem("")
        self.label_5 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_5.setGeometry(QtCore.QRect(10, 260, 121, 16))
        self.label_5.setObjectName("label_5")
        self.comboBoxBIOZCURRMAG = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZCURRMAG.setGeometry(QtCore.QRect(10, 280, 131, 22))
        self.comboBoxBIOZCURRMAG.setObjectName("comboBoxBIOZCURRMAG")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.comboBoxBIOZCURRMAG.addItem("")
        self.label_6 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_6.setGeometry(QtCore.QRect(10, 310, 131, 16))
        self.label_6.setObjectName("label_6")
        self.comboBoxBIOZCURRFREQ = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZCURRFREQ.setGeometry(QtCore.QRect(10, 330, 131, 22))
        self.comboBoxBIOZCURRFREQ.setObjectName("comboBoxBIOZCURRFREQ")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.comboBoxBIOZCURRFREQ.addItem("")
        self.label_7 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_7.setGeometry(QtCore.QRect(10, 360, 131, 16))
        self.label_7.setObjectName("label_7")
        self.comboBoxBIOZHPF = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZHPF.setGeometry(QtCore.QRect(10, 430, 131, 22))
        self.comboBoxBIOZHPF.setObjectName("comboBoxBIOZHPF")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.comboBoxBIOZHPF.addItem("")
        self.label_8 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_8.setGeometry(QtCore.QRect(10, 410, 131, 16))
        self.label_8.setObjectName("label_8")
        self.comboBoxBIOZLPF = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZLPF.setGeometry(QtCore.QRect(10, 380, 131, 22))
        self.comboBoxBIOZLPF.setObjectName("comboBoxBIOZLPF")
        self.comboBoxBIOZLPF.addItem("")
        self.comboBoxBIOZLPF.addItem("")
        self.comboBoxBIOZLPF.addItem("")
        self.comboBoxBIOZLPF.addItem("")
        self.label_9 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_9.setGeometry(QtCore.QRect(10, 460, 131, 16))
        self.label_9.setObjectName("label_9")
        self.comboBoxBIOZGAIN = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZGAIN.setGeometry(QtCore.QRect(10, 480, 131, 22))
        self.comboBoxBIOZGAIN.setObjectName("comboBoxBIOZGAIN")
        self.comboBoxBIOZGAIN.addItem("")
        self.comboBoxBIOZGAIN.addItem("")
        self.comboBoxBIOZGAIN.addItem("")
        self.comboBoxBIOZGAIN.addItem("")
        self.label_10 = QtWidgets.QLabel(self.groupBoxMeasurements)
        self.label_10.setGeometry(QtCore.QRect(10, 510, 121, 16))
        self.label_10.setObjectName("label_10")
        self.comboBoxBIOZGAIN_2 = QtWidgets.QComboBox(self.groupBoxMeasurements)
        self.comboBoxBIOZGAIN_2.setGeometry(QtCore.QRect(10, 530, 131, 22))
        self.comboBoxBIOZGAIN_2.setObjectName("comboBoxBIOZGAIN_2")
        self.comboBoxBIOZGAIN_2.addItem("")
        self.comboBoxBIOZGAIN_2.addItem("")
        self.Graph = QChartView(self.centralwidget)
        self.Graph.setGeometry(QtCore.QRect(170, 10, 881, 621))
        self.Graph.setObjectName("Graph")
        self.pushButtonSet = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSet.setGeometry(QtCore.QRect(10, 640, 75, 23))
        self.pushButtonSet.setObjectName("pushButtonSet")
        self.pushButtonStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStart.setGeometry(QtCore.QRect(170, 640, 75, 23))
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.pushButtonStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStop.setGeometry(QtCore.QRect(260, 640, 75, 23))
        self.pushButtonStop.setObjectName("pushButtonStop")
        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(10, 670, 75, 23))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.statusBar = QtWidgets.QLabel(self.centralwidget)
        self.statusBar.setGeometry(QtCore.QRect(450, 640, 371, 16))
        self.statusBar.setObjectName("statusBar")
        self.pushButtonClearGraph = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonClearGraph.setGeometry(QtCore.QRect(350, 640, 75, 23))
        self.pushButtonClearGraph.setObjectName("pushButtonClearGraph")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1055, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonConnect.setText(_translate("MainWindow", "Po????cz"))
        self.groupBoxMeasurements.setTitle(_translate("MainWindow", "Pomiary"))
        self.radioButtonEMGMeasure.setText(_translate("MainWindow", "EMG"))
        self.radioButtonBIOZMeasure.setText(_translate("MainWindow", "BIO Z"))
        self.comboBoxEMGGAIN.setItemText(0, _translate("MainWindow", "20 V/V"))
        self.comboBoxEMGGAIN.setItemText(1, _translate("MainWindow", "40 V/V"))
        self.comboBoxEMGGAIN.setItemText(2, _translate("MainWindow", "80 V/V"))
        self.comboBoxEMGGAIN.setItemText(3, _translate("MainWindow", "160 V/V"))
        self.label.setText(_translate("MainWindow", "Wzmocnienie"))
        self.label_2.setText(_translate("MainWindow", "Filtr DP"))
        self.comboBoxEMGLPF.setItemText(0, _translate("MainWindow", "BYPASS"))
        self.comboBoxEMGLPF.setItemText(1, _translate("MainWindow", "40 Hz"))
        self.comboBoxEMGLPF.setItemText(2, _translate("MainWindow", "100 Hz"))
        self.comboBoxEMGLPF.setItemText(3, _translate("MainWindow", "150 Hz"))
        self.label_3.setText(_translate("MainWindow", "Filtr GP"))
        self.comboBoxEMGHPF.setItemText(0, _translate("MainWindow", "BYPASS"))
        self.comboBoxEMGHPF.setItemText(1, _translate("MainWindow", "0.5 Hz"))
        self.label_4.setText(_translate("MainWindow", "Odczyt"))
        self.comboBoxEMGRATE.setItemText(0, _translate("MainWindow", "Powolny"))
        self.comboBoxEMGRATE.setItemText(1, _translate("MainWindow", "Normalny"))
        self.comboBoxEMGRATE.setItemText(2, _translate("MainWindow", "Szybki"))
        self.label_5.setText(_translate("MainWindow", "Pr??d wzbudzenia"))
        self.comboBoxBIOZCURRMAG.setItemText(0, _translate("MainWindow", "OFF"))
        self.comboBoxBIOZCURRMAG.setItemText(1, _translate("MainWindow", "8 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(2, _translate("MainWindow", "16 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(3, _translate("MainWindow", "32 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(4, _translate("MainWindow", "48 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(5, _translate("MainWindow", "64 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(6, _translate("MainWindow", "80 uA"))
        self.comboBoxBIOZCURRMAG.setItemText(7, _translate("MainWindow", "96 uA"))
        self.label_6.setText(_translate("MainWindow", "Cz??stotliwo???? wzbudzenia"))
        self.comboBoxBIOZCURRFREQ.setItemText(0, _translate("MainWindow", "128 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(1, _translate("MainWindow", "80 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(2, _translate("MainWindow", "40 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(3, _translate("MainWindow", "10 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(4, _translate("MainWindow", "8 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(5, _translate("MainWindow", "4 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(6, _translate("MainWindow", "2 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(7, _translate("MainWindow", "1 kHz"))
        self.comboBoxBIOZCURRFREQ.setItemText(8, _translate("MainWindow", "500 Hz"))
        self.comboBoxBIOZCURRFREQ.setItemText(9, _translate("MainWindow", "250 Hz"))
        self.comboBoxBIOZCURRFREQ.setItemText(10, _translate("MainWindow", "125 Hz"))
        self.label_7.setText(_translate("MainWindow", "Filtr DP"))
        self.comboBoxBIOZHPF.setItemText(0, _translate("MainWindow", "BYPASS"))
        self.comboBoxBIOZHPF.setItemText(1, _translate("MainWindow", "125 Hz"))
        self.comboBoxBIOZHPF.setItemText(2, _translate("MainWindow", "300 Hz"))
        self.comboBoxBIOZHPF.setItemText(3, _translate("MainWindow", "800 Hz"))
        self.comboBoxBIOZHPF.setItemText(4, _translate("MainWindow", "2000 Hz"))
        self.comboBoxBIOZHPF.setItemText(5, _translate("MainWindow", "3700 Hz"))
        self.comboBoxBIOZHPF.setItemText(6, _translate("MainWindow", "7200 Hz"))
        self.label_8.setText(_translate("MainWindow", "Filtr GP"))
        self.comboBoxBIOZLPF.setItemText(0, _translate("MainWindow", "BYPASS"))
        self.comboBoxBIOZLPF.setItemText(1, _translate("MainWindow", "4 Hz"))
        self.comboBoxBIOZLPF.setItemText(2, _translate("MainWindow", "8 Hz"))
        self.comboBoxBIOZLPF.setItemText(3, _translate("MainWindow", "16 Hz"))
        self.label_9.setText(_translate("MainWindow", "Wzmocnienie"))
        self.comboBoxBIOZGAIN.setItemText(0, _translate("MainWindow", "10 V/V"))
        self.comboBoxBIOZGAIN.setItemText(1, _translate("MainWindow", "20 V/V"))
        self.comboBoxBIOZGAIN.setItemText(2, _translate("MainWindow", "40 V/V"))
        self.comboBoxBIOZGAIN.setItemText(3, _translate("MainWindow", "80 V/V"))
        self.label_10.setText(_translate("MainWindow", "Odczyt"))
        self.comboBoxBIOZGAIN_2.setItemText(0, _translate("MainWindow", "Szybki"))
        self.comboBoxBIOZGAIN_2.setItemText(1, _translate("MainWindow", "Powolny"))
        self.pushButtonSet.setText(_translate("MainWindow", "Ustaw"))
        self.pushButtonStart.setText(_translate("MainWindow", "Start pomiaru"))
        self.pushButtonStop.setText(_translate("MainWindow", "Stop pomiaru"))
        self.pushButtonSave.setText(_translate("MainWindow", "Zapisz CSV"))
        self.statusBar.setText(_translate("MainWindow", "STATUS"))
        self.pushButtonClearGraph.setText(_translate("MainWindow", "Wyczy????"))
from PyQt5.QtChart import QChartView

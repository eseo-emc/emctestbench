# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dpi_view.ui'
#
# Created: Thu Apr 26 11:07:01 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(675, 480)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setMargin(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.progress = QtGui.QProgressBar(Form)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout.addWidget(self.progress, 0, 0, 1, 5)
        self.startStop = QtGui.QPushButton(Form)
        self.startStop.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStop.setObjectName(_fromUtf8("startStop"))
        self.gridLayout.addWidget(self.startStop, 0, 5, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Frequency minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.frequencyMinimum = QtGui.QDoubleSpinBox(Form)
        self.frequencyMinimum.setDecimals(0)
        self.frequencyMinimum.setMaximum(1000000000.0)
        self.frequencyMinimum.setProperty("value", 10.0)
        self.frequencyMinimum.setObjectName(_fromUtf8("frequencyMinimum"))
        self.gridLayout.addWidget(self.frequencyMinimum, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 2, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Power minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 3, 1, 1)
        self.powerMinimum = QtGui.QDoubleSpinBox(Form)
        self.powerMinimum.setDecimals(0)
        self.powerMinimum.setMinimum(-60.0)
        self.powerMinimum.setMaximum(40.0)
        self.powerMinimum.setProperty("value", -30.0)
        self.powerMinimum.setObjectName(_fromUtf8("powerMinimum"))
        self.gridLayout.addWidget(self.powerMinimum, 1, 4, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setText(QtGui.QApplication.translate("Form", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 5, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Frequency maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.frequencyMaximum = QtGui.QDoubleSpinBox(Form)
        self.frequencyMaximum.setDecimals(0)
        self.frequencyMaximum.setMaximum(2000000000.0)
        self.frequencyMaximum.setProperty("value", 6000.0)
        self.frequencyMaximum.setObjectName(_fromUtf8("frequencyMaximum"))
        self.gridLayout.addWidget(self.frequencyMaximum, 2, 1, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setText(QtGui.QApplication.translate("Form", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Power maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 3, 1, 1)
        self.powerMaximum = QtGui.QDoubleSpinBox(Form)
        self.powerMaximum.setDecimals(0)
        self.powerMaximum.setMinimum(-60.0)
        self.powerMaximum.setMaximum(40.0)
        self.powerMaximum.setSingleStep(1.0)
        self.powerMaximum.setProperty("value", 10.0)
        self.powerMaximum.setObjectName(_fromUtf8("powerMaximum"))
        self.gridLayout.addWidget(self.powerMaximum, 2, 4, 1, 1)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setText(QtGui.QApplication.translate("Form", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 5, 1, 1)
        self.label_10 = QtGui.QLabel(Form)
        self.label_10.setText(QtGui.QApplication.translate("Form", "Frequency steps:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.frequencySteps = QtGui.QDoubleSpinBox(Form)
        self.frequencySteps.setDecimals(0)
        self.frequencySteps.setMinimum(1.0)
        self.frequencySteps.setMaximum(10000.0)
        self.frequencySteps.setProperty("value", 101.0)
        self.frequencySteps.setObjectName(_fromUtf8("frequencySteps"))
        self.gridLayout.addWidget(self.frequencySteps, 3, 1, 1, 1)
        self.label_11 = QtGui.QLabel(Form)
        self.label_11.setText(QtGui.QApplication.translate("Form", "Power search:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 3, 3, 1, 1)
        self.searchMethod = QtGui.QComboBox(Form)
        self.searchMethod.setObjectName(_fromUtf8("searchMethod"))
        self.searchMethod.addItem(_fromUtf8(""))
        self.searchMethod.setItemText(0, QtGui.QApplication.translate("Form", "IEC 62132-4", None, QtGui.QApplication.UnicodeUTF8))
        self.searchMethod.addItem(_fromUtf8(""))
        self.searchMethod.setItemText(1, QtGui.QApplication.translate("Form", "Upward successive approximation", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.searchMethod, 3, 4, 1, 2)
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setText(QtGui.QApplication.translate("Form", "Logaritmic sweep:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.logarithmic = QtGui.QCheckBox(Form)
        self.logarithmic.setText(_fromUtf8(""))
        self.logarithmic.setObjectName(_fromUtf8("logarithmic"))
        self.gridLayout.addWidget(self.logarithmic, 4, 1, 1, 1)
        self.label_12 = QtGui.QLabel(Form)
        self.label_12.setText(QtGui.QApplication.translate("Form", "Save all transmitted powers:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 4, 3, 1, 1)
        self.saveTransmittedPowers = QtGui.QCheckBox(Form)
        self.saveTransmittedPowers.setText(_fromUtf8(""))
        self.saveTransmittedPowers.setObjectName(_fromUtf8("saveTransmittedPowers"))
        self.gridLayout.addWidget(self.saveTransmittedPowers, 4, 4, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.stimulus = DropWidget(Form)
        self.stimulus.setObjectName(_fromUtf8("stimulus"))
        self.verticalLayout.addWidget(self.stimulus)
        self.criterion = DropWidget(Form)
        self.criterion.setObjectName(_fromUtf8("criterion"))
        self.verticalLayout.addWidget(self.criterion)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from gui.dropwidget_controller import DropWidget

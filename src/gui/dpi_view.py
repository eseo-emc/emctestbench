# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dpi_view.ui'
#
# Created: Tue Apr 03 16:07:03 2012
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
        Form.resize(640, 480)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, -1, 0, 0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Power minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.powerMinimum = QtGui.QDoubleSpinBox(Form)
        self.powerMinimum.setDecimals(0)
        self.powerMinimum.setMinimum(-60.0)
        self.powerMinimum.setMaximum(40.0)
        self.powerMinimum.setProperty("value", -30.0)
        self.powerMinimum.setObjectName(_fromUtf8("powerMinimum"))
        self.gridLayout.addWidget(self.powerMinimum, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setText(QtGui.QApplication.translate("Form", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 2, 1, 1)
        spacerItem = QtGui.QSpacerItem(442, 69, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 3, 4, 2)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Power maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.powerMaximum = QtGui.QDoubleSpinBox(Form)
        self.powerMaximum.setDecimals(0)
        self.powerMaximum.setMinimum(-60.0)
        self.powerMaximum.setMaximum(40.0)
        self.powerMaximum.setSingleStep(1.0)
        self.powerMaximum.setProperty("value", 10.0)
        self.powerMaximum.setObjectName(_fromUtf8("powerMaximum"))
        self.gridLayout.addWidget(self.powerMaximum, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setText(QtGui.QApplication.translate("Form", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setText(QtGui.QApplication.translate("Form", "Frequency minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.frequencyMinimum = QtGui.QDoubleSpinBox(Form)
        self.frequencyMinimum.setDecimals(0)
        self.frequencyMinimum.setMaximum(1000000000.0)
        self.frequencyMinimum.setProperty("value", 10.0)
        self.frequencyMinimum.setObjectName(_fromUtf8("frequencyMinimum"))
        self.gridLayout.addWidget(self.frequencyMinimum, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 2, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Frequency maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.frequencyMaximum = QtGui.QDoubleSpinBox(Form)
        self.frequencyMaximum.setDecimals(0)
        self.frequencyMaximum.setMaximum(2000000000.0)
        self.frequencyMaximum.setProperty("value", 6000.0)
        self.frequencyMaximum.setObjectName(_fromUtf8("frequencyMaximum"))
        self.gridLayout.addWidget(self.frequencyMaximum, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setText(QtGui.QApplication.translate("Form", "Hz", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 3, 2, 1, 1)
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setText(QtGui.QApplication.translate("Form", "Logaritmic sweep:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.logarithmic = QtGui.QCheckBox(Form)
        self.logarithmic.setText(_fromUtf8(""))
        self.logarithmic.setObjectName(_fromUtf8("logarithmic"))
        self.gridLayout.addWidget(self.logarithmic, 4, 1, 1, 1)
        self.startStop = QtGui.QPushButton(Form)
        self.startStop.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStop.setObjectName(_fromUtf8("startStop"))
        self.gridLayout.addWidget(self.startStop, 4, 3, 1, 1)
        self.progress = QtGui.QProgressBar(Form)
        self.progress.setProperty("value", 24)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout.addWidget(self.progress, 4, 4, 1, 1)
        self.dpiGraph = PlotWidget(Form)
        self.dpiGraph.setObjectName(_fromUtf8("dpiGraph"))
        self.gridLayout.addWidget(self.dpiGraph, 5, 0, 1, 5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from gui.plotwidget import PlotWidget


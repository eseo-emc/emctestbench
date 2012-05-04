# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dpiresult_view.ui'
#
# Created: Fri Apr 27 14:57:02 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DpiResult(object):
    def setupUi(self, DpiResult):
        DpiResult.setObjectName(_fromUtf8("DpiResult"))
        DpiResult.resize(729, 377)
        DpiResult.setWindowTitle(QtGui.QApplication.translate("DpiResult", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(DpiResult)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dpiGraph = MatplotlibWidget(DpiResult)
        self.dpiGraph.setObjectName(_fromUtf8("dpiGraph"))
        self.gridLayout.addWidget(self.dpiGraph, 0, 0, 1, 3)
        self.powerUnit = QtGui.QGroupBox(DpiResult)
        self.powerUnit.setTitle(QtGui.QApplication.translate("DpiResult", "Power unit", None, QtGui.QApplication.UnicodeUTF8))
        self.powerUnit.setFlat(False)
        self.powerUnit.setObjectName(_fromUtf8("powerUnit"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.powerUnit)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setMargin(3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.dBm = QtGui.QRadioButton(self.powerUnit)
        self.dBm.setText(QtGui.QApplication.translate("DpiResult", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.dBm.setChecked(True)
        self.dBm.setObjectName(_fromUtf8("dBm"))
        self.horizontalLayout_2.addWidget(self.dBm)
        self.W = QtGui.QRadioButton(self.powerUnit)
        self.W.setText(QtGui.QApplication.translate("DpiResult", "W", None, QtGui.QApplication.UnicodeUTF8))
        self.W.setObjectName(_fromUtf8("W"))
        self.horizontalLayout_2.addWidget(self.W)
        self.gridLayout.addWidget(self.powerUnit, 1, 0, 1, 1)
        self.additional = QtGui.QGroupBox(DpiResult)
        self.additional.setTitle(QtGui.QApplication.translate("DpiResult", "Additional data", None, QtGui.QApplication.UnicodeUTF8))
        self.additional.setObjectName(_fromUtf8("additional"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.additional)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.generated = QtGui.QCheckBox(self.additional)
        self.generated.setText(QtGui.QApplication.translate("DpiResult", "Generator power", None, QtGui.QApplication.UnicodeUTF8))
        self.generated.setChecked(False)
        self.generated.setObjectName(_fromUtf8("generated"))
        self.horizontalLayout.addWidget(self.generated)
        self.s11 = QtGui.QCheckBox(self.additional)
        self.s11.setText(QtGui.QApplication.translate("DpiResult", "|S11|", None, QtGui.QApplication.UnicodeUTF8))
        self.s11.setObjectName(_fromUtf8("s11"))
        self.horizontalLayout.addWidget(self.s11)
        self.forwardReflected = QtGui.QCheckBox(self.additional)
        self.forwardReflected.setText(QtGui.QApplication.translate("DpiResult", "Forward and reflected", None, QtGui.QApplication.UnicodeUTF8))
        self.forwardReflected.setObjectName(_fromUtf8("forwardReflected"))
        self.horizontalLayout.addWidget(self.forwardReflected)
        self.passFail = QtGui.QCheckBox(self.additional)
        self.passFail.setText(QtGui.QApplication.translate("DpiResult", "Pass/fail points", None, QtGui.QApplication.UnicodeUTF8))
        self.passFail.setObjectName(_fromUtf8("passFail"))
        self.horizontalLayout.addWidget(self.passFail)
        self.gridLayout.addWidget(self.additional, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(229, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)

        self.retranslateUi(DpiResult)
        QtCore.QMetaObject.connectSlotsByName(DpiResult)

    def retranslateUi(self, DpiResult):
        pass

from matplotlibwidget import MatplotlibWidget

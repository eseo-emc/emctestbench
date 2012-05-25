# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nearfieldscanresult_view.ui'
#
# Created: Fri May 25 11:23:06 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NearFieldScanResult(object):
    def setupUi(self, NearFieldScanResult):
        NearFieldScanResult.setObjectName(_fromUtf8("NearFieldScanResult"))
        NearFieldScanResult.resize(729, 377)
        NearFieldScanResult.setWindowTitle(QtGui.QApplication.translate("NearFieldScanResult", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(NearFieldScanResult)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graph = MatplotlibWidget(NearFieldScanResult)
        self.graph.setObjectName(_fromUtf8("graph"))
        self.gridLayout.addWidget(self.graph, 0, 0, 1, 3)
        self.additional = QtGui.QGroupBox(NearFieldScanResult)
        self.additional.setTitle(QtGui.QApplication.translate("NearFieldScanResult", "Additional data", None, QtGui.QApplication.UnicodeUTF8))
        self.additional.setObjectName(_fromUtf8("additional"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.additional)
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.transmittedPower = QtGui.QCheckBox(self.additional)
        self.transmittedPower.setText(QtGui.QApplication.translate("NearFieldScanResult", "Transmitted power", None, QtGui.QApplication.UnicodeUTF8))
        self.transmittedPower.setChecked(False)
        self.transmittedPower.setObjectName(_fromUtf8("transmittedPower"))
        self.horizontalLayout.addWidget(self.transmittedPower)
        self.gridLayout.addWidget(self.additional, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(229, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.powerUnit = QtGui.QGroupBox(NearFieldScanResult)
        self.powerUnit.setTitle(QtGui.QApplication.translate("NearFieldScanResult", "Power unit", None, QtGui.QApplication.UnicodeUTF8))
        self.powerUnit.setFlat(False)
        self.powerUnit.setObjectName(_fromUtf8("powerUnit"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.powerUnit)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setMargin(3)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.dBm = QtGui.QRadioButton(self.powerUnit)
        self.dBm.setText(QtGui.QApplication.translate("NearFieldScanResult", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.dBm.setChecked(True)
        self.dBm.setObjectName(_fromUtf8("dBm"))
        self.horizontalLayout_2.addWidget(self.dBm)
        self.W = QtGui.QRadioButton(self.powerUnit)
        self.W.setText(QtGui.QApplication.translate("NearFieldScanResult", "W", None, QtGui.QApplication.UnicodeUTF8))
        self.W.setObjectName(_fromUtf8("W"))
        self.horizontalLayout_2.addWidget(self.W)
        self.gridLayout.addWidget(self.powerUnit, 1, 0, 1, 1)

        self.retranslateUi(NearFieldScanResult)
        QtCore.QMetaObject.connectSlotsByName(NearFieldScanResult)

    def retranslateUi(self, NearFieldScanResult):
        pass

from matplotlibwidget import MatplotlibWidget

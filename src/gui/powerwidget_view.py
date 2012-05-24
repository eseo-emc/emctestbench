# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerwidget_view.ui'
#
# Created: Wed May 16 14:33:55 2012
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
        Form.resize(209, 20)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.value = QtGui.QDoubleSpinBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value.sizePolicy().hasHeightForWidth())
        self.value.setSizePolicy(sizePolicy)
        self.value.setDecimals(1)
        self.value.setSingleStep(0.1)
        self.value.setObjectName(_fromUtf8("value"))
        self.horizontalLayout.addWidget(self.value)
        self.unit = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unit.sizePolicy().hasHeightForWidth())
        self.unit.setSizePolicy(sizePolicy)
        self.unit.setObjectName(_fromUtf8("unit"))
        self.unit.addItem(_fromUtf8(""))
        self.unit.setItemText(0, QtGui.QApplication.translate("Form", "dBm", None, QtGui.QApplication.UnicodeUTF8))
        self.unit.addItem(_fromUtf8(""))
        self.unit.setItemText(1, QtGui.QApplication.translate("Form", "W", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout.addWidget(self.unit)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass


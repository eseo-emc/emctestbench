# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'receivedpower_view.ui'
#
# Created: Fri Jun 01 20:18:30 2012
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
        Form.resize(481, 69)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(6)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Span:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.span = QuantityWidgetController(Form)
        self.span.setObjectName(_fromUtf8("span"))
        self.gridLayout.addWidget(self.span, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(216, 54, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 2, 1)
        self.measure = QtGui.QPushButton(Form)
        self.measure.setText(QtGui.QApplication.translate("Form", "Measure", None, QtGui.QApplication.UnicodeUTF8))
        self.measure.setObjectName(_fromUtf8("measure"))
        self.gridLayout.addWidget(self.measure, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Averaging points:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.numberOfAveragingPoints = QtGui.QSpinBox(Form)
        self.numberOfAveragingPoints.setMinimum(1)
        self.numberOfAveragingPoints.setMaximum(1000000000)
        self.numberOfAveragingPoints.setObjectName(_fromUtf8("numberOfAveragingPoints"))
        self.gridLayout.addWidget(self.numberOfAveragingPoints, 1, 1, 1, 1)
        self.receivedPower = PowerWidgetController(Form)
        self.receivedPower.setReadOnly(True)
        self.receivedPower.setObjectName(_fromUtf8("receivedPower"))
        self.gridLayout.addWidget(self.receivedPower, 1, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from gui.quantitywidget_controller import QuantityWidgetController
from gui.powerwidget_controller import PowerWidgetController

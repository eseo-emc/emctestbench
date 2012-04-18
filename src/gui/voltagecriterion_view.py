# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'voltagecriterion_view.ui'
#
# Created: Tue Apr 17 17:40:29 2012
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
        Form.resize(640, 80)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setMargin(3)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(Form)
        self.label_4.setText(QtGui.QApplication.translate("Form", "Nominal Voltage:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.nominalVoltage = QtGui.QDoubleSpinBox(Form)
        self.nominalVoltage.setDecimals(3)
        self.nominalVoltage.setMinimum(-99.99)
        self.nominalVoltage.setObjectName(_fromUtf8("nominalVoltage"))
        self.gridLayout.addWidget(self.nominalVoltage, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setText(QtGui.QApplication.translate("Form", "V", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.measureNominal = QtGui.QPushButton(Form)
        self.measureNominal.setText(QtGui.QApplication.translate("Form", "Measure", None, QtGui.QApplication.UnicodeUTF8))
        self.measureNominal.setObjectName(_fromUtf8("measureNominal"))
        self.gridLayout.addWidget(self.measureNominal, 0, 4, 1, 1)
        spacerItem = QtGui.QSpacerItem(200, 58, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 5, 3, 1)
        self.widget = PassFailWidget(Form)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout.addWidget(self.widget, 0, 6, 3, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Voltage Margin:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setText(QtGui.QApplication.translate("Form", "±", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 1, 1, 1)
        self.voltageMargin = QtGui.QDoubleSpinBox(Form)
        self.voltageMargin.setDecimals(3)
        self.voltageMargin.setMinimum(-99.99)
        self.voltageMargin.setObjectName(_fromUtf8("voltageMargin"))
        self.gridLayout.addWidget(self.voltageMargin, 1, 2, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "V", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 3, 1, 1)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setText(QtGui.QApplication.translate("Form", "Voltage:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.measuredVoltage = QtGui.QLineEdit(Form)
        self.measuredVoltage.setText(_fromUtf8(""))
        self.measuredVoltage.setReadOnly(True)
        self.measuredVoltage.setObjectName(_fromUtf8("measuredVoltage"))
        self.gridLayout.addWidget(self.measuredVoltage, 2, 2, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        self.label_5.setText(QtGui.QApplication.translate("Form", "V", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 3, 1, 1)
        self.measure = QtGui.QPushButton(Form)
        self.measure.setText(QtGui.QApplication.translate("Form", "Measure", None, QtGui.QApplication.UnicodeUTF8))
        self.measure.setObjectName(_fromUtf8("measure"))
        self.gridLayout.addWidget(self.measure, 2, 4, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from gui.passfailwidget import PassFailWidget
import icons_rc
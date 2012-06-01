# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nearfieldscan_view.ui'
#
# Created: Fri Jun 01 20:47:05 2012
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
        Form.resize(651, 442)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(3)
        self.gridLayout.setSpacing(3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText(QtGui.QApplication.translate("Form", "x", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setText(QtGui.QApplication.translate("Form", "y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 2, 1, 1)
        self.label_5 = QtGui.QLabel(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setText(QtGui.QApplication.translate("Form", "z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 3, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setText(QtGui.QApplication.translate("Form", "Start position:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 4, 0, 1, 1)
        self.yStart = QuantityWidgetController(Form)
        self.yStart.setObjectName(_fromUtf8("yStart"))
        self.gridLayout.addWidget(self.yStart, 4, 2, 1, 1)
        self.readStartPosition = QtGui.QPushButton(Form)
        self.readStartPosition.setEnabled(True)
        self.readStartPosition.setText(QtGui.QApplication.translate("Form", "Read current position", None, QtGui.QApplication.UnicodeUTF8))
        self.readStartPosition.setFlat(False)
        self.readStartPosition.setObjectName(_fromUtf8("readStartPosition"))
        self.gridLayout.addWidget(self.readStartPosition, 4, 4, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setText(QtGui.QApplication.translate("Form", "Stop position:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)
        self.yStop = QuantityWidgetController(Form)
        self.yStop.setObjectName(_fromUtf8("yStop"))
        self.gridLayout.addWidget(self.yStop, 5, 2, 1, 1)
        self.readStopPosition = QtGui.QPushButton(Form)
        self.readStopPosition.setEnabled(True)
        self.readStopPosition.setText(QtGui.QApplication.translate("Form", "Read current position", None, QtGui.QApplication.UnicodeUTF8))
        self.readStopPosition.setFlat(False)
        self.readStopPosition.setObjectName(_fromUtf8("readStopPosition"))
        self.gridLayout.addWidget(self.readStopPosition, 5, 4, 1, 1)
        self.label_6 = QtGui.QLabel(Form)
        self.label_6.setText(QtGui.QApplication.translate("Form", "Number of steps:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 6, 0, 1, 1)
        self.numberOfSteps = QtGui.QSpinBox(Form)
        self.numberOfSteps.setObjectName(_fromUtf8("numberOfSteps"))
        self.gridLayout.addWidget(self.numberOfSteps, 6, 1, 1, 1)
        self.rehearsePath = QtGui.QPushButton(Form)
        self.rehearsePath.setText(QtGui.QApplication.translate("Form", "Rehearse path", None, QtGui.QApplication.UnicodeUTF8))
        self.rehearsePath.setObjectName(_fromUtf8("rehearsePath"))
        self.gridLayout.addWidget(self.rehearsePath, 6, 4, 1, 1)
        self.label_7 = QtGui.QLabel(Form)
        self.label_7.setText(QtGui.QApplication.translate("Form", "Generator power:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 8, 0, 1, 1)
        self.generatorPower = PowerWidgetController(Form)
        self.generatorPower.setObjectName(_fromUtf8("generatorPower"))
        self.gridLayout.addWidget(self.generatorPower, 8, 1, 1, 1)
        self.label_8 = QtGui.QLabel(Form)
        self.label_8.setText(QtGui.QApplication.translate("Form", "Generator frequency:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 9, 0, 1, 1)
        self.generatorFrequency = QuantityWidgetController(Form)
        self.generatorFrequency.setObjectName(_fromUtf8("generatorFrequency"))
        self.gridLayout.addWidget(self.generatorFrequency, 9, 1, 1, 1)
        self.transmittedPower = DropWidget(Form)
        self.transmittedPower.setObjectName(_fromUtf8("transmittedPower"))
        self.gridLayout.addWidget(self.transmittedPower, 10, 0, 1, 5)
        self.measurement = DropWidget(Form)
        self.measurement.setObjectName(_fromUtf8("measurement"))
        self.gridLayout.addWidget(self.measurement, 11, 0, 1, 5)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 7, 0, 1, 5)
        self.xStart = QuantityWidgetController(Form)
        self.xStart.setEnabled(True)
        self.xStart.setObjectName(_fromUtf8("xStart"))
        self.gridLayout.addWidget(self.xStart, 4, 1, 1, 1)
        self.xStop = QtGui.QDoubleSpinBox(Form)
        self.xStop.setEnabled(False)
        self.xStop.setObjectName(_fromUtf8("xStop"))
        self.gridLayout.addWidget(self.xStop, 5, 1, 1, 1)
        self.zStart = QuantityWidgetController(Form)
        self.zStart.setEnabled(True)
        self.zStart.setObjectName(_fromUtf8("zStart"))
        self.gridLayout.addWidget(self.zStart, 4, 3, 1, 1)
        self.zStop = QtGui.QDoubleSpinBox(Form)
        self.zStop.setEnabled(False)
        self.zStop.setObjectName(_fromUtf8("zStop"))
        self.gridLayout.addWidget(self.zStop, 5, 3, 1, 1)
        self.line_2 = QtGui.QFrame(Form)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 2, 0, 1, 5)
        self.startStop = QtGui.QPushButton(Form)
        self.startStop.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.startStop.setObjectName(_fromUtf8("startStop"))
        self.gridLayout.addWidget(self.startStop, 0, 4, 1, 1)
        self.progress = QtGui.QProgressBar(Form)
        self.progress.setProperty("value", 0)
        self.progress.setObjectName(_fromUtf8("progress"))
        self.gridLayout.addWidget(self.progress, 0, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

from gui.dropwidget_controller import DropWidget
from gui.quantitywidget_controller import QuantityWidgetController
from gui.powerwidget_controller import PowerWidgetController

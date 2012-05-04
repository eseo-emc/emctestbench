# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scalarresult_view.ui'
#
# Created: Mon Apr 23 14:06:43 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ScalarResult(object):
    def setupUi(self, ScalarResult):
        ScalarResult.setObjectName(_fromUtf8("ScalarResult"))
        ScalarResult.resize(320, 240)
        ScalarResult.setWindowTitle(QtGui.QApplication.translate("ScalarResult", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(ScalarResult)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.textView = QtGui.QLabel(ScalarResult)
        self.textView.setText(QtGui.QApplication.translate("ScalarResult", "No result", None, QtGui.QApplication.UnicodeUTF8))
        self.textView.setAlignment(QtCore.Qt.AlignCenter)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.horizontalLayout.addWidget(self.textView)

        self.retranslateUi(ScalarResult)
        QtCore.QMetaObject.connectSlotsByName(ScalarResult)

    def retranslateUi(self, ScalarResult):
        pass


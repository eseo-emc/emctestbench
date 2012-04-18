# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'passfailwidget_view.ui'
#
# Created: Tue Apr 17 15:29:07 2012
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
        Form.resize(357, 208)
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.button = QtGui.QPushButton(Form)
        self.button.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/logging/Unknown.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button.setIcon(icon)
        self.button.setIconSize(QtCore.QSize(32, 32))
        self.button.setFlat(True)
        self.button.setObjectName(_fromUtf8("button"))
        self.gridLayout.addWidget(self.button, 0, 0, 1, 1)
        self.text = QtGui.QLabel(Form)
        self.text.setText(QtGui.QApplication.translate("Form", "Unknown", None, QtGui.QApplication.UnicodeUTF8))
        self.text.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.text.setObjectName(_fromUtf8("text"))
        self.gridLayout.addWidget(self.text, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        pass

import icons_rc

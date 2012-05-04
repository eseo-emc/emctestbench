# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dictresult_view.ui'
#
# Created: Thu Apr 26 10:02:08 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DictResult(object):
    def setupUi(self, DictResult):
        DictResult.setObjectName(_fromUtf8("DictResult"))
        DictResult.resize(320, 240)
        DictResult.setWindowTitle(QtGui.QApplication.translate("DictResult", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(DictResult)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtGui.QTableWidget(DictResult)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(2)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "Nouvelle ligne", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "Nouvelle ligne", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "Quantity", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        item.setText(QtGui.QApplication.translate("DictResult", "2", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setItem(1, 0, item)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(17)
        self.tableWidget.verticalHeader().setHighlightSections(True)
        self.horizontalLayout.addWidget(self.tableWidget)

        self.retranslateUi(DictResult)
        QtCore.QMetaObject.connectSlotsByName(DictResult)

    def retranslateUi(self, DictResult):
        item = self.tableWidget.verticalHeaderItem(0)
        item = self.tableWidget.verticalHeaderItem(1)
        item = self.tableWidget.horizontalHeaderItem(0)
        item = self.tableWidget.horizontalHeaderItem(1)
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item = self.tableWidget.item(1, 0)
        self.tableWidget.setSortingEnabled(__sortingEnabled)


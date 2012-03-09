import sys
from PyQt4 import QtGui, uic

application = QtGui.QApplication(sys.argv)
QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Cleanlooks"))
widget = uic.loadUi("djangotextwriter.ui")
widget.show()

application.exec_()
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'applicationwindow_view.ui'
#
# Created: Mon Mar 26 13:41:41 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_ApplicationWindow(object):
    def setupUi(self, ApplicationWindow):
        ApplicationWindow.setObjectName(_fromUtf8("ApplicationWindow"))
        ApplicationWindow.resize(1024, 768)
        ApplicationWindow.setWindowTitle(QtGui.QApplication.translate("ApplicationWindow", "EMC Testbench", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(ApplicationWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.systemTree = QtGui.QTreeView(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.systemTree.setFont(font)
        self.systemTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.systemTree.setIconSize(QtCore.QSize(18, 18))
        self.systemTree.setObjectName(_fromUtf8("systemTree"))
        self.systemTree.header().setVisible(False)
        self.systemTree.header().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.systemTree)
        self.refreshButton = QtGui.QPushButton(self.layoutWidget)
        self.refreshButton.setText(QtGui.QApplication.translate("ApplicationWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setObjectName(_fromUtf8("refreshButton"))
        self.verticalLayout.addWidget(self.refreshButton)
        self.inspector = QtGui.QFrame(self.splitter)
        self.inspector.setFrameShape(QtGui.QFrame.StyledPanel)
        self.inspector.setFrameShadow(QtGui.QFrame.Raised)
        self.inspector.setObjectName(_fromUtf8("inspector"))
        self.pushButton = QtGui.QPushButton(self.inspector)
        self.pushButton.setGeometry(QtCore.QRect(54, 200, 91, 31))
        self.pushButton.setText(QtGui.QApplication.translate("ApplicationWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/Amplifier.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        ApplicationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ApplicationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setTitle(QtGui.QApplication.translate("ApplicationWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setTitle(QtGui.QApplication.translate("ApplicationWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        ApplicationWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ApplicationWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ApplicationWindow.setStatusBar(self.statusbar)
        self.action_Quit = QtGui.QAction(ApplicationWindow)
        self.action_Quit.setText(QtGui.QApplication.translate("ApplicationWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("ApplicationWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_About = QtGui.QAction(ApplicationWindow)
        self.action_About.setText(QtGui.QApplication.translate("ApplicationWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.menuFile.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(ApplicationWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), ApplicationWindow.close)
        QtCore.QMetaObject.connectSlotsByName(ApplicationWindow)

    def retranslateUi(self, ApplicationWindow):
        pass

import icons_rc

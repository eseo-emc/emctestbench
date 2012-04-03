# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'applicationwindow_view.ui'
#
# Created: Tue Apr 03 10:38:03 2012
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
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName(_fromUtf8("splitter_2"))
        self.layoutWidget = QtGui.QWidget(self.splitter_2)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.systemTree = SystemTreeWidget(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.systemTree.setFont(font)
        self.systemTree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.systemTree.setIconSize(QtCore.QSize(18, 18))
        self.systemTree.setColumnCount(1)
        self.systemTree.setObjectName(_fromUtf8("systemTree"))
        self.systemTree.headerItem().setText(0, _fromUtf8("1"))
        self.systemTree.header().setVisible(False)
        self.systemTree.header().setMinimumSectionSize(1)
        self.verticalLayout.addWidget(self.systemTree)
        self.splitter = QtGui.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.inspector = QtGui.QWidget(self.splitter)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inspector.sizePolicy().hasHeightForWidth())
        self.inspector.setSizePolicy(sizePolicy)
        self.inspector.setMinimumSize(QtCore.QSize(640, 480))
        self.inspector.setObjectName(_fromUtf8("inspector"))
        self.logView = LogWidget(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.logView.setFont(font)
        self.logView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.logView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.logView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.logView.setIconSize(QtCore.QSize(18, 18))
        self.logView.setShowGrid(False)
        self.logView.setCornerButtonEnabled(False)
        self.logView.setColumnCount(3)
        self.logView.setObjectName(_fromUtf8("logView"))
        self.logView.setRowCount(0)
        self.logView.horizontalHeader().setCascadingSectionResizes(False)
        self.logView.horizontalHeader().setMinimumSectionSize(1)
        self.logView.horizontalHeader().setSortIndicatorShown(False)
        self.logView.horizontalHeader().setStretchLastSection(True)
        self.logView.verticalHeader().setVisible(False)
        self.logView.verticalHeader().setCascadingSectionResizes(False)
        self.logView.verticalHeader().setDefaultSectionSize(17)
        self.horizontalLayout.addWidget(self.splitter_2)
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
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setTitle(QtGui.QApplication.translate("ApplicationWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuLogging_Level = QtGui.QMenu(self.menuView)
        self.menuLogging_Level.setTitle(QtGui.QApplication.translate("ApplicationWindow", "Logging Level", None, QtGui.QApplication.UnicodeUTF8))
        self.menuLogging_Level.setObjectName(_fromUtf8("menuLogging_Level"))
        ApplicationWindow.setMenuBar(self.menubar)
        self.action_Quit = QtGui.QAction(ApplicationWindow)
        self.action_Quit.setText(QtGui.QApplication.translate("ApplicationWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("ApplicationWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setObjectName(_fromUtf8("action_Quit"))
        self.action_About = QtGui.QAction(ApplicationWindow)
        self.action_About.setText(QtGui.QApplication.translate("ApplicationWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setObjectName(_fromUtf8("action_About"))
        self.actionErrors_only = QtGui.QAction(ApplicationWindow)
        self.actionErrors_only.setText(QtGui.QApplication.translate("ApplicationWindow", "Errors only", None, QtGui.QApplication.UnicodeUTF8))
        self.actionErrors_only.setObjectName(_fromUtf8("actionErrors_only"))
        self.actionInfo = QtGui.QAction(ApplicationWindow)
        self.actionInfo.setText(QtGui.QApplication.translate("ApplicationWindow", "Info", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInfo.setObjectName(_fromUtf8("actionInfo"))
        self.actionDebug = QtGui.QAction(ApplicationWindow)
        self.actionDebug.setText(QtGui.QApplication.translate("ApplicationWindow", "Debug", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDebug.setObjectName(_fromUtf8("actionDebug"))
        self.menuFile.addAction(self.action_Quit)
        self.menu_Help.addAction(self.action_About)
        self.menuLogging_Level.addAction(self.actionErrors_only)
        self.menuLogging_Level.addAction(self.actionInfo)
        self.menuLogging_Level.addAction(self.actionDebug)
        self.menuView.addAction(self.menuLogging_Level.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(ApplicationWindow)
        QtCore.QObject.connect(self.action_Quit, QtCore.SIGNAL(_fromUtf8("triggered()")), ApplicationWindow.close)
        QtCore.QMetaObject.connectSlotsByName(ApplicationWindow)

    def retranslateUi(self, ApplicationWindow):
        pass

from gui.logwidget import LogWidget
from gui.systemtreewidget import SystemTreeWidget
import icons_rc

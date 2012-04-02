# MEMO
# To compile the UI:
#    pyuic4 -o applicationwindow_view.py applicationwindow_view.ui   
# To compile the resources:
#    pyrcc4 -o icons_rc.py icons\icons.qrc
from PyQt4.QtGui import QMainWindow, QMessageBox
from gui.applicationwindow_view import Ui_ApplicationWindow
from gui.applicationwindow_model import ApplicationWindowModel
from gui import logging
from gui import logwidget

class ApplicationWindowController(QMainWindow,Ui_ApplicationWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.action_About.triggered.connect(self.about)
        
        self.model = ApplicationWindowModel()
        
        self.refreshButton.clicked.connect(self.model.refresh)        

        logging.LogItem("EMC Testbench started",logging.info)
        self.actionErrors_only.triggered.connect(lambda : self.logView.setLevel(logging.warning))
        self.actionInfo.triggered.connect(lambda : self.logView.setLevel(logging.info))
        self.actionDebug.triggered.connect(lambda : self.logView.setLevel(logging.debug))
        
    def aboutToQuit(self):
        logging.LogItem('Bye!')
    def about(self):
        progname = 'EMC Testbench'
        progversion = 0.1
        
        QMessageBox.about(self, "About %s" % progname,
u"""%(prog)s version %(version)s
Groupe ESEO, Angers"""
% {"prog": progname, "version": progversion})
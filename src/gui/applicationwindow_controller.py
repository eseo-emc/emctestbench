# MEMO
# To compile the UI:
#    pyuic4 -o applicationwindow_view.py applicationwindow_view.ui   
# To compile the resources:
#    pyrcc4 -o icons_rc.py icons\icons.qrc

from PyQt4.QtGui import QMainWindow, QMessageBox
from gui.applicationwindow_view import Ui_ApplicationWindow
from gui.applicationwindow_model import ApplicationWindowModel

class ApplicationWindowController(QMainWindow,Ui_ApplicationWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.action_About.triggered.connect(self.about)
        
        def showError(message):
            self.statusBar().showMessage(message,2000)
        self.model = ApplicationWindowModel(showError)
        
        self.systemTree.setModel(self.model.systemTreeModel)
        self.refreshButton.clicked.connect(self.model.refresh)        
        
        self.statusBar().showMessage("EMC Testbench started", 2000)

        
    def aboutToQuit(self):
        self.statusBar().showMessage('Bye!')
    def about(self):
        progname = 'EMC Testbench'
        progversion = 0.1
        
        QMessageBox.about(self, "About %s" % progname,
u"""%(prog)s version %(version)s
Groupe ESEO, Angers"""
% {"prog": progname, "version": progversion})
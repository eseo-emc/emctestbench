import sys

from PyQt4.QtGui import QMainWindow, QMessageBox,QDockWidget
from PyQt4.QtCore import Qt
from gui.mockup_view import Ui_MainWindow
#from gui.applicationwindow_model import ApplicationWindowModel
from gui import logging

class MockupController(QMainWindow,Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.showFullScreen()
        
        self.setCorner(Qt.BottomRightCorner,Qt.RightDockWidgetArea)
        
        self.actionAbout.triggered.connect(self.about)
        self.actionTree_Left.triggered.connect(self.placeTreeLeft)
        self.actionTree_on_Top.triggered.connect(self.placeTreeOnTop)
        self.placeTreeLeft()
        
    def placeTreeLeft(self):
        for child in self.children():
            if isinstance(child,QDockWidget) and child not in [self.metadataViewer]:
    
                child.setAllowedAreas(Qt.RightDockWidgetArea)
                self.removeDockWidget(child)
        self.metadataViewer.setAllowedAreas(Qt.BottomDockWidgetArea)
        self.removeDockWidget(self.metadataViewer)
        
        self.addDockWidget(Qt.BottomDockWidgetArea,self.metadataViewer)
#        self.metadataViewer.show()
        self.addDockWidget(Qt.RightDockWidgetArea,self.experimentViewer)
        self.splitDockWidget(self.experimentViewer,self.logWindow,Qt.Vertical)
#        
        for child in self.children():
            if isinstance(child,QDockWidget):
                if child not in [self.experimentViewer,self.logWindow,self.metadataViewer]:
                    self.tabifyDockWidget(self.logWindow,child)
                child.show()
        
    def placeTreeOnTop(self):
        for child in self.children():
            if isinstance(child,QDockWidget):
                child.setAllowedAreas(Qt.BottomDockWidgetArea)
                self.removeDockWidget(child)
                
        self.addDockWidget(Qt.BottomDockWidgetArea,self.logWindow)
        
        for child in self.children():
            if isinstance(child,QDockWidget):
                if child not in [self.logWindow]:
                    self.tabifyDockWidget(self.logWindow,child)
                child.show()
           
        
    def aboutToQuit(self):
        logging.LogItem('Bye!')
    def about(self):
        progname = 'EMC Testbench'
        progversion = 0.1
        
        QMessageBox.about(self, "About %s" % progname,
u"""%(prog)s version %(version)s
Groupe ESEO, Angers"""
% {"prog": progname, "version": progversion})

if __name__ == '__main__':
    import sys
    from PyQt4.QtGui import QApplication
#    from gui.applicationwindow_controller import ApplicationWindowController
    
    application = QApplication(sys.argv)
    window = MockupController()
    window.show()
    sys.exit(application.exec_())
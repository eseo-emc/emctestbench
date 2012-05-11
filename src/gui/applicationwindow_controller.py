# MEMO
# To compile the UI:
#    pyuic4 applicationwindow_view.ui > applicationwindow_view.py
# To compile the resources:
#    pyrcc4 icons\icons.qrc > icons_rc.py
import sys

from PyQt4.QtGui import QMainWindow, QMessageBox,QDockWidget
from PyQt4.QtCore import Qt
from gui.applicationwindow_view import Ui_ApplicationWindow
from gui.applicationwindow_model import ApplicationWindowModel
from gui import logging
from experiment.experiment import ExperimentSlot

import string

class ApplicationWindowController(QMainWindow,Ui_ApplicationWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)     
        
        self.topLevelExperiment = ExperimentSlot()
        self.mainDropWidget.model = self.topLevelExperiment
        self.mainDropWidget.topLevel = True
        
        self.showFullScreen()
        self.setCorner(Qt.BottomRightCorner,Qt.RightDockWidgetArea)
        
        self.action_About.triggered.connect(self.about)
        
        self.experimentResultTree.update()
        self.experimentResultTree.experimentResultSelected.connect(self.experimentResultSelected)
        self.experimentResultTree.changed.connect(self.showExperimentResultTree)
        
        
        self.model = ApplicationWindowModel()
        self.experimentTree.experimentSelected.connect(self.experimentSelected)

        logging.LogItem("EMC Testbench started",logging.info)
        self.actionErrors_only.triggered.connect(lambda : self.logView.setLevel(logging.warning))
        self.actionInfo.triggered.connect(lambda : self.logView.setLevel(logging.info))
        self.actionDebug.triggered.connect(lambda : self.logView.setLevel(logging.debug))
        
        self.actionTree_left.triggered.connect(self.placeTreeLeft)
        self.actionTree_on_top.triggered.connect(self.placeTreeOnTop)
        self.placeTreeLeft()
        
        
        
    def placeTreeLeft(self):
        for child in self.children():
            if isinstance(child,QDockWidget) and child not in []: #self.metadataViewer]:
                child.setAllowedAreas(Qt.RightDockWidgetArea)
                self.removeDockWidget(child)
#        self.metadataViewer.setAllowedAreas(Qt.BottomDockWidgetArea)
#        self.removeDockWidget(self.metadataViewer)
        
#        self.addDockWidget(Qt.BottomDockWidgetArea,self.metadataViewer)
##        self.metadataViewer.show()
        self.addDockWidget(Qt.RightDockWidgetArea,self.experimentViewer)
        self.splitDockWidget(self.experimentViewer,self.logWindow,Qt.Vertical)
#        
        for child in self.children():
            if isinstance(child,QDockWidget):
                if child not in [self.experimentViewer,self.logWindow]: #,self.metadataViewer]:
                    self.tabifyDockWidget(self.logWindow,child)
                child.show()
                
        self.mainTabWidget.setCurrentIndex(1)
        
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
                
        self.mainTabWidget.setCurrentIndex(0)
        
    def experimentSelected(self,experimentName):
        self.topLevelExperiment.value = experimentName.__name__
    def experimentResultSelected(self,experimentResult):
        if hasattr(self,'activeResultController'):
            self.activeResultController.deleteLater()
            del(self.activeResultController)
        
        resultType = experimentResult.result.__class__.__name__
#        try:
        
        exec('''
from {moduleName} import {controllerName}
self.activeResultController = {controllerName}(self.resultViewerWidget)
self.resultVerticalLayout.addWidget(self.activeResultController)
'''.format(moduleName=string.lower(resultType)+'_controller',controllerName=resultType+'Controller'))
        self.activeResultController.model = experimentResult.result
        self.resultViewer.raise_()
#        except:
#            logging.LogItem(sys.exc_info()[1],logging.error)         
    
    def showExperimentResultTree(self):
        self.mainTabWidget.setCurrentIndex(0)
    
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
    window = ApplicationWindowController()
    window.show()
    sys.exit(application.exec_())
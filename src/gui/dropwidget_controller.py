from PyQt4.QtGui import QWidget,QFont
from gui.dropwidget_view import Ui_Form

import logging
import sys
import string

class DropWidget(QWidget,Ui_Form):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        
        self._label = 'Experiment'
        self._updateLabel()
        
    def _updateLabel(self):
        font = self.experimentName.font()
        if hasattr(self,'activeExperimentController'):
            self.experimentName.setText(self._label+': '+self.activeExperimentController.model.name)
#            self.experimentNameSideways.setText(self.activeExperimentController.model.name)
            font.setItalic(False)
        else:
            self.experimentName.setText('Drop '+self._label+' here')
#            self.experimentNameSideways.setText('')
            font.setItalic(True)
        self.experimentName.setFont(font)
   
    @property
    def label(self):
        return self._label
    @label.setter
    def label(self,newLabel):
        self._label = newLabel
        self._updateLabel()
        
    def dragEnterEvent(self,dragEvent):
        dragEvent.acceptProposedAction()
        
    def dropEvent(self,dropEvent):
        experimentName = str(dropEvent.mimeData().text())
        self.selectExperiment(experimentName)
        
    def selectExperiment(self,experimentName):        
        if hasattr(self,'activeExperimentController'):
            self.activeExperimentController.deleteLater()
            del(self.activeExperimentController)

        try:
            exec('''
from {moduleName} import {controllerName}
self.activeExperimentController = {controllerName}(self)
self.gridLayout.addWidget(self.activeExperimentController,1,1)'''.format(moduleName=string.lower(experimentName)+'_controller',controllerName=experimentName+'Controller'))
        except:
            logging.LogItem(sys.exc_info()[1],logging.error)
            
        self._updateLabel()

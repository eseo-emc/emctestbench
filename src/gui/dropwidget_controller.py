from PyQt4.QtGui import QWidget
from PyQt4.QtCore import Qt
from gui.dropwidget_view import Ui_Form

import logging
import sys
import string

class DropWidget(QWidget,Ui_Form):
    def __init__(self,parent,topLevel=False):
        QWidget.__init__(self,parent)
        self.setupUi(self)
        self.topLevel = topLevel
        
        self._model = None
        
        self._label = 'Experiment'
        self._updateLabel()
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        if self._model:
            self._model.changedTo.disconnect()
        self._model = value
        self.loadController(self._model.value)
        self._model.changedTo.connect(self.loadController)
        
    def _updateLabel(self):
        font = self.experimentName.font()
        
        if self.model and self.model.value:
            self.experimentName.setText(self._label+': '+self.model.value.name)
#            self.experimentNameSideways.setText(self.activeExperimentController.model.name)
            font.setItalic(False)
            self.experimentName.setAlignment(Qt.AlignLeft|Qt.AlignTop)            
        else:
            self.experimentName.setText('Drop '+self._label+' here')
#            self.experimentNameSideways.setText('')
            font.setItalic(True)
            self.experimentName.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
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
        self.model.value = experimentName

#        self.selectExperiment(experimentName)
        
        
    def loadController(self,experiment):        
        if hasattr(self,'activeExperimentController'):
            self.activeExperimentController.deleteLater()
            del(self.activeExperimentController)

        if experiment:
            experimentName = experiment.__class__.__name__
    #        try:
            exec('''
from {moduleName} import {controllerName}
self.activeExperimentController = {controllerName}(self.frame,topLevel={topLevel})
self.verticalLayout_2.addWidget(self.activeExperimentController)'''.format(moduleName=string.lower(experimentName)+'_controller',controllerName=experimentName+'Controller',topLevel=self.topLevel))
    #        except:
    #            logging.LogItem(sys.exc_info()[1],logging.error)
            self.activeExperimentController.model = experiment
        self._updateLabel()

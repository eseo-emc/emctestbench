from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from device import knownDevices,Device

from PyQt4.QtGui import QApplication

import logging
import inspect

from copy import deepcopy

from datetime import datetime


class ExperimentResult(QObject):
    changed = pyqtSignal()    
    changedTo = pyqtSignal(object)    
    
    def __init__(self,experiment,result,save=True):
        QObject.__init__(self)
        
        self.experiment = deepcopy(experiment)
        self.result = result
        creationDate = datetime.now()
        self.metadata = {'Name':self.experiment.name + creationDate.strftime(' %Y%m%d-%H%M%S'),'DUT':'','Operator':'','Creation':creationDate}
        
        if save:
            ExperimentResultCollection.Instance().append(self)
        

@Singleton
class ExperimentResultCollection(QObject):
    changed = pyqtSignal()   
    extendedWith = pyqtSignal(object)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.experimentResults = []   
    def __getitem__(self,key):
        return self.experimentResults[key]
    def readFromFileSystem(self):
        pass
    def append(self,newExperimentResult):
        self.experimentResults.append(newExperimentResult)
        self.extendedWith.emit(newExperimentResult)
        self.changed.emit()
        
if __name__ == '__main__':
    class DummyExperiment:
        name = 'DummyExperiment'
    dummyExperiment = DummyExperiment()
    print dummyExperiment
    ExperimentResult(dummyExperiment,3)
    print ExperimentResultCollection.Instance().results[0].experiment
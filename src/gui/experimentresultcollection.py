from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from device import knownDevices,Device

from PyQt4.QtGui import QApplication
from result.persistance import Dommable
from xml.dom.minidom import getDOMImplementation,parseString

import logging
import inspect


from copy import deepcopy

from datetime import datetime


class ExperimentResult(QObject,Dommable):
    changed = pyqtSignal()    
    changedTo = pyqtSignal(object)    
    
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        experimentElement = self.appendChildTag(element,'Experiment')        
        resultElement = self.appendChildTag(element,'Result')
        
        self.castToDommable(self.result).asDom(resultElement)
        return element
    
    def __init__(self,experiment,result,save=True):
        QObject.__init__(self)
        
        self.experiment = deepcopy(experiment)
        self.result = result
        creationDate = datetime.now()
        self.metadata = {'Name':self.experiment.name + creationDate.strftime(' %Y%m%d-%H%M%S'),'DUT':'','Operator':'','Creation':creationDate}
        
        if save:
            ExperimentResultCollection.Instance().append(self)
            self.saveToFileSystem()
            
        self.result.changed.connect(self.saveToFileSystem)
            
    def saveToFileSystem(self):
        print 'Saving'
        fileHandle = open('Y:/emctestbench/results/'+self.metadata['Name']+'.xml','wb')
        document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
        self.asDom(document.documentElement)
        fileHandle.write(document.toxml(encoding='utf-8'))
        fileHandle.close()
        del(fileHandle)
        
        

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
from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from device import knownDevices,Device

from PyQt4.QtGui import QApplication,QDesktopServices
from result.persistance import Dommable
from xml.dom.minidom import getDOMImplementation,parse
from result.persistance import Dict

import logging
import inspect

import glob
import os

from copy import deepcopy

from datetime import datetime

class ExperimentResult(QObject,Dommable):
    changed = pyqtSignal()    
    changedTo = pyqtSignal(object)    
    
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        
        self.appendChildObject(element,self.metadata,'Metadata')
      
        experimentElement = self.appendChildTag(element,'Experiment')   
        experimentElement.setAttribute('id','Experiment')
        
        self.appendChildObject(element,self.result,'Result')
        
        return element

    @classmethod
    def fromDom(cls,dom):
        metadata = cls.childObjectById(dom,'Metadata')
        result = cls.childObjectById(dom,'Result')
        return cls(None,result,save=False,metadata=metadata,name='From anonymous DOM')
    
    def __init__(self,experiment,result,save=True,metadata=None,name=None):
        QObject.__init__(self)
        self.saveCount = 0
        self._name = None
        
        if metadata == None:
            creationDate = datetime.now()
            metadata = Dict({'DUT':'','Operator':'','Creation':creationDate})
        self.metadata = metadata

        if name == None:
            name = experiment.name + creationDate.strftime(' %Y%m%d-%H%M%S')
        self.name = name

        self.experiment = deepcopy(experiment)
        self.result = result
        
        ExperimentResultCollection.Instance().append(self)
#        if save:
#            self.saveToFileSystem()
            
        self.result.changed.connect(self.saveToFileSystem)
        
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self,value):
        self._name = value.replace('\\','').replace('/','').replace(':','')
        self.changed.emit()
        
    @classmethod
    def loadFromFileSystem(cls,fileName):
        fileHandle = open(fileName,'rb')
        document = parse(fileHandle)
        experimentResultElement = document.getElementsByTagName('ExperimentResult')[0]
        newExperimentResult = cls.fromDom(experimentResultElement)
        newExperimentResult.name = os.path.splitext(os.path.split(fileName)[-1])[0]
        return newExperimentResult
        
    def saveToFileSystem(self):
        QApplication.removePostedEvents(self)
        fileHandle = open(ExperimentResultCollection.Instance().resultPath+self.name+ExperimentResultCollection.Instance().resultExtension,'wb')
        document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
        self.asDom(document.documentElement)
        fileHandle.write(document.toxml(encoding='utf-8'))
        fileHandle.close()
#        self.saveCount += 1
#        print self.saveCount
        del(fileHandle)
        
        

@Singleton
class ExperimentResultCollection(QObject):  
    resultExtension = '.xml' 
        
    changed = pyqtSignal()   
    extendedWith = pyqtSignal(object)
    
    
    def __init__(self):
        QObject.__init__(self)
        self.experimentResults = []   
        
        self.resultPath = os.path.join(str(QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)),'EmcTestbench/')
        if not os.path.exists(self.resultPath):
            os.mkdir(self.resultPath)
            
        
    def __getitem__(self,key):
        return self.experimentResults[key]
    def refresh(self):
        self.experimentResults = []
        for fileName in glob.glob(self.resultPath+'*'+self.resultExtension):
            ExperimentResult.loadFromFileSystem(fileName)
    def append(self,newExperimentResult):
        self.experimentResults.append(newExperimentResult)
        self.extendedWith.emit(newExperimentResult)
        self.changed.emit()
        
if __name__ == '__main__':
#    ExperimentResult.loadFromFileSystem('Direct Power Injection 20120509-174045')
    ExperimentResultCollection.Instance().loadFromFileSystem()
#    class DummyExperiment:
#        name = 'DummyExperiment'
#    dummyExperiment = DummyExperiment()
#    print dummyExperiment
#    ExperimentResult(dummyExperiment,3)
#    print ExperimentResultCollection.Instance().results[0].experiment

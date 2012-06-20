#from PyQt4.QtGui import QApplication,QDesktopServices
from PyQt4.QtCore import QObject,pyqtSignal

#import log
#import inspect

#from device import knownDevices,Device
from result.resultset import Result
import experimentresultcollection


from result.persistance import Dommable
from xml.dom.minidom import getDOMImplementation,parse
from result.persistance import Dict

from copy import deepcopy
from datetime import datetime
import os

class ExperimentResult(QObject,Dommable):
    changed = pyqtSignal()    
    changedTo = pyqtSignal(object)    
    
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendChildObject(element,self.metadata,'metadata')
        self.appendChildObject(element,self.experiment,'experiment')
        self.appendChildObject(element,self.result,'result')
        return element

    @classmethod
    def fromDom(cls,dom):
        metadata = cls.childObjectById(dom,'metadata')
        result = cls.childObjectById(dom,'result')
        assert isinstance(result,Result),'Tag with id="result" yields no Result instance'
        return cls(None,result,save=False,metadata=metadata,name='From anonymous DOM')
    
    def __init__(self,experiment,result,save=True,metadata=None,name=None):
        QObject.__init__(self)
        self.saveCount = 0
        self._name = None
        
        if metadata == None:
            creationDate = datetime.now()
            metadata = Dict({'DUT':'','operator':'','creation':creationDate})
        self.metadata = metadata

        if name == None:
            name = experiment.name + creationDate.strftime(' %Y%m%d-%H%M%S')
        self.name = name

        self.experiment = deepcopy(experiment)
        self.result = result
        
        if save:
            self.saveToFileSystem()
        experimentresultcollection.ExperimentResultCollection.Instance().append(self)
        
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
#        QApplication.removePostedEvents(self)
        fileHandle = open(experimentresultcollection.ExperimentResultCollection.Instance().resultPath+self.name+experimentresultcollection.ExperimentResultCollection.Instance().resultExtension,'wb')
        document = getDOMImplementation().createDocument(None,'EmcTestbench',None)
        self.asDom(document.documentElement)
        fileHandle.write(document.toxml(encoding='utf-8'))
        fileHandle.close()
#        self.saveCount += 1
#        print self.saveCount
        del(fileHandle)
        
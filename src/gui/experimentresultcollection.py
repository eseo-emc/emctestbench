from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from PyQt4.QtGui import QDesktopServices,QApplication
import experimentresult

import glob
import os
import sys
import log
        

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
    def experimentResultFiles(self,relativePath):
        return glob.glob(self.resultPath+relativePath+'*'+self.resultExtension)
    def loadExperimentResultFiles(self,relativePath):
        experimentResults = {}
        for fileName in self.experimentResultFiles(relativePath):
            try:
                experimentResult = experimentresult.ExperimentResult.loadFromFileSystem(fileName)
                experimentResults.update({experimentResult.name : experimentResult})
            except:
                log.LogItem('Error while reading {fileName}: {errorMessage}'.format(fileName=fileName,errorMessage=sys.exc_info()[1]),log.warning)
        return experimentResults

    def refresh(self):
        self.experimentResults = []
        self.loadExperimentResultFiles(relativePath='')
                         
    def append(self,newExperimentResult):
        self.experimentResults.append(newExperimentResult)
        self.extendedWith.emit(newExperimentResult)
        self.changed.emit()
    def remove(self,existingExperimentResult):
        self.experimentResults.remove(existingExperimentResult)
        self.changed.emit()
        
if __name__ == '__main__':
#    ExperimentResult.loadFromFileSystem('Direct Power Injection 20120509-174045')
    ExperimentResultCollection.Instance().refresh()
#    class DummyExperiment:
#        name = 'DummyExperiment'
#    dummyExperiment = DummyExperiment()
#    print dummyExperiment
#    ExperimentResult(dummyExperiment,3)
#    print ExperimentResultCollection.Instance().results[0].experiment

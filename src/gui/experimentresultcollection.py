from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal
from PyQt4.QtGui import QDesktopServices,QApplication
import experimentresult

import glob
import os
import sys
import logging
        

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
            try:
                experimentresult.ExperimentResult.loadFromFileSystem(fileName)
            except:
                logging.LogItem('Error while reading {fileName}: {errorMessage}'.format(fileName=fileName,errorMessage=sys.exc_info()[1]),logging.error)
                raise 
    def append(self,newExperimentResult):
        self.experimentResults.append(newExperimentResult)
        self.extendedWith.emit(newExperimentResult)
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

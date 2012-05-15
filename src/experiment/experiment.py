from PyQt4.QtCore import QObject,QThread
from PyQt4.QtCore import pyqtSignal
import numpy
import string

from result.persistance import Dommable
from gui.experimentresult import ExperimentResult

class Property(QObject):
    changed = pyqtSignal()
    changedTo = pyqtSignal(object)    
    
    def __init__(self,defaultValue,castTo=None,changedSignal=None):
        QObject.__init__(self)
        self._castTo = castTo
        self.setValue(defaultValue)
        if changedSignal:
            self.changed.connect(changedSignal)
        
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self.setValue(value)
    def setValue(self,value):
        if self._castTo is not None:
            value = self._castTo(value)
        self._value = value
        self._emitChanged()
    def _emitChanged(self):
        self.changed.emit()
        self.changedTo.emit(self.value)
        
class ExperimentSlot(Property):
    def __init__(self,parent=None,defaultValue=None):
        self._value = None
        self.parent = parent
        Property.__init__(self,defaultValue=defaultValue)
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self.setValue(value)
    def setValue(self,experiment):
        if type(experiment) == str:
            exec('''
from {moduleName} import {experimentName}
experiment = {experimentName}'''.format(moduleName=string.lower(experiment),experimentName=experiment) )

        if isinstance(experiment,type):
            experiment = experiment()
        if type(experiment) is not type(self._value):
            self._value = experiment
            self._value.parent = self.parent
            self._emitChanged()

class SweepRange(Dommable):
    def __init__(self,startValue=0,stopValue=1,numberOfPoints=101,logarithmic=False,changedSignal=None):
        self.start = Property(startValue,changedSignal=changedSignal)
        self.stop = Property(stopValue,changedSignal=changedSignal)
        self.numberOfPoints = Property(numberOfPoints,changedSignal=changedSignal,castTo=int)
        self.logarithmic = Property(logarithmic,changedSignal=changedSignal)
    @property
    def values(self):
        if self.logarithmic.value:
            return numpy.exp(numpy.linspace(numpy.log(self.start.value),numpy.log(self.stop.value),self.numberOfPoints.value))
        else:
            return numpy.linspace(self.start.value,self.stop.value,self.numberOfPoints.value)
    @classmethod
    def fromDom(cls,dom):
        startValue = float(dom.getAttribute('startValue'))
        stopValue = float(dom.getAttribute('stopValue'))
        numberOfPoints = int(dom.getAttribute('numberOfPoints'))
        logarithmic = dom.getAttribute('logarithmic') == 'True'
        return SweepRange(startValue,stopValue,numberOfPoints,logarithmic)
        
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        element.setAttribute('startValue',str(self.start.value))
        element.setAttribute('stopValue',str(self.stop.value))
        element.setAttribute('numberOfPoints',str(self.numberOfPoints.value))
        element.setAttribute('logarithmic',str(self.logarithmic.value))
        return element

class Experiment(QThread):
    name = 'Experiment'
    settingsChanged = pyqtSignal()
    
    progressed = pyqtSignal(int)
    finished = pyqtSignal()    
    newResult = pyqtSignal(object)
    
    def __init__(self):
        QThread.__init__(self)
        self.stopRequested = False
        self._result = None
        self.parent = None
    
    def prepare(self):
        raise NotImplementedError
  
    def measure(self):
        return self.run()  
        
    def stop(self):
        self.stopRequested = True
        
    def emitResult(self,result):
        if self.parent == None:
            ExperimentResult(self,result)
        self.newResult.emit(result)
    

    
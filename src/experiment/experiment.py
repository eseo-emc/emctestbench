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
        
class ScalarProperty(Property):
    def __init__(self,defaultValue,castTo=None,changedSignal=None,minimum=None,maximum=None):
        Property.__init__(self,defaultValue,castTo,changedSignal)
        if minimum == None:
            minimum = type(defaultValue)(-numpy.inf)
        if maximum == None:
            maximum = type(defaultValue)(numpy.inf)
            
        self.minimum = minimum
        self.maximum = maximum
        
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
        startValue = cls.childObjectById(dom,'start value')
        stopValue = cls.childObjectById(dom,'stop value')
        numberOfPoints = cls.childObjectById(dom,'number of points')
        logarithmic = cls.childObjectById(dom,'logarithmic')
        return SweepRange(startValue,stopValue,numberOfPoints,logarithmic)
        
    def asDom(self,parent):
        element = Dommable.asDom(self,parent)
        self.appendChildObject(element,self.start.value,'start value')
        self.appendChildObject(element,self.stop.value,'stop value')
        self.appendChildObject(element,self.numberOfPoints.value,'number of points')
        self.appendChildObject(element,self.logarithmic.value,'logarithmic')
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
    

if __name__ == '__main__':
    from utility import quantities
    import copy
    a = Property(quantities.Power(3,'dBm'))
    print a.value
    b= copy.deepcopy(a)
    print b.value
    
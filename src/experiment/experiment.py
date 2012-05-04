from PyQt4.QtCore import QObject,QThread
from PyQt4.QtCore import pyqtSignal
import numpy
import string

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
    def __init__(self,defaultValue=None):
        self._value = None
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
            self._emitChanged()

class SweepRange(object):
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



class Experiment(QThread):
    name = 'Experiment'
    settingsChanged = pyqtSignal()
    newResult = pyqtSignal(object)
    
    progressed = pyqtSignal(int)
    finished = pyqtSignal()    
    
    def __init__(self):
        QThread.__init__(self)
        self.stopRequested = False
        self._result = None
    
#    def result(self):
#        return self._result
#        
    def measure(self):
        return self.run()  
        
    def stop(self):
        self.stopRequested = True
    
    name = None
    def prepare(self):
        raise NotImplementedError
    
from PyQt4.QtCore import QObject,QThread
from PyQt4.QtCore import pyqtSignal
import numpy


class Property(QObject):
    changed = pyqtSignal()
    changedTo = pyqtSignal(object)    
    
    def __init__(self,defaultValue,castTo=None,changedSignal=None):
        QObject.__init__(self)
        self._value = defaultValue
        if changedSignal:
            self.changed.connect(changedSignal)
        self._castTo = castTo
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

        self.changed.emit()
        self.changedTo.emit(self.value)

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

#class Result(Property):
#    def __init__(self,parent,defaultValue):
#        Property.__init__(self,defaultValue,changedSignal=parent.resultChanged)

   

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
    
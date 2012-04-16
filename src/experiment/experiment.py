from PyQt4.QtCore import QObject,QThread

class Property(object):
    def __init__(self,defaultValue,castTo=None,changedSignal=None):
        self._value = defaultValue
        self._changedSignal = changedSignal
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
        if self._changedSignal:
            self._changedSignal.emit()
    

class Experiment(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.stopRequested = False
    def stop(self):
        self.stopRequested = True
    
    name = None
    def prepare():
        raise NotImplementedError
    def measure():
        raise NotImplementedError
from PyQt4.QtCore import QObject,QThread

class Property(object):
    def __init__(self,defaultValue,changedSignal=None):
        self._value = defaultValue
        self._changedSignal = changedSignal
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        self.setValue(value)
    def setValue(self,value):
        self._value = value
        if self._changedSignal:
            self._changedSignal.emit()
    

class Experiment(QThread):
    name = None
    def prepare():
        raise NotImplementedError
    def measure():
        raise NotImplementedError
from utility import Singleton
from PyQt4.QtCore import QObject,pyqtSignal


import inspect
import logging

import experiment

@Singleton
class ExperimentCollection(QObject):
    changed = pyqtSignal()    
    
    def __init__(self):
        QObject.__init__(self)
        self.experiments = []        
    def discover(self):
        discoveredExperimentClasses = []
        for moduleName in experiment.__all__:
            exec('import experiment.'+moduleName)
            module = eval('experiment.'+moduleName)
            logging.LogItem('Looking for experiments in {moduleName}...'.format(moduleName=moduleName),logging.debug)
            for className in dir(module):
                
                testClass = getattr(module,className)
                if inspect.isclass(testClass):
                    if issubclass(testClass,experiment.experiment.Experiment) and testClass != experiment.experiment.Experiment:
                        if testClass not in discoveredExperimentClasses:
                            logging.LogItem('Found {className}...'.format(className=testClass.__name__),logging.debug)
                            discoveredExperimentClasses.append(testClass)
        
        for discoveredExperimentClass in discoveredExperimentClasses:
            self.experiments.append(discoveredExperimentClass())
        self.changed.emit()

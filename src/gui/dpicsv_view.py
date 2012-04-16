import csv
import datetime
from PyQt4.QtCore import QObject
from gui import logging


class DpiCsv(QObject):
    def __init__(self):
        QObject.__init__(self)
        self._fileHandle = None

    def _createFile(self):
        #TODO: the date should actually come from the creation timestamp of the resultset
        fileName = 'Y:/emctestbench/results/dpi'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'.xls'
        self._fileHandle = open(fileName,'wb') #,buffering=1)
        logging.LogItem('Created {fileName}'.format(fileName=fileName),logging.info)
        tableHeaders = ['frequency (Hz)','generator (dBm)','forward (dBm)','reflected (dBm)','transmitted (dBm)','fail']
        self._writer = csv.DictWriter(self._fileHandle,tableHeaders,dialect='excel-tab')
        self._writer.writeheader()
        
        
    def writeResultRow(self,result):
        if self._fileHandle == None:
            self._createFile()
        self._writer.writerow({'frequency (Hz)':result['frequency'],
                         'generator (dBm)':result['generatorPower'].dBm(),
                         'forward (dBm)':result['forwardPower'].dBm(),
                         'reflected (dBm)':result['reflectedPower'].dBm(),
                         'transmitted (dBm)':result['transmittedPower'].dBm(),
                         'fail':(0 if result['pass'] else 1) })
        self._fileHandle.flush()
        
    def close(self):
        self._fileHandle.close()
        self._fileHandle = None
         
        
if __name__ == '__main__':
    import time
    from utility import Power
    test = DpiCsv()
    print test.fileName
    for frequency in range(10000,250000,10000):
        print frequency
        test.writeResultRow({'frequency':10000*frequency,
                            'generatorPower':Power(20,'dBm'),
                            'forwardPower':Power(15,'dBm'),
                            'reflectedPower':Power(10,'dBm'),
                            'transmittedPower':Power(19,'dBm'),
                            'pass':True})
        time.sleep(1)
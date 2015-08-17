from device import knownDevices
from utility import debugging
from utility import latex

import numpy
import skrf
import pylab

from PyQt4.QtGui import QDesktopServices,QApplication
import os
import inspect
import datetime

import ConfigParser



# sequence parameters
switchNames = ['Gen Out','DUT','E4419 Pi','E4419 Pr']
oppositeSuffices = ['In','Out','Pi','Pr']

positions = ['86205A','773D','Prana','Milmega']
measureIncidents = [False,False,True,True]

def prompt(message,showOptions = False):
#    print message
    if showOptions:
        message += ' (press s to skip, a to abort)'
    return raw_input(message)


class Connection(object):
    
    def __init__(self,switchName,oppositePort,oppositeSuffix,switchPosition):
        self.switchName = switchName
        self.oppositePort = oppositePort
        self.oppositeSuffix = oppositeSuffix
        self.switchPosition = switchPosition
    
    @property
    def port1(self):
        return self.switchName
    @property
    def port2(self):
        return self.oppositePort + ' ' + self.oppositeSuffix
          
    @property
    def fileName(self):
        return '{0}-{1} (position {2})'.format(self.port1,self.port2,self.switchPosition)

    def promptToPlug(self,lastConnection=None):
        if not(lastConnection) or self.port1 != lastConnection.port1:
            QApplication.beep()
            prompt('Connect port 1 to '+self.port1)
        if not(lastConnection) or self.port2 != lastConnection.port2:
            QApplication.beep()
            return prompt('Connect port 2 to '+self.port2,showOptions=True)
        return ''
            
    def measureAndSave(self,vna,switch,resultDirectory):
        switch.setPreset(self.switchPosition)
        self.measurement = vna.measure()
        self.measurement.name = self.fileName
        self.measurement.write_touchstone(dir=resultDirectory)
    def loadFromNetworkSet(self,networkSet):
        try:
            self.measurement = networkSet[self.fileName]
        except KeyError:
            return False
        return True
        
    @property
    def shouldThru(self):
        return self.oppositePort == self.switchPosition
    @property
    def _diagonalSimilarity(self):
        return numpy.average(numpy.abs(self.measurement.s_db[:,1,0]-self.measurement.s_db[:,0,1]))
    def _diagonalSimilarityPassThru(self):
        return abs(self._diagonalSimilarity) < 10
    @property
    def _minimumTransfer(self):
        return numpy.min(self.measurement.s_db[:,1,0])
    @property
    def _minimumTransferPassThru(self):
        return self._minimumTransfer > -3.0
    
    @property
    def _maximumTransfer(self):
        return numpy.max(self.measurement.s_db[:,1,0])
    @property
    def _maximumTransferPassNonThru(self):
        return self._maximumTransfer < -65.0

    @property    
    def passNotFail(self):
        if self.shouldThru:
            return self._diagonalSimilarityPassThru and self._minimumTransferPassThru
        else:
            return self._maximumTransferPassNonThru
            
    def reportPass(self):
        return self.fileName + ' ' + ('pass' if self.passNotFail else 'FAIL') + '(' + self.report() + ')'
    def report(self):
        reportText = ''            
        if self.shouldThru:
            reportText += '$\min(S_{{21}}) = {transfer:.1f} dB'.format(transfer=self._minimumTransfer)
        else:
            reportText += '$\max(S_{{21}}) = {transfer:.1f} dB'.format(transfer=self._maximumTransfer)
        return reportText
        
    

class QualifySwitch(object):
    def __init__(self):
        self.metadata = ConfigParser.RawConfigParser()
    
    def platformConnections(self):
        for (switchName,oppositeSuffix) in zip(switchNames,oppositeSuffices):
            for (oppositePort,measureIncident) in zip(positions,measureIncidents):
                if not(switchName == 'E4419 Pi' and not(measureIncident)):
                    for (switchPosition,measureIncident) in zip(positions,measureIncidents):
                        if not(switchName == 'E4419 Pi' and not(measureIncident)):                    
                            yield Connection(switchName,oppositePort,oppositeSuffix,switchPosition)
    
    def connectionsPerSwitch(self):
        connections = dict()
        for switchName in switchNames:
            connections[switchName] = {'thru':[],'nonThru':[]}
            
            for connection in self.platformConnections():
                if connection.switchName == switchName:
                    if connection.shouldThru:
                        connections[switchName]['thru'].append(connection)
                    else:
                        connections[switchName]['nonThru'].append(connection)
        return connections
            
    @property
    def connectionsDirectory(self):
        return os.path.realpath(os.path.join(self.qualificationDirectory,'connections')) 
class QualifySwitchMeasurement(QualifySwitch):
    def __init__(self):
        self.startMoment = datetime.datetime.now()              
        
        super(QualifySwitchMeasurement,self).__init__()
        
        self.vna = knownDevices['networkAnalyzer']
        self.switch = knownDevices['switchPlatform']        
        self.vna.putOnline()
        self.switch.putOnline()

        self.qualificationDirectory = os.path.join(str(QDesktopServices.storageLocation(QDesktopServices.DocumentsLocation)),'EmcTestbench/Qualification/L4490 '+self.startMoment.strftime('%Y-%m-%d %H%M%S'))
        os.mkdir(self.qualificationDirectory)        
        os.mkdir(self.connectionsDirectory)
    
        self.metadata.add_section('operation')        
        self.metadata.set('operation','startMoment',self.startMoment.isoformat())
        self.metadata.set('operation','operator',prompt('Please enter your name:'))
        self.metadata.set('operation','scriptFile',debugging.currentFile())

        self.metadata.add_section('equipment')
        self.metadata.set('equipment','vna',self.vna.detailedInformation)
        self.metadata.set('equipment','switchPlatform',self.switch.detailedInformation)
        
        
        self.metadata.add_section('calibration')
        self.metadata.set('calibration','calibrationKit',prompt('Please enter the used calibration kit:'))
        self.metadata.set('calibration','calibrationNotes',prompt('Please enter other notes on the calibration (cables used, added offset, resulting reference plane:'))
        

         
    def start(self):
#        raw_input('Please calibrate the VNA to an N-connector male reference plane')
#        raw_input('Please connect a N-connector female short circuit to port 1')

        lastConnection = None
        for connection in self.platformConnections():
            userResponse = connection.promptToPlug(lastConnection)
            if userResponse == '':
                lastConnection = connection
                
                print('Measuring '+connection.fileName+'...')
                connection.measureAndSave(self.vna,self.switch,self.connectionsDirectory)
                if connection.passNotFail:
                    print "OK"
                else:
                    print "FAIL (" + connection.reportPass() + ')'
    #            print+(', should' if connection.shouldThru else ', should NOT')+' ressemble a thru')            
            elif userResponse == 'a':
                print 'Aborting'
                break
            elif userResponse == 's':
                continue
            else:
                print 'Input '+repr(userResponse)+' not recognized, aborting.'
                break
        
        self.metadata.set('operation','endMoment',datetime.datetime.now().isoformat())
        with open(self.qualificationDirectory + '/metadata.txt','w') as metaDataFile:
            self.metadata.write(metaDataFile)
        print "Measurements saved to "+repr(self.connectionsDirectory)
            
class QualifySwitchReport(QualifySwitch):
    def __init__(self,qualificationDirectory):
        super(QualifySwitchReport,self).__init__()
        self.qualificationDirectory = qualificationDirectory
        self._loadFromFileSystem()
        
    def _loadFromFileSystem(self):
        self.touchStones = skrf.read_all(self.connectionsDirectory)
        self.metadata.read(self.qualificationDirectory + '/metadata.txt')
        self.startMoment = datetime.datetime.strptime(self.metadata.get('operation','startmoment'),"%Y-%m-%dT%H:%M:%S.%f")
        self.endMoment = datetime.datetime.strptime(self.metadata.get('operation','endmoment'),"%Y-%m-%dT%H:%M:%S.%f")

    def show(self):
#        self.touchStones['Calibration Check 1'].plot_s_db()
        print "Measurements by " + self.metadata.get('operation','operator')
        for connection in self.platformConnections():
            if connection.loadFromNetworkSet(self.touchStones):
                print connection.reportPass()
            else:
                print "Measurement "+connection.fileName+" not found."
        
        for (switchName,switchConnections) in self.connectionsPerSwitch().items():
            pylab.figure()
            pylab.title(switchName)
            for thruConnection in switchConnections['thru']:
                thruConnection.loadFromNetworkSet(self.touchStones)
                thruConnection.measurement.plot_s_db(1,0)
        pylab.show()

    def writeReport(self):
        reportDirectory = os.path.join(self.qualificationDirectory,'report')    

        document = latex.LatexDocument(reportDirectory)  
        
        document.appendTitle('LL4490 Integration Test Report')
        document.appendBody('''\\section{Introduction}
This is the automatically generated report of the LL4490 integration test. The most important RF performance metrics are listed, such as the transmission and reflection of closed switches. The reference plane is (close to) the N-connectors at the front- and backpanel of the L4490.
All measurement data was stored at ''' + document.texEscape(self.connectionsDirectory) + ' The measurement was guided by '+document.texEscape(self.metadata.get('operation','scriptfile'))+'\\\\')

        document.appendTabular([
            ('Measurement start:',self.startMoment.strftime("%d-%m-%Y %H:%M")),
            ('Measurement end:',self.endMoment.strftime("%d-%m-%Y %H:%M")),
            ('Operator:',self.metadata.get('operation','operator')),
        ],alignment='rl')
        

        document.appendBody('\n\\subsection{Calibration}\nCalibration kit: '+document.texEscape(self.metadata.get('calibration','calibrationkit'))+'\n\n')
        document.appendBody(document.texEscape(self.metadata.get('calibration','calibrationnotes')))        
        
        document.appendBody('\n\\subsection{Equipment}\n')
        document.appendBody('Network analyser: '+document.texEscape(self.metadata.get('equipment','vna')))
        document.appendBody('\\\\DUT: '+document.texEscape(self.metadata.get('equipment','switchplatform')))
        
        document.appendBody('''
\\subsection{Signature}
'''+document.texEscape(self.metadata.get('operation','operator'))+', '+ self.endMoment.strftime("%d-%m-%Y") + '''\\\\
\\\\
\\\\
\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots\\ldots
''')

        for (switchName,switchConnections) in self.connectionsPerSwitch().items():
            document.appendBody('\n\\clearpage\n\\section{Switch '+switchName+'}\n')            
            document.appendBody('\n\\subsection{Closed switch}\n')            
            
            graph = pylab.figure()
            name = switchName + '_transmission'
            for thruConnection in switchConnections['thru']:
                thruConnection.loadFromNetworkSet(self.touchStones)
                thruConnection.measurement.plot_s_db(1,0)
            pylab.legend(loc='upper right')
            document.appendGraph(graph,name,switchName+' transmission parameters in the different preset positions.')

            graph = pylab.figure()
            name = switchName + '_reflection'
            for thruConnection in switchConnections['thru']:
                thruConnection.loadFromNetworkSet(self.touchStones)
                thruConnection.measurement.plot_s_db(0,0)
                thruConnection.measurement.plot_s_db(1,1)
            pylab.legend(loc='lower right')
            document.appendGraph(graph,name,switchName+' reflection parameters in the different preset positions.')


        document.writeOut()
#    ('Power',document.texQuantity(-3,'dB',emphasis=True))

        
        
if __name__ == '__main__':
    # MEASUREMENT
    measurement = QualifySwitchMeasurement()
    measurement.start()
    print repr(measurement.qualificationDirectory)

#    # REPORT
#    report = QualifySwitchReport('D:\\User_My_Documents\\Instrument\\My Documents\\EmcTestbench\\Qualification\\L4490 2013-09-24 100249 26 GHz calibration tightened')
#    report.writeReport()
    
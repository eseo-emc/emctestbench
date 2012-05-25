from PyQt4.QtGui import QWidget
from gui.nearfieldscanresult_view import Ui_NearFieldScanResult

class NearFieldScanResultController(QWidget,Ui_NearFieldScanResult):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setupUi(self)  
        
        self._model = None
        
    @property
    def model(self):
        return self._model
    @model.setter
    def model(self,value):
        self._model = value
        self.update(self._model)
        self._model.changedTo.connect(self.update)
        
        self.transmittedPower.toggled.connect(self.updateSettings)
        self.dBm.toggled.connect(self.updateSettings)
        self.W.toggled.connect(self.updateSettings)
        
    def updateSettings(self):
        self.update(self._model)
    def update(self,result):
        unitName = ('W' if self.W.isChecked() else 'dBm')   
        horizontalUnit = result['position'].preferredUnit()

        if result is not None:
            yPoints = result['position'][:,1].asUnit(horizontalUnit)
            self.graph.axes.hold(False)
            self.graph.axes.plot(yPoints, result['received power'].asUnit(unitName),label='Received power')
            self.graph.axes.hold(True)
            if self.transmittedPower.isChecked():
                self.graph.axes.plot(yPoints, result['transmitted power'].asUnit(unitName),label='Transmitted power')
                    
        self.graph.axes.set_xlabel('y Position ({unitName})'.format(unitName=horizontalUnit))
        self.graph.axes.set_ylabel('Power ({unitName})'.format(unitName=unitName))
        self.graph.axes.legend()
        self.graph.draw() #redraw_in_frame()
#        self.graph.figure.set_frameon(False)



#if __name__ == '__main__':
#    import sys
#    from PyQt4.QtGui import QApplication,QMainWindow
#    from experiment.dpi import DpiResult
#    from experiment.experiment import SweepRange
#    from utility.quantities import Power
#    from numpy import nan
#    import datetime
#    
#    application = QApplication(sys.argv)
#    window = QMainWindow()
#    
#    widgetUnderTest = NearFieldScanResultController(window)
#
#    testResult = DpiResult(Power([-25,+20],'dBm'),SweepRange(30e3,6e9))
#    testResult._data = {'reflectedPower': Power([nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.1, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.1, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.2, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.2, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, -0.4, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, -3.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, -4.1],'dBm'),
#                        'forwardPower': Power([nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.1, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.1, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.2, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.2, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +7.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +5.6, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +3.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.9],'dBm'),
#                        'timeStamp': [datetime.datetime(2012, 4, 27, 11, 51, 42, 131000), datetime.datetime(2012, 4, 27, 11, 51, 42, 131000), datetime.datetime(2012, 4, 27, 11, 51, 42, 131000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 146000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 162000), datetime.datetime(2012, 4, 27, 11, 51, 42, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 177000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 193000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 209000), datetime.datetime(2012, 4, 27, 11, 51, 43, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 224000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 240000), datetime.datetime(2012, 4, 27, 11, 51, 44, 256000), datetime.datetime(2012, 4, 27, 11, 51, 44, 256000), datetime.datetime(2012, 4, 27, 11, 51, 44, 256000), datetime.datetime(2012, 4, 27, 11, 51, 44, 256000), datetime.datetime(2012, 4, 27, 11, 51, 44, 256000), datetime.datetime(2012, 4, 27, 11, 51, 44, 271000), datetime.datetime(2012, 4, 27, 11, 51, 44, 271000), datetime.datetime(2012, 4, 27, 11, 51, 44, 271000), datetime.datetime(2012, 4, 27, 11, 51, 45, 271000), datetime.datetime(2012, 4, 27, 11, 51, 45, 271000), datetime.datetime(2012, 4, 27, 11, 51, 45, 287000), datetime.datetime(2012, 4, 27, 11, 51, 45, 287000), datetime.datetime(2012, 4, 27, 11, 51, 45, 287000), datetime.datetime(2012, 4, 27, 11, 51, 45, 287000), datetime.datetime(2012, 4, 27, 11, 51, 45, 287000), datetime.datetime(2012, 4, 27, 11, 51, 45, 302000), datetime.datetime(2012, 4, 27, 11, 51, 45, 302000), datetime.datetime(2012, 4, 27, 11, 51, 45, 302000), datetime.datetime(2012, 4, 27, 11, 51, 45, 302000), datetime.datetime(2012, 4, 27, 11, 51, 45, 318000), datetime.datetime(2012, 4, 27, 11, 51, 45, 318000), datetime.datetime(2012, 4, 27, 11, 51, 45, 318000), datetime.datetime(2012, 4, 27, 11, 51, 45, 318000), datetime.datetime(2012, 4, 27, 11, 51, 45, 318000), datetime.datetime(2012, 4, 27, 11, 51, 45, 334000), datetime.datetime(2012, 4, 27, 11, 51, 45, 334000), datetime.datetime(2012, 4, 27, 11, 51, 45, 334000), datetime.datetime(2012, 4, 27, 11, 51, 45, 334000), datetime.datetime(2012, 4, 27, 11, 51, 45, 334000), datetime.datetime(2012, 4, 27, 11, 51, 45, 349000), datetime.datetime(2012, 4, 27, 11, 51, 46, 349000), datetime.datetime(2012, 4, 27, 11, 51, 46, 349000), datetime.datetime(2012, 4, 27, 11, 51, 46, 349000), datetime.datetime(2012, 4, 27, 11, 51, 46, 365000), datetime.datetime(2012, 4, 27, 11, 51, 46, 365000), datetime.datetime(2012, 4, 27, 11, 51, 46, 365000), datetime.datetime(2012, 4, 27, 11, 51, 46, 365000), datetime.datetime(2012, 4, 27, 11, 51, 46, 380000), datetime.datetime(2012, 4, 27, 11, 51, 46, 380000), datetime.datetime(2012, 4, 27, 11, 51, 46, 380000), datetime.datetime(2012, 4, 27, 11, 51, 46, 380000), datetime.datetime(2012, 4, 27, 11, 51, 46, 380000), datetime.datetime(2012, 4, 27, 11, 51, 46, 396000), datetime.datetime(2012, 4, 27, 11, 51, 46, 396000), datetime.datetime(2012, 4, 27, 11, 51, 46, 396000), datetime.datetime(2012, 4, 27, 11, 51, 46, 396000), datetime.datetime(2012, 4, 27, 11, 51, 46, 412000), datetime.datetime(2012, 4, 27, 11, 51, 46, 412000), datetime.datetime(2012, 4, 27, 11, 51, 46, 412000), datetime.datetime(2012, 4, 27, 11, 51, 46, 412000), datetime.datetime(2012, 4, 27, 11, 51, 46, 427000), datetime.datetime(2012, 4, 27, 11, 51, 47, 427000), datetime.datetime(2012, 4, 27, 11, 51, 47, 427000), datetime.datetime(2012, 4, 27, 11, 51, 47, 427000), datetime.datetime(2012, 4, 27, 11, 51, 47, 443000), datetime.datetime(2012, 4, 27, 11, 51, 47, 443000), datetime.datetime(2012, 4, 27, 11, 51, 47, 443000), datetime.datetime(2012, 4, 27, 11, 51, 47, 443000), datetime.datetime(2012, 4, 27, 11, 51, 47, 459000), datetime.datetime(2012, 4, 27, 11, 51, 47, 459000), datetime.datetime(2012, 4, 27, 11, 51, 47, 459000), datetime.datetime(2012, 4, 27, 11, 51, 47, 474000), datetime.datetime(2012, 4, 27, 11, 51, 47, 474000), datetime.datetime(2012, 4, 27, 11, 51, 47, 474000), datetime.datetime(2012, 4, 27, 11, 51, 47, 474000), datetime.datetime(2012, 4, 27, 11, 51, 47, 490000), datetime.datetime(2012, 4, 27, 11, 51, 47, 490000), datetime.datetime(2012, 4, 27, 11, 51, 47, 490000), datetime.datetime(2012, 4, 27, 11, 51, 47, 490000), datetime.datetime(2012, 4, 27, 11, 51, 47, 505000), datetime.datetime(2012, 4, 27, 11, 51, 47, 505000), datetime.datetime(2012, 4, 27, 11, 51, 47, 505000), datetime.datetime(2012, 4, 27, 11, 51, 47, 521000), datetime.datetime(2012, 4, 27, 11, 51, 48, 521000), datetime.datetime(2012, 4, 27, 11, 51, 48, 521000), datetime.datetime(2012, 4, 27, 11, 51, 48, 521000), datetime.datetime(2012, 4, 27, 11, 51, 48, 537000), datetime.datetime(2012, 4, 27, 11, 51, 48, 537000), datetime.datetime(2012, 4, 27, 11, 51, 48, 537000), datetime.datetime(2012, 4, 27, 11, 51, 48, 552000), datetime.datetime(2012, 4, 27, 11, 51, 48, 552000), datetime.datetime(2012, 4, 27, 11, 51, 48, 552000), datetime.datetime(2012, 4, 27, 11, 51, 48, 552000), datetime.datetime(2012, 4, 27, 11, 51, 48, 568000), datetime.datetime(2012, 4, 27, 11, 51, 48, 568000), datetime.datetime(2012, 4, 27, 11, 51, 48, 568000), datetime.datetime(2012, 4, 27, 11, 51, 48, 584000), datetime.datetime(2012, 4, 27, 11, 51, 48, 584000), datetime.datetime(2012, 4, 27, 11, 51, 48, 584000), datetime.datetime(2012, 4, 27, 11, 51, 48, 599000), datetime.datetime(2012, 4, 27, 11, 51, 48, 599000), datetime.datetime(2012, 4, 27, 11, 51, 48, 599000), datetime.datetime(2012, 4, 27, 11, 51, 48, 599000), datetime.datetime(2012, 4, 27, 11, 51, 48, 615000), datetime.datetime(2012, 4, 27, 11, 51, 48, 615000), datetime.datetime(2012, 4, 27, 11, 51, 49, 615000), datetime.datetime(2012, 4, 27, 11, 51, 49, 630000), datetime.datetime(2012, 4, 27, 11, 51, 49, 630000), datetime.datetime(2012, 4, 27, 11, 51, 49, 630000), datetime.datetime(2012, 4, 27, 11, 51, 49, 646000), datetime.datetime(2012, 4, 27, 11, 51, 49, 646000), datetime.datetime(2012, 4, 27, 11, 51, 49, 646000), datetime.datetime(2012, 4, 27, 11, 51, 49, 662000), datetime.datetime(2012, 4, 27, 11, 51, 49, 662000), datetime.datetime(2012, 4, 27, 11, 51, 49, 662000), datetime.datetime(2012, 4, 27, 11, 51, 49, 677000), datetime.datetime(2012, 4, 27, 11, 51, 50, 677000), datetime.datetime(2012, 4, 27, 11, 51, 50, 677000), datetime.datetime(2012, 4, 27, 11, 51, 50, 693000), datetime.datetime(2012, 4, 27, 11, 51, 50, 693000), datetime.datetime(2012, 4, 27, 11, 51, 50, 709000), datetime.datetime(2012, 4, 27, 11, 51, 50, 709000), datetime.datetime(2012, 4, 27, 11, 51, 50, 709000), datetime.datetime(2012, 4, 27, 11, 51, 50, 724000), datetime.datetime(2012, 4, 27, 11, 51, 50, 724000), datetime.datetime(2012, 4, 27, 11, 51, 50, 724000), datetime.datetime(2012, 4, 27, 11, 51, 50, 740000), datetime.datetime(2012, 4, 27, 11, 51, 51, 740000), datetime.datetime(2012, 4, 27, 11, 51, 51, 740000), datetime.datetime(2012, 4, 27, 11, 51, 51, 755000), datetime.datetime(2012, 4, 27, 11, 51, 51, 755000), datetime.datetime(2012, 4, 27, 11, 51, 51, 755000), datetime.datetime(2012, 4, 27, 11, 51, 51, 771000), datetime.datetime(2012, 4, 27, 11, 51, 51, 771000), datetime.datetime(2012, 4, 27, 11, 51, 51, 771000), datetime.datetime(2012, 4, 27, 11, 51, 51, 787000), datetime.datetime(2012, 4, 27, 11, 51, 51, 787000), datetime.datetime(2012, 4, 27, 11, 51, 51, 787000), datetime.datetime(2012, 4, 27, 11, 51, 52, 802000), datetime.datetime(2012, 4, 27, 11, 51, 52, 802000), datetime.datetime(2012, 4, 27, 11, 51, 52, 818000), datetime.datetime(2012, 4, 27, 11, 51, 52, 818000), datetime.datetime(2012, 4, 27, 11, 51, 52, 818000), datetime.datetime(2012, 4, 27, 11, 51, 52, 834000), datetime.datetime(2012, 4, 27, 11, 51, 52, 834000), datetime.datetime(2012, 4, 27, 11, 51, 52, 834000), datetime.datetime(2012, 4, 27, 11, 51, 52, 849000), datetime.datetime(2012, 4, 27, 11, 51, 52, 849000), datetime.datetime(2012, 4, 27, 11, 51, 52, 865000), datetime.datetime(2012, 4, 27, 11, 51, 53, 865000)],
#                        'frequency': [150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 150000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 600135000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1200120000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 1800105000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 2400090000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3000075000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 3600060000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4200045000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 4800030000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 5400015000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0, 6000000000.0], 
#                        'generatorPower': Power([-30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +5.0, +6.0, +7.0, +8.0, +9.0, +8.0, +8.5, +8.0, +8.2, +8.2, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +10.0, +10.5, +11.0, +10.5, +10.8, +11.0, +11.0, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +12.0, +13.0, +12.0, +12.5, +12.0, +12.2, +12.2, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +12.0, +13.0, +14.0, +15.0, +14.0, +14.5, +14.0, +14.2, +14.5, +14.5, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +12.0, +13.0, +14.0, +13.0, +13.5, +13.0, +13.2, +13.5, +13.5, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +12.0, +13.0, +14.0, +13.0, +13.5, +14.0, +13.5, +13.8, +14.0, +14.0, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +10.0, +11.0, +12.0, +13.0, +14.0, +15.0, +14.0, +14.5, +14.0, +14.2, +14.5, +14.5, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +15.0, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +15.0, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +15.0, -30.0, -25.0, -20.0, -15.0, -10.0, -5.0, +0.0, +5.0, +10.0, +15.0, +15.0],'dBm'), 
#                        'pass': [True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, False, True, False, False, True, True, True, True, True, True, True, True, True, False, True, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, False, True, False, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, False, True, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, False, True, True, True, True, True, False, True, False, True, True, False, False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True], 'limit': [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, True], 
#                        'transmittedPower': Power([nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +5.9, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +6.1, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +5.9, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +6.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +6.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +6.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +6.0, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +5.8, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +4.3, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +1.8, nan, nan, nan, nan, nan, nan, nan, nan, nan, nan, +0.7],'dBm')}
#
#    widgetUnderTest.model = testResult
#    
#    
#    window.setCentralWidget(widgetUnderTest)
#    window.show()
#        
#
#        
#    sys.exit(application.exec_())
from device import knownDevices
from utility.quantities import PowerRatio,Frequency


from numpy import pi,sqrt,sin


from calibration.bridge import bridgeInsertionTransferAt,bridgeCouplingFactorAt

class AnalyticBenchCorrections(object):
    def corrections(self,amplifier,frequency):
        switchAttenuation = PowerRatio(sqrt(frequency/Frequency(170,'GHz')),'dB') # 2 switches - cable - cable - 2 switches
        # in the incident path, these losses cancel (same loss for DUT and incident power meter)
        # in the reflected path, these losses appear (the signal suffers from two cables and twice the switch platform)
        if amplifier == 'None (86205A)':
            forwardCorrection = 1/PowerRatio(1.5,'dB')
            reflectedCorrection = switchAttenuation * PowerRatio(16.0 + 0.6*sin(2*pi*frequency/Frequency(12,'GHz')),'dB')
        elif amplifier == 'None (773D)':
            # http://cp.literature.agilent.com/litweb/pdf/00772-90001.pdf
            forwardCorrection = 1/PowerRatio(0.9,'dB')
            reflectedCorrection = switchAttenuation * PowerRatio(20.0,'dB')
        elif amplifier == 'Prana':
            forwardCorrection = PowerRatio(48.7 - 0.4*sin(2*pi*frequency/Frequency(1,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * forwardCorrection / PowerRatio(0.1,'dB')            
        elif amplifier == 'Milmega 1':
            forwardCorrection = PowerRatio(44.9 - 0.6*sin(2*pi*(frequency-Frequency(900,'MHz'))/Frequency(2,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * forwardCorrection * PowerRatio(0.4,'dB')
        elif amplifier == 'Milmega 2':
            forwardCorrection = PowerRatio(43.6 - 0.6*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
            reflectedCorrection = switchAttenuation * PowerRatio(44.4 - 1.1*sin(2*pi*(frequency-Frequency(1.9,'GHz'))/Frequency(4,'GHz')),'dB')
        
        elif amplifier.startswith('None'):
            raise ValueError, 'Non-existant bridge specifier'    
        else:
            raise ValueError, 'The switch platform is in an unsupported position.'
        
        return (forwardCorrection,reflectedCorrection)
    

class CompositeBenchCorrections(object):
    def corrections(self,amplifier,frequency):
        assert amplifier == 'None (86205A)'
        
        forwardCorrection = bridgeInsertionTransferAt(frequency)
        reflectedCorrection = 1 / bridgeCouplingFactorAt(frequency)
        
        return (forwardCorrection,reflectedCorrection)

class MeasuredBenchCorrections(object):
    pass
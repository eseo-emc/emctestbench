import scipy.optimize
import numpy
import pylab

from utility.touchstone import s1pFile
from utility.plotting_sjoerd import * 

# def testFunction(x):
#     return -(x[0]**2)
# 
# scipy.optimize.fmin(testFunction,numpy.array([2]))
# 
class Adapter:
    '''
    Representative of a two-port adapter, port 1 being connected to the 
    measurement reference plane, port 2 being connected to the DUT:
        VNA|-1adapter2-DUT
    '''
    def __init__(self,standards,measurements):
        '''
        currently, the only way to construct an Adapter, is based on SOL        
        measurements
        @param standards : sequence of standards, either each indexable with .frequencies and .s11Values, or consisting of one value
        @param measurements : sequence of measurements, each with .frequencies and .s11Values
        '''
        # Check that sampled frequencies of all data are the same, using the second measurement as reference
        self.frequencies = measurements[1].frequencies
        assert (measurements[0].frequencies == self.frequencies).all()
        assert (measurements[2].frequencies == self.frequencies).all()
        measurements = numpy.array([measurements[0].s11Values,measurements[1].s11Values,measurements[2].s11Values])
        
        # Check the standard definitions and elaborate to a list in case of a single complex value
        assert len(standards) == 3
        elaborateStandards = [] # list of numpy.arrays
        for standard in standards:
            if hasattr(standard, 'frequencies'):
                assert (standard.frequencies == self.frequencies).all()
                elaborateStandards.append(numpy.array(standard.s11Values))
            else:
                elaborateStandards.append(numpy.repeat(standard,len(self.frequencies)))
        elaborateStandards = numpy.array(elaborateStandards)
                
        # Solve for each frequency
        self.s11Values = []
        self.s22Values = []
        self.s1221Values = []
        for number,frequency in enumerate(self.frequencies):
            print '#%d: standards %s' % (number,str(elaborateStandards[:,number]))
            (s11Guess, s22Guess, s1221Guess) = Adapter.findAdapterParameters(elaborateStandards[:,number],measurements[:,number])
            self.s11Values.append(s11Guess)
            self.s22Values.append(s22Guess)
            self.s1221Values.append(s1221Guess)
            
        self.s1221Values = numpy.array(self.s1221Values)
        self.s11Values = numpy.array(self.s11Values)
        self.s22Values = numpy.array(self.s22Values)
        
    def deEmbed(self,measurement):
        '''
        De-embed a measurement performed with this adapter. That is, the 
        measurement was taken with the reference plane at port 1 of the adapter,
        and this function returns the measurement with the reference plane at 
        port 2 of this adapter.
        '''
        assert (measurement.frequencies == self.frequencies).all()
        return 1/(self.s1221Values/(measurement.s11Values-self.s11Values)+self.s22Values)
    def deEmbedOne(self,measurement,frequencyNumber=100):
        return 1/(self.s1221Values[frequencyNumber]/(measurement-self.s11Values[frequencyNumber])+self.s22Values[frequencyNumber])

        
    @staticmethod
    def findAdapterParameters(standards,measurements):
        adapterGuess = scipy.optimize.brute(Adapter.solCalibrationError,ranges=[(-1,1),(-1,1),(-1,1),(-1,1),(-1,1),(-1,1)],args=(standards,measurements),Ns=4,full_output=False)
    #     (adapterGuess,numberOfIterations,resultCode) = scipy.optimize.fmin_tnc(Adapter.solCalibrationError,numpy.array(adapterGuess),args=(standards,measurements),approx_grad=True,bounds=[(-1,1),(-1,1),(-1,1),(-1,1),(-1,1),(-1,1)])
    #     assert resultCode == 1
    #         
        s11Guess = complex(adapterGuess[0],adapterGuess[1])
        s22Guess = complex(adapterGuess[2],adapterGuess[3])
        s1221Guess = complex(adapterGuess[4],adapterGuess[5])
        
        return (s11Guess, s22Guess, s1221Guess)
        
    @staticmethod
    def solCalibrationError(sParametersAdapter,standards,measurements):
        '''
        Return the residual error for guessed adapter parameters S11, S22 and S1221,
        for given calibration measurements and calibration standard definitions
        @param sParametersAdapter : array of guessed adapter S11, S21 and S12*S21 parameters, the real and complex part of each (totalling to a 6-element array) 
        @param standards : iterable with standard complex reflection coefficients (a golden standard would thus be [-1,0,1])
        @param measurements : iterable with measurements of the chain <-adapter-standards in the same order as the standards
        @return real : squareroot of the sum of squared errors for each standard
        '''
        S11 = numpy.complex(sParametersAdapter[0],sParametersAdapter[1])
        S22 = numpy.complex(sParametersAdapter[2],sParametersAdapter[3])
        S1221 = numpy.complex(sParametersAdapter[4],sParametersAdapter[5])
        
        def measuredGammaNominal(gammaStandard):
            return S11 + (S1221 * gammaStandard)/(1 - gammaStandard * S22)
        
        shortError = measuredGammaNominal(standards[0]) - measurements[0]
        loadError = measuredGammaNominal(standards[1]) - measurements[1]
        openError = measuredGammaNominal(standards[2]) - measurements[2]
            
        return numpy.sqrt(abs(openError)**2+abs(shortError)**2+abs(loadError)**2)


        
if __name__ == '__qsd:fkljnqsdmlfkjqsdmlfkj__':
#     # Single frequency test
#     standards = numpy.array([-1,0,1]) # assume golden standards
#     measurements = standards*numpy.complex(0,1)
#     print findAdapterParameters(standards,measurements)
#     # print solCalibrationError([0,0,0,0,1,0],standards,measurements) # should be 0
     pass

import matplotlib
import matplotlib.pyplot as pyplot
import utility.conversion as conversion

from matplotlib.pyplot import rc


## Electrical delay
pyplot.rc('font', family='serif', serif='palatino', weight='normal',size=11)
rc('text', usetex=True)

fixtureDelay = 53e-12 #s from the fixture's SMA reference plane
elbowCalibratedOpen = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_L_open.s1p',delay=0)
pyplot.plot(elbowCalibratedOpen.frequencies/1e9,numpy.rad2deg(numpy.unwrap(numpy.angle(elbowCalibratedOpen.s11Values))),'xk',label='Measured open')
pyplot.plot(elbowCalibratedOpen.frequencies/1e9,numpy.rad2deg(numpy.unwrap(numpy.angle(numpy.exp(numpy.complex(0,-1)*2*2*numpy.pi*elbowCalibratedOpen.frequencies*fixtureDelay)))),'k',label='Fitted %.1f ps' % (fixtureDelay/1e-12))

def paperStyleGraph():
    pyplot.grid(True,which='major')
    pyplot.box(False)
    pyplot.tick_params(which='both',direction='out',top='off',right='off')
    pyplot.axvline(x=pyplot.xlim()[0],color='k')
    pyplot.axhline(y=pyplot.ylim()[0],color='k',clip_on=False)
pyplot.xlabel('Frequency (GHz)')
pyplot.ylabel('Unwrapped $\\angle S_{11}$ ($^{\\circ}$)')
paperStyleGraph()
oldYLimits = pyplot.ylim()
pyplot.yticks(90.*numpy.array(range(-10.,10.)))
pyplot.ylim(oldYLimits)
pyplot.xlim(0,20)

matplotlib.pyplot.legend()
matplotlib.pyplot.show()



## De-embed raw measurements
electricalDelay = 0 #174e-12 #s from the VNA port
shortMeasurement = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_shortA.s1p',delay=electricalDelay)
loadMeasurement  = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_loadA.s1p',delay=electricalDelay)
openMeasurement  = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_open.s1p',delay=electricalDelay)
shortStandard = s1pFile('../../../../ADS/Fixture_tests_prj/misc/simulated_short.s1p')
loadStandard = s1pFile('../../../../ADS/Fixture_tests_prj/misc/simulated_load.s1p')
openStandard = s1pFile('../../../../ADS/Fixture_tests_prj/misc/simulated_open.s1p')

# idealAdapter = Adapter([-1,0,1],[shortMeasurement,loadMeasurement,openMeasurement])
# loadAdapter = Adapter([-1,loadStandard,1],[shortMeasurement,loadMeasurement,openMeasurement])
loadShortOpenAdapter = Adapter([shortStandard,loadStandard,openStandard],[shortMeasurement,loadMeasurement,openMeasurement])
# 
# ## Find out electrical delay
# 
# matplotlib.pyplot.plot(loadShortOpenAdapter.frequencies,numpy.angle(loadShortOpenAdapter.s1221Values),label='Fitted')
# delay = 174e-12 #s
# matplotlib.pyplot.plot(loadShortOpenAdapter.frequencies,numpy.angle(numpy.exp(numpy.complex(0,-1)*2*2*numpy.pi*loadShortOpenAdapter.frequencies*delay)),label='Test')
# matplotlib.pyplot.xscale('symlog')
# matplotlib.pyplot.legend()
# matplotlib.pyplot.show()
#     

dutMeasurement = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_1pFC.s1p',delay=electricalDelay)
# realGamma = idealAdapter.deEmbed(dutMeasurement)
# loadRealGamma = loadAdapter.deEmbed(dutMeasurement)
loadShortRealGamma = loadShortOpenAdapter.deEmbed(dutMeasurement)
# 

## Polar plot
shiftedMeasurement = s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_L_1pFC.s1p',delay=fixtureDelay)
cstOffset = -8.0E-12
cstDeembed = s1pFile('../../../../ADS/Fixture_tests_prj/misc/simulatedFixture_deembed_1pF.s1p',delay=cstOffset)

# # pyplot.plot(self.frequencies,dB(abs(stoz(self.s11Values,50.0))),label=self.title)
# pyplot.polar(numpy.angle(dutMeasurement.s11Values),abs(dutMeasurement.s11Values),label='Uncompensated')
# pyplot.polar(numpy.angle(loadShortRealGamma),abs(loadShortRealGamma),label='Compensated')

smith()
pyplot.plot(numpy.real(shiftedMeasurement.s11Values),numpy.imag(shiftedMeasurement.s11Values),'k-',label='Electrical delay')
pyplot.plot(numpy.real(loadShortRealGamma),numpy.imag(loadShortRealGamma),'k--',label='SOL calibration')
pyplot.plot(numpy.real(cstDeembed.s11Values),numpy.imag(cstDeembed.s11Values),'k:',label='CST de-embedded + %.1f ps' % (-cstOffset/1e-12))

# pyplot.polar(numpy.angle(loadShortRealGamma),abs(loadShortRealGamma),label='$\{0\Omega,50\Omega+0.64\mathrm{nH}+0.1\mathrm{pF},0.22\mathrm{nH}\}$')
# pyplot.polar(numpy.angle(loadRealGamma),abs(loadRealGamma),          label='$\{0\Omega,50\Omega+0.64\mathrm{nH}+0.1\mathrm{pF},\infty\Omega\}$')    
# pyplot.polar(numpy.angle(realGamma),abs(realGamma),                  label='$\{0\Omega,50\Omega,\infty\Omega\}$')                                   
# pyplot.title('Calibrating with different standard definitions')

theLegend = pyplot.legend(loc='lower right')

pyplot.grid(False)
pyplot.box(False)
pyplot.tick_params(top='off',bottom='off',left='off',right='off',labeltop='off',labelbottom='off',labelleft='off',labelright='off')

pyplot.show()

## Magnitude plot

pyplot.plot(loadMeasurement.frequencies,abs(conversion.stoz(shiftedMeasurement.s11Values,50.0)),'k-',label='Electrical delay')
pyplot.plot(loadMeasurement.frequencies,abs(conversion.stoz(loadShortRealGamma,50.0)),'k--',label='SOL calibration')
pyplot.plot(cstDeembed.frequencies,abs(conversion.stoz(cstDeembed.s11Values,50.0)),'k:',label='CST de-embedded + %.1f ps' % (-cstOffset/1e-12))

# pyplot.plot(loadMeasurement.frequencies,abs(conversion.stoz(loadRealGamma,50.0)),     label='$\{0\Omega,50\Omega+0.64\mathrm{nH}+0.1\mathrm{pF},\infty\Omega\}$')    
# pyplot.plot(loadMeasurement.frequencies,abs(conversion.stoz(realGamma,50.0)),         label='$\{0\Omega,50\Omega,\infty\Omega\}$')        
pyplot.xlim(50e6,20e9)
pyplot.ylim(.01,1e4)

# pyplot.grid()
pyplot.xscale('symlog')
pyplot.yscale('symlog')
pyplot.xlabel('Frequency (Hz)')
pyplot.ylabel('$|Z|$ ($\Omega$)')
paperStyleGraph()

pyplot.legend()
pyplot.show()


## Phase plot

pyplot.plot(loadMeasurement.frequencies,numpy.rad2deg(numpy.angle(conversion.stoz(shiftedMeasurement.s11Values,50.0))),'k-',label='Electrical delay')
pyplot.plot(loadMeasurement.frequencies,numpy.rad2deg(numpy.angle(conversion.stoz(loadShortRealGamma,50.0))),'k--',label='SOL calibration')
pyplot.plot(cstDeembed.frequencies,numpy.rad2deg(numpy.angle(conversion.stoz(cstDeembed.s11Values,50.0))),'k:',label='CST de-embedded + %.1f ps' % (-cstOffset/1e-12))
# pyplot.plot(loadMeasurement.frequencies,numpy.rad2deg(numpy.angle(conversion.stoz(loadRealGamma,50.0))),     label='$\{0\Omega,50\Omega+0.64\mathrm{nH}+0.1\mathrm{pF},\infty\Omega\}$')    
# pyplot.plot(loadMeasurement.frequencies,numpy.rad2deg(numpy.angle(conversion.stoz(realGamma,50.0))),         label='$\{0\Omega,50\Omega,\infty\Omega\}$')        
pyplot.grid()
pyplot.xscale('symlog')
pyplot.yticks([-180,-90,0,90,180])
pyplot.xlabel('Frequency (Hz)')
pyplot.ylabel('$\\angle Z$ ($^{\\circ}$)')

pyplot.xlim(50e6,20e9)
pyplot.ylim(-120,+120)
paperStyleGraph()

pyplot.legend(loc='upper left')
pyplot.show()

    
# ## Show transformation
# 
# 
# from utility.efloat import EFloat
# 
# # adapter = idealAdapter
# # adapter = loadAdapter
# adapter = loadShortOpenAdapter
# 
# frequencyEnumerator = enumerate(adapter.frequencies)
# for i in range(180):
#     frequencyEnumerator.next()
# 
# for frequencyNumber,frequency in frequencyEnumerator:
#     def deEmbedAtCurrentFrequency(S):
#         return adapter.deEmbedOne(S,frequencyNumber)
# 
#     def drawDeEmbeddedBoth(dutMeasurement,markerColor='blue'):
#         # draw all measurements, de-embedded for that frequency in red
#         drawSParameter(dutMeasurement.s11Values,sTransform=deEmbedAtCurrentFrequency,chartColor='red',lineWidth=2)
# 
#         # draw all measurements, de-embedded for their proper frequencies until this frequency in black
#         deEmbeddedGamma = adapter.deEmbed(dutMeasurement)
#         deEmbeddedGammaTrace = deEmbeddedGamma[:frequencyNumber] # excluding the current point
#         currentDeEmbeddedGamma = deEmbeddedGamma[frequencyNumber] # the current point
#         drawSParameter(deEmbeddedGammaTrace,lineWidth=2)
# 
#         # draw the current point with a marker or something
#         ax1 = plb.gca()
#         ax1.add_patch(matplotlib.patches.Ellipse([currentDeEmbeddedGamma.real,currentDeEmbeddedGamma.imag],.05,.05,ec=markerColor,fc=markerColor))
# 
#     drawDeEmbeddedBoth(s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_shortA.s1p',delay=electricalDelay),markerColor='red')
#     drawDeEmbeddedBoth(s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_loadA.s1p',delay=electricalDelay),markerColor='red')
#     drawDeEmbeddedBoth(s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_open.s1p',delay=electricalDelay),markerColor='red')
# #    drawDeEmbeddedBoth(s1pFile('../../../../ADS/Fixture_tests_prj/misc/eco35Cal_1pFC.s1p',delay=electricalDelay),markerColor='blue')
# 
# 
#     # show axes
#     smith(chartColor='red',sTransform=deEmbedAtCurrentFrequency)
#     smith()
#     pyplot.title('1 pF (ideal standard), '+str(EFloat(frequency))+'Hz')
#         
#     fileName = str('temp/Ideal1pF%03d' % frequencyNumber) + '.png'
#     pyplot.savefig(fileName, dpi=100)
#     pyplot.clf()
#     print fileName
#     
#     
# #pylab.show()
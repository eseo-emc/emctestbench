import skrf
import numpy

frequencyList = numpy.array([1e9])
def makeStandard(name,coefficient):
    assert coefficient.ndim == 2
    standard = skrf.Network(name=name)
    standard.f = frequencyList
    standard.s = numpy.array([coefficient]).repeat(len(standard.f),0)
    return standard
    
ideals = [  makeStandard('open' ,numpy.array( [[+1.,+0.],[+0.,+1.]] )),
            makeStandard('load' ,numpy.array( [[+0.,+0.],[+0.,+0.]] )),
            makeStandard('short',numpy.array( [[-1.,+0.],[+0.,-1.]] )),
            makeStandard('thru' ,numpy.array( [[+0.,+1.],[+1.,+0.]] ))]
            
calibration = skrf.Calibration(ideals,ideals)
calibration.run()

dut = ideals[3]
dutCalibrated = calibration.apply_cal(dut)
print dutCalibrated.s
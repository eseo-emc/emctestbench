from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy
import tables

## read file
fileName = 'D1C-diff-50Ohm-500MHz'
nfsFile = tables.openFile(fileName+'.h5',mode = 'r')

xGrid = nfsFile.getNode(nfsFile.root,'xCoords')
yGrid = nfsFile.getNode(nfsFile.root,'yCoords')
complexVoltagesGrid = nfsFile.getNode(nfsFile.root,'voltage')

## create simple XML
samplesList = ''
for (xCoordinate,yCoordinate,complexVoltage) in zip(numpy.array(xGrid).flat,numpy.array(yGrid).flat,numpy.array(complexVoltagesGrid).flat):
    samplesList += '{x:.6f} {y:.6f} 0.0 {realVoltage:.6e} {imaginaryVoltage:.6e}\n'.format(x=xCoordinate,y=yCoordinate,realVoltage=complexVoltage.real,imaginaryVoltage=complexVoltage.imag) 
xmlText = '''<?xml version="1.0" encoding="UTF-8"?>
<EmissionScan>
  <Nfs_ver>0.4</Nfs_ver>
  <Filename>'''+fileName+'''</Filename>
  <File_ver>1.0</File_ver>
  <Date>24 avr. 2014</Date>
  <Source>ESEO-EMC</Source>
  <Disclaimer>This file saves result of near field measurement. Others using is not guaranteed.</Disclaimer>
  <Copyright>This document is the property of ESEO</Copyright>
  <Notes>Built by EMC TestBench</Notes>
  <Probe>
    <Name>no_probe</Name>
    <Field>Hz</Field>
    <Frequencies>
      <Unit>MHz</Unit>
      <List>0.00001 100000</List>
    </Frequencies>
    <Perf_factor>
      <Unit>ohm.m</Unit>
      <List>0 0</List>
    </Perf_factor>
  </Probe>
  <Data>
    <Coordinates>xyz</Coordinates>
    <X0>0.0</X0>
    <Y0>0.0</Y0>
    <Z0>0.3</Z0>
    <Frequencies>
      <Unit>MHz</Unit>
      <List>500.0</List>
    </Frequencies>
    <Measurement>
      <Unit>v</Unit>
      <Unit_x>m</Unit_x>
      <Unit_y>m</Unit_y>
      <Unit_z>m</Unit_z>
      <Format>ri</Format>
      <List>'''+samplesList+'''</List>
    </Measurement>
  </Data>
</EmissionScan>
'''

## writout
fileHandle = open(fileName+'.xml','w')
fileHandle.write(xmlText)
fileHandle.close()
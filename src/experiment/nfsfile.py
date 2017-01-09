import os
import shutil
import zipfile
import numpy

from utility.quantities import Position
from probecalibration import ProbeCalibration

class DutImage(object):
    imagesFolder = 'D:/measurements/NFSE-in-Photo'
    
    def __init__(self,sourceFileName,dimensions,anchorPosition):
        self.fileNameAndExtension = sourceFileName
        self.sourcePath = self.imagesFolder+'/'+self.fileNameAndExtension
        self.dimensions = dimensions
        self.anchorPosition = anchorPosition
    def nfsXml(self,fileName=None):
        return '''<Image>
      <Path>'''+self.fileNameAndExtension+'''</Path>
      <Unit>m</Unit>
      <Xoffset>'''+str(-self.anchorPosition[0].asUnit('m'))+'''</Xoffset>
      <Yoffset>'''+str(+self.anchorPosition[1].asUnit('m'))+'''</Yoffset>
      <Zoffset>0</Zoffset>
      <Xsize>'''+str(+self.dimensions[0].asUnit('m'))+'''</Xsize>
      <Ysize>'''+str(+self.dimensions[1].asUnit('m'))+'''</Ysize>
    </Image>'''
    def copyTo(self,folder,name):
        (_,extension) = os.path.splitext(self.sourcePath)
        self.fileNameAndExtension = name+extension
        shutil.copy(self.sourcePath,
                    folder+'/'+self.fileNameAndExtension)
    
dutImages = {
    'D1A': DutImage('D1A.png',Position([120,78],'mm'),Position([30.36,38.07],'mm')), 
    'D1B': DutImage('D1B.png',Position([120,78],'mm'),Position([27.34,35.54],'mm')),
    'D1C': DutImage('D1C.png',Position([120,78],'mm'),Position([15.15,30.45],'mm')),
    'D1D': DutImage('D1D.png',Position([120,78],'mm'),Position([32.38,30.93],'mm')),
    'D2': DutImage('D2.png',Position([127,127],'mm'),Position([12.5,60],'mm')),
    'D3_F6151': DutImage('D3-F6151.png',Position([277,182],'mm'),Position([77,95],'mm')),
    'D3_FAQ15': DutImage('D3-FAQ15.png',Position([277,182],'mm'),Position([77,95],'mm')),
    'D4': DutImage('D4.png',Position([205.6,71],'mm'),Position([102.8,48],'mm')),
    'Patch2GHz': DutImage('Patch2GHz.png',Position([100,100],'mm'),Position([33,33],'mm')),
    'Patch2GHzOrEcran': DutImage('Patch2GHzOrienteEcran.png',Position([100,100],'mm'),Position([33,33],'mm')),
    'Piste20cm':DutImage('Piste20cm.png',Position([194,100],'mm'),Position([10,10],'mm')),
    'TMC01':DutImage('TMC01.png',Position([126,57],'mm'),Position([20,33],'mm')),
    'CarteTransfoIntegre_V1':DutImage('CarteTransfoIntegre_V1.png',Position([200,140],'mm'),Position([200-25,140-35],'mm')),
    'CarteTransfoBobine':DutImage('CarteTransfoBobine.png',Position([120,110],'mm'),Position([120-12,68],'mm')),
    'CarteTransfoDeporte':DutImage('CarteTransfoDeporte.png',Position([133,160],'mm'),Position([133-23,70],'mm')),
}



#%% export XML newstyle

class NfsFile(object):
    def __init__(self,resultFolder,fileName,imageName,frequencies,calibration):
        self._fileName = fileName
        self._frequencies = frequencies
        self._calibration = calibration
        self._resultFolder = resultFolder
        self._imageName = imageName
        
        
    def __enter__(self):
        self._archiveFolder = self._resultFolder + '/' + self._fileName
        os.mkdir(self._archiveFolder)        
        
        self._image = dutImages[self._imageName]
        self._image.copyTo(self._archiveFolder,self._fileName)
        
        self._xmlFileHandle = open(self._archiveFolder + '/' + self._fileName+'.xml','w')
        self._dataFileHandle = open(self._archiveFolder + '/' + self._fileName+'.dat','w')
        
        self._writeXml()
        return self
        
    def __exit__(self,*args,**kwargs):
        print "Exiting",args,kwargs
        self._dataFileHandle.close()
        
        print 'Zipping...'
        zipFileHandle = zipfile.ZipFile(self._resultFolder+'/'+self._fileName +'.nfs', 'w')
        for fileName in os.listdir(self._archiveFolder):
            zipFileHandle.write(os.path.join(self._archiveFolder, fileName),arcname=fileName)
        zipFileHandle.close() 
        print 'Finished write out!'
        
    def _writeXml(self):
        self._xmlFileHandle.write('''<?xml version="1.0" encoding="UTF-8"?>
<EmissionScan>
  <Nfs_ver>0.4</Nfs_ver>
  <Filename>'''+self._fileName+'''</Filename>
  <File_ver>1.0</File_ver>
  <Date>24 avr. 2014</Date>
  <Source>ESEO-EMC</Source>
  <Disclaimer>This file saves result of near field measurement. Others using is not guaranteed.</Disclaimer>
  <Copyright>This document is the property of ESEO</Copyright>
  <Notes>Built by EMC TestBench</Notes>
'''+self._calibration.nfsXml()+'''
  <Component>
    <Name>'''+self._fileName+'''</Name>
    '''+self._image.nfsXml()+'''
  </Component>
  <Data>
    <Coordinates>xyz</Coordinates>
    <X0>0</X0>
    <Y0>0</Y0>
    <Z0>0</Z0>
    <Frequencies>
      <Unit>Hz</Unit>
      <List>''' + ' '.join(map(str,self._frequencies.tolist())) + '''</List>
    </Frequencies>
    <Measurement>
      <Unit>v</Unit>
      <Unit_x>m</Unit_x>
      <Unit_y>m</Unit_y>
      <Unit_z>m</Unit_z>
      <Format>ri</Format>
      <Data_files>'''+self._fileName+'''.dat</Data_files>
    </Measurement>
  </Data>
</EmissionScan>
''')
        self._xmlFileHandle.close()
        
    def writePoint(self,position,complexVoltages):
        self._dataFileHandle.write('{position[0]:.6f} {position[1]:.6f} {position[2]:.6f}'.format(position=position.asUnit('m')))
        complexVoltageArray = numpy.array(complexVoltages)
        for (realVoltage,imaginaryVoltage) in zip(complexVoltageArray.real.flat,complexVoltageArray.imag.flat):
            self._dataFileHandle.write(' {realVoltage:.6e} {imaginaryVoltage:.6e}'.format(realVoltage=realVoltage,imaginaryVoltage=imaginaryVoltage))
        self._dataFileHandle.write('\n')

    def writePoints(self,xGrid,yGrid,zCoordinate,complexVoltagesGrid):
        for (xCoordinate,yCoordinate,complexVoltage) in zip(xGrid.flat,yGrid.flat,complexVoltagesGrid.reshape(xGrid.size,self._frequencies.size).tolist()):
            position = Position(numpy.array([xCoordinate,yCoordinate,zCoordinate]),'m')            
            self.writePoint(position,complexVoltage)
            
if __name__ == '__main__':            
    import numpy
    frequencies = numpy.arange(1000000,10000000,1000000)
    (xGrid, yGrid) = numpy.meshgrid(numpy.arange(0,5.0,1)/1000,numpy.arange(0,4.0,1)/1000,indexing='ij')
    zPosition = 5.0/1000
    complexVoltagesGrid = numpy.random.random((5,4,9))
    
    calibration = ProbeCalibration.fromFile('Hy-5mm.xml')
    
    with NfsFile('Z:/Measurements/NFSE-in','D2-Hy-newstyle10',imageName='D2',calibration=calibration.electrical,frequencies=frequencies) as nfsFile:
        nfsFile.writePoints(xGrid,
                            yGrid,
                            zPosition,
                            complexVoltagesGrid)

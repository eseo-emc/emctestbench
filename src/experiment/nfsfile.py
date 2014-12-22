import os
import shutil
import zipfile
import numpy

from utility.quantities import Position
from probecalibration import ProbeCalibration

class DutImage(object):
    imagesFolder = 'Z:/measurements/NFSE-in'
    
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
    'D3-F6151': DutImage('D3-F6151.png',Position([120,78],'mm'),Position([0,0],'mm')),
    'D3-FAQ15': DutImage('D3-FAQ15.png',Position([120,78],'mm'),Position([0,0],'mm')),
    'D4': DutImage('D4.png',Position([120,78],'mm'),Position([0,0],'mm'))
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
#        self._xmlFileHandle.write('''<?xml version="1.0" encoding="utf-8"?>
#<EmissionScan>
#  <Nfs_ver>0.4</Nfs_ver>
#  <Filename>D2-Hy-newstyle8</Filename>
#  <Groupname>D2-Hy-newstyle8</Groupname>
#  <File_ver>1.0</File_ver>
#  <Date>24 avr. 2014</Date>
#  <Source>ESEO-EMC</Source>
#  <Disclaimer>This file saves result of near field measurement. Others using is not guaranteed.</Disclaimer>
#  <Copyright>This document is the property of ESEO</Copyright>
#  <Notes>Built by EMC TestBench</Notes>
#  <Document />
#  <Component>
#    <Notes></Notes>
#    <Documentation></Documentation>
#    <Name>D2-Hy-newstyle8</Name>
#    <Manufacturer></Manufacturer>
#    <Status></Status>
#    <Image>
#      <Path>D2-Hy-newstyle8.png</Path>
#      <Unit>mm</Unit>
#      <Xsize>127</Xsize>
#      <Ysize>127</Ysize>
#      <Xoffset>-12.5</Xoffset>
#      <Yoffset>60</Yoffset>
#      <Zoffset>0</Zoffset>
#    </Image>
#  </Component>
#  <Setup>
#    <Notes></Notes>
#    <Documentation></Documentation>
#    <Config>
#      <Probe_signal></Probe_signal>
#      <Att></Att>
#      <Average></Average>
#      <Ref_level></Ref_level>
#      <Rbw></Rbw>
#      <Vbw></Vbw>
#      <Swp></Swp>
#      <Tps></Tps>
#      <Detector></Detector>
#      <Preamp></Preamp>
#      <Preselector></Preselector>
#      <Xdiv></Xdiv>
#      <Ydiv></Ydiv>
#      <Bw></Bw>
#      <Coupling></Coupling>
#    </Config>
#    <Transducer>
#      <Format>m</Format>
#      <Frequencies>
#        <Unit>Hz</Unit>
#        <List></List>
#      </Frequencies>
#      <Gain></Gain>
#    </Transducer>
#  </Setup>
#  <Probe>
#    <Notes></Notes>
#    <Documentation></Documentation>
#    <Name>Hyprobe</Name>
#    <Field>Hy</Field>
#    <Frequencies>
#      <Unit>MHz</Unit>
#      <List>0.3 15.2985 30.297 45.2955 60.294 75.2925 90.291 105.2895 120.288 135.2865 150.285 165.2835 180.282 195.2805 210.279 225.2775 240.276 255.2745 270.273 285.2715 300.27 315.2685 330.267 345.2655 360.264 375.2625 390.261 405.2595 420.258 435.2565 450.255 465.2535 480.252 495.2505 510.249 525.2475 540.246 555.2445 570.243 585.2415 600.24 615.2385 630.237 645.2355 660.234 675.2325 690.231 705.2295 720.228 735.2265 750.225 765.2235 780.222 795.2205 810.219 825.2175 840.216 855.2145 870.213 885.2115 900.21 915.2085 930.207 945.2055 960.204 975.2025 990.201 1005.1995 1020.198 1035.1965 1050.195 1065.1935 1080.192 1095.1905 1110.189 1125.1875 1140.186 1155.1845 1170.183 1185.1815 1200.18 1215.1785 1230.177 1245.1755 1260.174 1275.1725 1290.171 1305.1695 1320.168 1335.1665 1350.165 1365.1635 1380.162 1395.1605 1410.159 1425.1575 1440.156 1455.1545 1470.153 1485.1515 1500.15 1515.1485 1530.147 1545.1455 1560.144 1575.1425 1590.141 1605.1395 1620.138 1635.1365 1650.135 1665.1335 1680.132 1695.1305 1710.129 1725.1275 1740.126 1755.1245 1770.123 1785.1215 1800.12 1815.1185 1830.117 1845.1155 1860.114 1875.1125 1890.111 1905.1095 1920.108 1935.1065 1950.105 1965.1035 1980.102 1995.1005 2010.099 2025.0975 2040.096 2055.0945 2070.093 2085.0915 2100.09 2115.0885 2130.087 2145.0855 2160.084 2175.0825 2190.081 2205.0795 2220.078 2235.0765 2250.075 2265.0735 2280.072 2295.0705 2310.069 2325.0675 2340.066 2355.0645 2370.063 2385.0615 2400.06 2415.0585 2430.057 2445.0555 2460.054 2475.0525 2490.051 2505.0495 2520.048 2535.0465 2550.045 2565.0435 2580.042 2595.0405 2610.039 2625.0375 2640.036 2655.0345 2670.033 2685.0315 2700.03 2715.0285 2730.027 2745.0255 2760.024 2775.0225 2790.021 2805.0195 2820.018 2835.0165 2850.015 2865.0135 2880.012 2895.0105 2910.009 2925.0075 2940.006 2955.0045 2970.003 2985.0015 3000.0 </List>
#    </Frequencies>
#    <Perf_factor>
#      <Unit_a>m</Unit_a>
#      <Unit>ohm.m</Unit>
#      <Format>m</Format>
#      <List>-47.22291 -36.81583 -27.15343 -26.70613 -30.82966 -26.96922 -18.42679 -14.51388 -11.66891 -10.10094 -8.543244 -7.365313 -6.157361 -5.009314 -4.335181 -3.543164 -3.279802 -3.269331 -3.345142 -2.756687 -2.060873 -1.339744 -0.8925339 -0.6210214 -0.6313764 -0.5721167 -0.6646136 -0.6623498 -0.6689209 -2.81704 -0.8876022 -0.8161821 -0.7802228 -0.7268221 -0.7387837 -0.703823 -1.021601 -0.8663794 -0.5705768 -0.34178 0.1078458 0.4017838 0.6155455 0.8411914 1.462156 2.013541 2.870493 3.307126 3.904087 4.564833 5.254639 5.868823 6.473434 6.982129 7.398268 7.85168 7.952662 7.85403 7.705787 7.565408 7.391656 7.244075 7.003828 6.654795 6.260818 5.910054 5.397872 5.060801 4.767676 4.520994 4.475716 4.464652 4.499343 4.499611 4.602229 4.764255 4.887273 5.003778 5.156126 5.390232 5.701611 5.903752 6.36552 6.751862 7.297046 7.743072 8.393477 9.116855 9.8886 10.71493 11.60346 12.287 12.70703 12.82879 12.60096 12.00905 11.13294 10.30033 9.813844 9.390891 9.144882 8.957838 8.660512 8.42608 8.029276 7.713839 7.477115 7.295868 7.078235 6.967169 6.904899 6.804551 6.837588 6.843355 7.018477 7.140327 7.405774 7.770018 8.346708 8.027099 8.40526 8.816681 9.344888 9.837356 10.35479 10.85697 11.48935 12.23858 12.87436 13.55082 14.08646 14.50741 14.77934 14.46771 13.56689 12.5601 11.56456 10.88473 10.3099 9.640242 9.480433 9.055592 8.788201 8.561295 8.362631 8.301269 8.206689 8.166498 7.983224 8.003785 8.005633 8.103358 8.270311 8.404108 8.54741 8.739002 9.0442 9.445526 9.993938 10.47958 11.0589 11.48754 12.10975 12.80339 13.41458 13.99734 14.52687 14.9332 15.20852 15.30278 15.32006 15.06245 14.59695 13.99958 13.0949 12.24064 11.56917 10.79802 10.30241 9.930281 9.63306 9.360388 9.300864 9.159076 9.102102 9.160172 9.210233 9.368157 9.441956 9.581678 9.835468 9.931129 10.34999 10.50793 10.85002 11.11958 11.41666 11.77601 12.11203 12.62775 12.96615 </List>
#    </Perf_factor>
#  </Probe>
#  <Data>
#    <Notes></Notes>
#    <Documentation></Documentation>
#    <Coordinates>xyz</Coordinates>
#    <X0>0 mm</X0>
#    <Y0>0 mm</Y0>
#    <Z0>0 mm</Z0>
#    <Frequencies>
#      <Unit>Hz</Unit>
#      <List>1000000 2000000 3000000 4000000 5000000 6000000 7000000 8000000 9000000 </List>
#    </Frequencies>
#    <Measurement>
#      <Format>ri</Format>
#      <Unit>v</Unit>
#      <Unit_x>mm</Unit_x>
#      <Unit_y>mm</Unit_y>
#      <Unit_z>mm</Unit_z>
#      <Vx_x>1000</Vx_x>
#      <Vx_y>0</Vx_y>
#      <Vx_z>0</Vx_z>
#      <Vy_x>0</Vy_x>
#      <Vy_y>1000</Vy_y>
#      <Vy_z>0</Vy_z>
#      <Vz_x>-0</Vz_x>
#      <Vz_y>-0</Vz_y>
#      <Vz_z>1000.00006</Vz_z>
#      <Data_files>00_D2-Hy-newstyle80.dat</Data_files>
#    </Measurement>
#  </Data>
#</EmissionScan>''')


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

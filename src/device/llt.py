# -*- coding: utf-8 -*-
"""
Attempt to a Pythonic bridge to the scanCONTROL LLT.dll. Function names are 
preserved wherever possible, in camelCaps starting with a lower case. Some 
functions are made loosely private with the _ prefix. Arguments can be passed 
without length, errors are translated into Exceptions.

@author: Sjoerd Op 't Land <sjoerd.optland@eseo.fr>
"""
from ctypes import windll
import ctypes
import warnings
import numpy
import time

from llt_scanControlDataTypes import *

stringBufferSize = 200
dummyValue = 42

llt = windll.LoadLibrary("C:/Program Files (x86)/scanCONTROL Configuration Tools 4.1/LLT.dll")

def raiseIfError(unprotectedFunction):
#    print 'Wrapping...'
    def protectedFunction(self,*args,**kwargs):
#        print 'Protecting...'
        returnValue = unprotectedFunction(self,*args,**kwargs)
        if returnValue < 0:
            errorString = self._translateErrorValue(returnValue)
            raise Exception('Error {value:d}: {string:s}'.format(value=returnValue,string=errorString))
        else:
            return returnValue
    return protectedFunction


class Llt(object):
    def __init__(self,interfaceType):
        self._pLLT = llt.s_CreateLLTDevice(interfaceType)
        if self._pLLT == 0 or self._pLLT == 0xffffffff:
            raise Exception('Device creation has failed')
    def __enter__(self):
        pass
    def __exit__(self,type,value,traceback):
        self.close()    
    
    def _translateErrorValue(self, errorValue):
        stringBuffer =ctypes.create_string_buffer(stringBufferSize)
        
        lengthOrError = llt.s_TranslateErrorValue(self._pLLT, errorValue, stringBuffer, stringBuffer._length_)       
        if lengthOrError < 0:
            if lengthOrError == ERROR_TRANSERRORVALUE_WRONG_ERROR_VALUE:
                raise ValueError('Unknown error value {0:d}'.format(errorValue))
            elif lengthOrError == ERROR_TRANSERRORVALUE_BUFFER_SIZE_TOO_LOW:
                raise MemoryError('Buffer size {0:d} too low'.format(stringBufferSize))
            else:
                raise Exception('Error {0:d} while translating error value {1:d}'.format(lengthOrError,errorValue))
        else:
            return stringBuffer.value
    
    def getDeviceInterfaces(self,fast=False):
        #TODO: generalise to more devices
        #numberOfInterfaces = 10
        interfaceList = ctypes.c_int(42)# *numberOfInterfaces
        if fast:
            self._GetDeviceInterfacesFast(ctypes.pointer(interfaceList),1)            
        else:
            self._GetDeviceInterfaces(ctypes.pointer(interfaceList),1)
        return interfaceList.value
    def setDeviceInterface(self,interfaceNumber,additionalParameter=0):
        self._SetDeviceInterface(interfaceNumber,additionalParameter)
    def connect(self):
        self._Connect()
    def close(self):
        print 'Closing'
        self._Disconnect()
        self._DelDevice()
    def getDeviceName(self):
        nameBuffer = ctypes.create_string_buffer(stringBufferSize)
        vendorBuffer = ctypes.create_string_buffer(stringBufferSize)
        self._GetDeviceName(nameBuffer,nameBuffer._length_,vendorBuffer,vendorBuffer._length_)
        return {'name':nameBuffer.value,'vendor':vendorBuffer.value}
    def transferProfiles(self,mode,enable=True):
        return self._TransferProfiles(mode,(1 if enable else 0))
    def multiShot(self,numberOfShots=1):
        self._MultiShot(numberOfShots)
        
    @property
    def profileConfiguration(self):
        profileConfiguration = ctypes.c_int(dummyValue)
        self._GetProfileConfig(ctypes.byref(profileConfiguration))
        return profileConfiguration.value    
    @profileConfiguration.setter
    def profileConfiguration(self,newValue):
        self._SetProfileConfig(newValue)
    
    def actualProfile(self):
        return self._convertProfileToValues(self._getActualProfile())
    
    def _getActualProfile(self,warnForLostProfiles=False):
        if self.profileConfiguration == PURE_PROFILE:
            bufferSize = self.resolution*4+16
        elif self.profileConfiguration == PROFILE:
            bufferSize = self.resolution*64
        else:
            raise ValueError('Profile Configuration {0:d} unhandled in getActualProfile'.format(self.profileConfiguration))
        
        profileBuffer = ctypes.create_string_buffer(bufferSize)
        lostProfilesBuffer = ctypes.c_int(dummyValue)
        bytesWritten = self._GetActualProfile(profileBuffer,ctypes.c_uint(profileBuffer._length_),self.profileConfiguration,ctypes.byref(lostProfilesBuffer))
        if bytesWritten != bufferSize:
            raise Exception('{bytesWritten:d} bytes were written by GetActualProfile into a {bufferSize:d} bytes buffer'.format(bytesWritten=bytesWritten,bufferSize=bufferSize))
        lostProfiles = lostProfilesBuffer.value
        if warnForLostProfiles and lostProfiles > 0:
            warnings.warn('Lost {0:d} profiles before getActualProfile call'.format(lostProfiles))
        return profileBuffer.raw[:bytesWritten]
    def _convertProfileToValues(self,profile,stripe=0):
        convertToMm = 1
#        xBuffer = (ctypes.c_double*self.resolution)(dummyValue)
        xBuffer = numpy.zeros((self.resolution,),dtype=ctypes.c_double)
        zBuffer = numpy.zeros((self.resolution,),dtype=ctypes.c_double)
        thresholdBuffer = numpy.zeros((self.resolution,),dtype=ctypes.c_ushort)
        m0Buffer = numpy.zeros((self.resolution,),dtype=ctypes.c_uint)        
        
        wroteArrays = self._ConvertProfile2Values(profile,
                                    self.resolution,
                                    self.profileConfiguration,
                                    self.scannerType,
                                    stripe,
                                    convertToMm,
                                    0,
                                    0,
                                    thresholdBuffer.ctypes.data_as(ctypes.POINTER(ctypes.c_ushort)),
                                    xBuffer.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                                    zBuffer.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                                    m0Buffer.ctypes.data_as(ctypes.POINTER(ctypes.c_uint)),
                                    0)
        return {'x':xBuffer,'z':zBuffer,'threshold':thresholdBuffer,'m0':m0Buffer}
    @property
    def holdBuffersForPolling(self):
        countBuffer = ctypes.c_int(dummyValue)
        self._GetHoldBuffersForPolling(ctypes.byref(countBuffer))
        return countBuffer.value
    @holdBuffersForPolling.setter
    def holdBuffersForPolling(self,value):
        self._SetHoldBuffersForPolling(value)
    @property
    def bufferCount(self):
        countBuffer = ctypes.c_int(dummyValue)
        self._GetBufferCount(ctypes.byref(countBuffer))
        return countBuffer.value
    @bufferCount.setter
    def bufferCount(self,value):
        self._SetBufferCount(value)
        
    @property
    def resolution(self):
        resolutionBuffer = ctypes.c_uint32(dummyValue)
        self._GetResolution(ctypes.byref(resolutionBuffer))
        return resolutionBuffer.value
    @resolution.setter
    def resolution(self,value):
        self._SetResolution(value)
    
    def getFeature(self,featureName):
        return eval('self._getFeature(FEATURE_FUNCTION_'+featureName+')')
    def _getFeature(self,feature):
        featureValueBuffer = ctypes.c_uint32(dummyValue)
        self._GetFeature(feature,ctypes.byref(featureValueBuffer))
        return featureValueBuffer.value
        
    def setFeature(self,featureName,newValue):
        eval('self._setFeature(FEATURE_FUNCTION_'+featureName+',newValue)')
    def _setFeature(self,feature,newValue):
        self._SetFeature(feature,newValue)
    
    def inquireFeature(self,featureName):
        metaData = eval('self._getFeature(INQUIRY_FUNCTION_'+featureName+')')
        return {'maxValue' : (metaData & 0x00000fff),
                'minValue' : (metaData & 0x00fff000)>>12,
                'autoMode' : bool((metaData & 0x02000000) >> 25),
                'available' : bool((metaData & 0x80000000) >> 31)}

    def _featureString(self,featureName):
        metadata = self.inquireFeature(featureName)
        metadata.update({'value':self.getFeature(featureName)})
        return '{featureName:25}: Available={metadata[available]:1}  Auto={metadata[autoMode]:1}  Value={metadata[value]:9} ({metadata[minValue]}-{metadata[maxValue]})'.format(metadata=metadata,featureName=featureName)
    def printFeatures(self):
        for feature in ['LASERPOWER',                          
                        'MEASURINGFIELD',               
                        'TRIGGER',                                
                        'SHUTTERTIME',                       
                        'IDLETIME',                             
                        'PROCESSING_PROFILEDATA',   
                        'THRESHOLD',                            
                        'MAINTENANCEFUNCTIONS',     
                        'CMMTRIGGER',                         
                        'REARRANGEMENT_PROFILE',    
                        'PROFILE_FILTER',                  
                        'RS422_INTERFACE_FUNCTION']:
            print self._featureString(feature)
    
#        'ANALOGFREQUENCY',              
#                        'ANALOGOUTPUTMODES',  
    def configureRight(self):
        self.setFeature('TRIGGER',0)
        self.setFeature('SHUTTERTIME',16777316)
        self.setFeature('IDLETIME',3900)
        self.setFeature('PROCESSING_PROFILEDATA',111)
        self.setFeature('THRESHOLD',16780416)
        self.setFeature('MAINTENANCEFUNCTIONS',2)
        self.setFeature('REARRANGEMENT_PROFILE',2149096449)
        self.setFeature('PROFILE_FILTER',0)
 
    @property
    def laserOn(self):
        return self.getFeature('LASERPOWER') != 0
    @laserOn.setter
    def laserOn(self,newValue):
        if newValue:
            self.setFeature('LASERPOWER',2)
        else:
            self.setFeature('LASERPOWER',0)
 
    @property
    def scannerType(self):
        typeBuffer = ctypes.c_uint32(dummyValue)
        self._GetLLTType(ctypes.byref(typeBuffer))
        return typeBuffer.value
        
    @raiseIfError
    def _GetDeviceInterfaces(self,*args):
        return llt.s_GetDeviceInterfaces(self._pLLT,*args)
    @raiseIfError
    def _GetDeviceInterfacesFast(self,*args):
        return llt.s_GetDeviceInterfacesFast(self._pLLT,*args)
    @raiseIfError
    def _SetDeviceInterface(self,*args):
        return llt.s_SetDeviceInterface(self._pLLT,*args)
    @raiseIfError
    def _Connect(self,*args):
        return llt.s_Connect(self._pLLT,*args)
    @raiseIfError
    def _Disconnect(self,*args):
        return llt.s_Disconnect(self._pLLT,*args)
    @raiseIfError    
    def _DelDevice(self):
        return llt.s_DelDevice(self._pLLT)
    @raiseIfError
    def _GetDeviceName(self,*args):
        return llt.s_GetDeviceName(self._pLLT,*args)
    @raiseIfError
    def _TransferProfiles(self,*args):
        return llt.s_TransferProfiles(self._pLLT,*args)
    @raiseIfError
    def _SetProfileConfig(self,*args):
        return llt.s_SetProfileConfig(self._pLLT,*args)
    @raiseIfError
    def _GetProfileConfig(self,*args):
        return llt.s_GetProfileConfig(self._pLLT,*args)    
    @raiseIfError
    def _GetActualProfile(self,*args):
        return llt.s_GetActualProfile(self._pLLT,*args)
    @raiseIfError
    def _ConvertProfile2Values(self,*args):
        return llt.s_ConvertProfile2Values(self._pLLT,*args)
    @raiseIfError
    def _MultiShot(self,*args):
        return llt.s_MultiShot(self._pLLT,*args)
    @raiseIfError
    def _GetResolution(self,*args):
        return llt.s_GetResolution(self._pLLT,*args)
    @raiseIfError
    def _SetResolution(self,*args):
        return llt.s_SetResolution(self._pLLT,*args)
    @raiseIfError
    def _GetHoldBuffersForPolling(self,*args):
        return llt.s_GetHoldBuffersForPolling(self._pLLT,*args)
    @raiseIfError
    def _SetHoldBuffersForPolling(self,*args):
        return llt.s_SetHoldBuffersForPolling(self._pLLT,*args)
    @raiseIfError
    def _GetBufferCount(self,*args):
        return llt.s_GetBufferCount(self._pLLT,*args)
    @raiseIfError
    def _SetBufferCount(self,*args):
        return llt.s_SetBufferCount(self._pLLT,*args)        
    @raiseIfError
    def _GetLLTType(self,*args):
        return llt.s_GetLLTType(self._pLLT,*args)
    @raiseIfError
    def _GetFeature(self,*args):
        return llt.s_GetFeature(self._pLLT,*args)
    @raiseIfError
    def _SetFeature(self,*args):
        return llt.s_SetFeature(self._pLLT,*args)        

        
if __name__ == '__main__':
#with Llt(INTF_TYPE_ETHERNET) as interface:
    interface = Llt(INTF_TYPE_ETHERNET)
    interfaceNumber = interface.getDeviceInterfaces(fast=True)
    interface.setDeviceInterface(interfaceNumber)
    interface.connect()
    
    interface.resolution = 640
    interface.profileConfiguration = PROFILE
    
    interface.configureRight()
    
    
    profileSize = interface.transferProfiles(NORMAL_TRANSFER,True)
    time.sleep(0.5)
    startTime = time.clock()
    profile = interface.actualProfile()
    print 'Download took {0:.2e}s'.format(time.clock()-startTime)    
    
    interface.transferProfiles(NORMAL_TRANSFER,False)
    
    
    import pylab
    pylab.axis('equal')
    #    (x_filter,z_filter,m0_filter) = (x[z!=0],z[z!=0],m0[z!=0])
    pylab.plot(profile['x'],profile['z'],'-')
    pylab.show()
    
    interface.printFeatures()
    
    interface.close()
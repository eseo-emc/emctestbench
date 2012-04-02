class SwitchPlatform(object):
    def __init__(self,switches):
        self._switches = switches
    def keys(self):
        return self._switches.keys()
    def __getitem__(self,key):
        return self._switches[key]
    def __iter__(self):
        return self._switches.__iter__()
      
    
    @property
    def iconName(self):
        return 'Switch'
        
class Switch(dict):
    def __init__(self,*args):
        super(Switch,self).__init__(*args)
        assert 'open' in self.keys()
    def setPosition(self,positionName):
        print 'setPosition ' + positionName
#        raise NotImplementedError
    def openSwitch(self):
        self.setPosition('open')
    def _readPosition(self,positionName):
        print '_readPosition ' + positionName
        return False
    def getPosition(self):
        for positionName in ['open'] + self.keys():
            if self._readPosition(positionName):
                return positionName
        else:
            return 'open'
#            raise Exception,'None of the positions {positions} was taken.'.format(positions=str(self.keys()))

if __name__ == '__main__':
    testSwitch = Switch({'a':1,'b':2,'c':3,'open':8})
    testSwitch.getPosition()
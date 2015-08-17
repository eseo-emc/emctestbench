import time

class Amplifier(object):
    @property
    def iconName(self):
        return 'Amplifier'
        
    @property
    def rfOn(self):
        return self.onProxy
    @rfOn.setter
    def rfOn(self,newValue):
        if newValue:
            self._turnRfOn()
            if not(hasattr(self,'onProxy') and self.onProxy):
                time.sleep(4)
        else:
            self._turnRfOff()
        self.onProxy = newValue
        
    def turnRfOn(self):
        raise Exception,'turnRf** deprecated, use new rfOn setter interface'
    def turnRfOff(self):
        raise Exception,'turnRf** deprecated, use new rfOn setter interface'
        
import time

class Amplifier(object):
    @property
    def iconName(self):
        return 'Amplifier'
        
    def turnRfOn(self):
        self._turnRfOn()
        if not(hasattr(self,'onProxy') and self.onProxy):
            time.sleep(4)
        self.onProxy = True
    def turnRfOff(self):
        self._turnRfOff()
        self.onProxy = False
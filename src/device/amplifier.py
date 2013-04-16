class Amplifier(object):
    @property
    def iconName(self):
        return 'Amplifier'
        
    def turnRfOn(self):
        raise NotImplementedError
    def turnRfOff(self):
        raise NotImplementedError
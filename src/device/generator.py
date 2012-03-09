class Generator(object):
    '''
    Abstract superclass for all signal generating devices.
    '''
    @property
    def iconName(self):
        return 'Generator'
        
    def enableOutput(self):
        raise NotImplementedError   
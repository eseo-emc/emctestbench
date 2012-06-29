from generator import Generator
from utility import quantities

class RfGenerator(Generator):
    @property
    def iconName(self):
        return 'RfGenerator'
        
    def tearDown(self):
        self.setPower(quantities.Power(0))
from basicansi import BasicANSI

# Assuming BasicANSI is a base class you've already defined
class AreaChange(BasicANSI):
    def __init__(self, util):
        super().__init__(util)
        self.util = util
        # Initialize other attributes specific to this class if needed


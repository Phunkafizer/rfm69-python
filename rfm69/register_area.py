from collections import OrderedDict

class RegisterArea(object):
    """ Represents a setting spread over multiple consecutive registers
        
        To use:
            - append values to VALUES in your derived __init__
            - add a static BASEREGISTER variable set to base register of value
    """
    
    def pack(self):
        regs = OrderedDict()
        for i, val in enumerate(self.VALUES):
            regs[self.BASEREGISTER + i] = val
        return regs
        
    def set_word(self, word):
        """ Sets complete registerarea using word
        """
        for i in reversed(range(len(self.VALUES))):
            self.VALUES[i] = word & 0xFF
            word >>= 8
        
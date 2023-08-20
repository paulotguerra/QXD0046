from . import MTNTM 

class TM(MTNTM):
    def __init__(self, Q={}, Sigma={}, Gamma={}, delta={}, q0=0, F={}):
        super().__init__(Q,Sigma,Gamma,{x:{delta[x]} for x in delta}, q0, F)

class MT(TM):
    def aceita(self, input_string=0):
        return self.accepts(input_string)
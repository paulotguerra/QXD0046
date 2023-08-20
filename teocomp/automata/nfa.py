from teocomp.automata import PDA

class NFA(PDA):
  def __init__(self, Q={}, Sigma={}, delta={}, q0=0, F={}):
        delta_pda = {(q,a,''):{(r,'') for r in delta[q,a]} for (q,a) in delta}
        super().__init__(Q,Sigma,{},delta_pda,q0,F)

class AFN(NFA):
  def aceita(self,input_string=0):
    return self.accepts(input_string)


from teocomp.automata import NFA

class DFA(NFA):
  def __init__(self, Q={}, Sigma={}, delta={}, q0=0, F={}):
        delta_nfa = {(q,a):{delta[q,a]} for (q,a) in delta}
        super().__init__(Q,Sigma,delta_nfa,q0,F)

class AFD(DFA):
  def aceita(self,input_string=0):
    return self.accepts(input_string)

from ..utils.view import to_graphviz

""" Multitape Nondeterministic Turing Machine """
class MTNTM:
    
    default = {'blank':'\u2294', 'right':'R','left':'L'}    
 
    def __init__(self, Q={}, Sigma={}, Gamma={}, delta={}, q0=0, F={}):
        self.states = Q
        self.inputAlphabet = Sigma
        self.tapeAlphabet = Gamma
        self.transition = delta
        self.startState = q0
        self.acceptStates = F
 
        self.blank_sym = self.default['blank']
        self.left_sym = self.default['left']
        self.right_sym = self.default['right']

        self.keep_traces = False
        self.show_steps = False
        self.ntapes = max([len(t)-1 for t in self.transition]) 

        self._subroutine = {}

        self.reset()

    def where(self, TMs):
        self.subroutines(TMs)
        return self

    def subroutines(self, TMs):
        self._subroutine = {m:TMs[m] for m in TMs if m in self.states}

        for m,M in self._subroutine.items():
            self.states.update({f'{m}_{q}' for q in M.states})
            
            t_in  = [(k,v) for k in self.transition for v in self.transition[k] if v[0] == m]
            for k,v in t_in:
                q0 = M.startState
                self.transition[k].remove(v)
                self.transition[k].add((f'{v[0]}_{q0}',*v[1:]))

            t_out = [k for k in self.transition if k[0] == m]  
            for k in t_out:
                v = self.transition.pop(k)
                for qa in M.acceptStates:
                    self.transition[(f'{k[0]}_{qa}', *k[1:])] = v     

            for k,v in M.transition.items():
                self.transition[(f'{m}_{k[0]}', *k[1:])] = {(f'{m}_{x[0]}', *x[1:]) for x in v} 
            
            if m in self.acceptStates:
                self.acceptStates.remove(m)
                self.acceptStates.update({f'{m}_{q}' for q in M.acceptStates})
            
            if m == self.startState:
                self.startState = f'{m}_{M.startState}'
            
            self.states.discard(m)

    def reset(self, input_string="", pos=0):
        input_list = list(input_string) if input_string else [self.blank_sym]
        input_list = input_list + [self.blank_sym]*(pos+1-len(input_list))
        self.traces = [ [(self.startState, [pos]+[0]*(self.ntapes-1), [input_list] + [[self.blank_sym]]*(self.ntapes-1), False)] ]

    def acceptingTraces(self):
        return [t for t in self.traces if t[-1][-1] == True]

    def result(self):
        return True if self.acceptingTraces() else (False if (not self.traces) else None)

    def step(self):
        if (self.acceptingTraces()):
            return False
        else:
            updated_traces = []
            for trace in self.traces:
                q, head, tape, _ = trace[-1]          

                args = (q,) + tuple([tape[i][h] for i,h in enumerate(head)])

                if (args in self.transition):                                        
                    for values in self.transition[args]:
                        h = head[:]
                        t = [t[:] for t in tape[:]]
                        r = values[0]
                        b = values[1:self.ntapes+1]
                        m = values[self.ntapes+1:]
                        for i in range(self.ntapes):
                            t[i][h[i]] = b[i]
                            h[i] += 1 if m[i] == self.right_sym else -1 if m[i] == self.left_sym else 0
                            # if h[i] < 0: # Permite movimento para a esquerda da posição inicial
                            #     h[i] = 0
                            #     t[i]= [self.blank_sym] + t[i]
                            h[i] = 0 if h[i] < 0 else h[i]
                            t[i] += [self.blank_sym] if h[i] == len(t[i]) else []
                        if (self.keep_traces):
                            updated_traces.append(trace+[(r,h,t,False)])    
                        else:
                            updated_traces.append([(r,h,t,False)])
                elif q in self.acceptStates:
                    updated_traces.append([(q,head[:],tape[:],True)])
            self.traces = updated_traces 
            return self.traces

    def run(self, max_steps=1000):
        while (self.step()):
            if max_steps == 0:
                raise Exception("Timeout")
            max_steps -= 1
        return self.result()

    def accepts(self, input_string=0):
        self.reset(input_string)
        return self.run()

    def _ipython_display_(self):
        display(to_graphviz(self))
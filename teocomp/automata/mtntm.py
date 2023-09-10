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

        self.reset()

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
                            #     t[i]= [self.blank_sym] +t[i]
                            h[i] = 0 if h[i] < 0 else h[i]
                            t[i] += [self.blank_sym] if h[i] == len(t[i]) else []
                        if (self.keep_traces):
                            updated_traces.append(trace+[(r,h,t,False)])    
                        else:
                            updated_traces.append([(r,h,t,False)])
                elif q in self.acceptStates:
                    updated_traces.append([(q,head[:],tape[:],True)]) # Se indefinido um estado de aceitação, marque a cabeça de leitura.
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
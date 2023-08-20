from ._utils import to_graphviz


class PDA:
    def __init__(self, Q={}, Sigma={}, Gamma={}, delta={}, q0=0, F={}):
        self.states = Q
        self.inputAlphabet = Sigma
        self.stackAlphabet = Gamma
        self.transition = delta
        self.startState = q0
        self.acceptStates = F

        self.reset()

    def reset(self, input_string=""):
        self.traces = [[(self.startState, tuple(input_string), ())]]

    def acceptingTraces(self):
        return [t for t in self.traces if t[-1][1] == () and t[-1][0] in self.acceptStates]

    def result(self):
        return True if self.acceptingTraces() else (False if (not self.traces) else None)

    def step(self):
        if (self.acceptingTraces()):
            return False
        else:
            updated_traces = []
            for trace in self.traces:
                s, string, stack = trace[-1]
                A = {'', string[0]} if string else {''}
                B = {'', stack[-1]} if stack else {''}
                possible_transitions = [
                    (s, a, b) for a in A for b in B if (s, a, b) in self.transition]
                for (s, a, b) in possible_transitions:
                    for r, c in self.transition[s, a, b]:
                        nstring = string[1:] if a else string
                        nstack = stack[:-1] if b else stack
                        nstack = nstack+(c,) if c else nstack
                        if (not (r, nstring, nstack) in trace):
                            updated_traces.append(trace+[(r, nstring, nstack)])
            self.traces = updated_traces
            return self.traces

    def run(self, max_steps=1000):
        while (self.step()):
            if max_steps == 0:
                raise Exception("Timeout")
            else:
                max_steps -= 1
        return self.result()

    def accepts(self, input_string=0):
        self.reset(input_string)
        return self.run()

    def _ipython_display_(self):
        display(to_graphviz(self))


class AP(PDA):
    def aceita(self, input_string=0):
        return self.accepts(input_string)

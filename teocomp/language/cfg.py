class CFG:
    def __init__(self, V, Sigma, R, S):
        self.variables = V
        self.terminals = Sigma
        self.rules = {(a, tuple(b)) for (a, b) in R}
        self.start = S

    def generates(self, string):
        if len(string) == 0:
            return (self.start, ()) in self.rules

        # CYK Algorithm
        G = self._to_chomsky()
        n = len(string)
        P = [[[] for x in range(n - y)] for y in range(n)]
        for i, c in enumerate(string):
            for v in [a for (a, b) in G.rules if len(b) == 1 and c in b]:
                P[0][i] += [v]
        for l in range(2, n+1):  # borda da iteração
            for s in range(0, n+1-l):  # coluna
                for p in range(1, l):  # linha
                    for u, v in [(a, b) for (a, b) in G.rules if len(b) == 2]:
                        if v[0] in P[p-1][s] and v[1] in P[l-p-1][s+p]:
                            P[l-1][s] += [u]
        return G.start in P[-1][0]

    def __repr__(self):
        rightarrow = "\u2192"
        varepsilon = "\u025b"
        output = ""
        right_str = '|'.join(sorted(
            [''.join(y if y else varepsilon) for x, y in self.rules if x == self.start]))
        output = output + \
            f"\n{self.start} {rightarrow} {right_str}" if right_str else output
        for v in sorted(self.variables.difference(self.start)):
            right_str = '|'.join(
                sorted([''.join(y if y else varepsilon) for x, y in self.rules if x == v]))
            output = output + \
                f"\n{v} {rightarrow} {right_str}" if right_str else output

        return output

    def _replace_epsilon(self, v, l):
        if not l:
            return {()}
        result = {(l[0],) + s for s in self._replace_epsilon(v, tuple(l[1:]))}
        if l[0] == v:
            result.update({tuple(s[1:]) for s in result})
        return result

    def _to_chomsky(self):
        n_state = 0

        S = '<{}>'.format(n_state)
        Sigma = self.terminals
        V = {S}.union(self.variables)
        R = {(S, (self.start,))}.union(self.rules)

        target = {alpha for alpha in self.variables if (alpha, ()) in R}
        while (target):
            for e in target:
                rules = {(alpha, beta) for (alpha, beta) in R if e in beta}
                for (a, b) in rules:
                    R.update({(a, beta) for beta in self._replace_epsilon(e, b)})
                R.discard((e, ()))
            target = {alpha for alpha in self.variables if (alpha, ()) in R}

        target = {(a, b) for (a, b) in R if len(b) == 1 and b[0] in V}
        while (target):
            for u, v in target:
                rules = {b for (a, b) in R if a == v[0]}
                R.update({(u, b) for b in rules})
                R.discard((u, v))
            target = {(a, b) for (a, b) in R if len(b) == 1 and b[0] in V}

        target = {(alpha, beta) for (alpha, beta) in R if len(beta) > 2}
        while (target):
            for u, v in target:
                n_state += 1
                state = '<{}>'.format(n_state)
                V.update({state})
                R.update({(u, (v[0], state)), (state, tuple(v[1:]))})
                R.discard((u, v))
            target = {(alpha, beta) for (alpha, beta) in R if len(beta) > 2}

        target = {(alpha, beta) for (alpha, beta) in R if len(beta) == 2}
        for u, v in target:
            n = list(v)
            for i in range(2):
                if v[i] in Sigma:
                    R.discard((u, (n[0], n[1])))
                    n_state += 1
                    n[i] = '<{}>'.format(n_state)
                    V.update({n[i]})
                    R.update({(u, (n[0], n[1]))})
                    R.update({(n[i], (v[i],))})

        return CFG(V, Sigma, R, S)


class GLC(CFG):
    def gera(self, input_string=0):
        return self.generates(input_string)

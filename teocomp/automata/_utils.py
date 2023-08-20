from graphviz import Digraph

def _graphviz_edge_label_format_pda(labels=[]):
        epsilon, right_arrow = "\u03B5", "\u2192"
        return '\n'.join([(a if (a or a==0) else epsilon) + "," + (b if (b or b==0) else epsilon) + right_arrow + (c if (c or c==0) else epsilon) for (a,b,c) in labels])
    
def _graphviz_edge_label_format_nfa(labels):
      epsilon = "\u03B5"
      return ",".join([(str(a) if (a or a==0) else epsilon) for (a,b,c) in labels])

def _to_graphviz_pda(tm, edge_label_format):
    f = Digraph('finite_state_machine', filename='fsm.gv')
    f.attr(rankdir='LR')

    f.attr('node', shape='point')
    f.node('')

    f.attr('node', shape='doublecircle')
    for n in tm.acceptStates:
        f.node(str(n))

    f.attr('node', shape='circle')
    for n in tm.states.difference(tm.acceptStates):
        f.node(str(n))

    label = {}
    for (q,a,b) in tm.transition:
        for (r,c) in tm.transition[q,a,b]:
            label[q,r] = label[q,r]+[(a,b,c)] if (q,r) in label else [(a,b,c)]

    f.edge('', str(tm.startState))
    for (q,r) in label:
        f.edge(str(q),str(r),label=edge_label_format(label[q,r]))

    return f  

def _to_graphviz_tm(tm, highlights=set()):             
        epsilon = "\u03B5"
        rightarrow = "\u2192"
 
        f = Digraph('turing_machine', filename='tm.gv')
        f.attr(rankdir='LR')
 
        f.attr('node', shape='point')
        f.node('')

        f.attr('node', shape='doublecircle')
        for n in tm.acceptStates:
            f.node(str(n),color='gray',style='filled') if n in highlights else f.node(str(n))            

        f.attr('node', shape='circle')
        for n in tm.states - tm.acceptStates:
            f.node(str(n),color='gray',style='filled') if n in highlights else f.node(str(n))
 
        f.edge('', str(tm.startState))
 
        label = {}        
        for key in tm.transition:
          for value in tm.transition[key]:          
            q,r = key[0],value[0]
            nlabel = ','.join(key[1:])+rightarrow+','.join(value[1:])
            label[q,r] = label[q,r]+'\n'+nlabel if (q,r) in label else nlabel
 
        for (q,r) in label:
          f.edge(str(q),str(r),label=label[q,r])      
 
        return f

def to_graphviz(tm):
    from . import PDA, AP, DFA, AFD, NFA, AFN, TM, MT, MTNTM
    
    if type(tm) in [PDA,AP]: 
        return _to_graphviz_pda(tm, _graphviz_edge_label_format_pda)
    if type(tm) in [DFA,AFD,NFA,AFN]: 
        return _to_graphviz_pda(tm, _graphviz_edge_label_format_nfa)
    if type(tm) in [TM,MT,MTNTM]: 
        return _to_graphviz_tm(tm)

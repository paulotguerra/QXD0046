from graphviz import Digraph

def _graphviz_edge_label_format_pda(labels=[]):
        epsilon, right_arrow = "\u03B5", "\u2192"
        return '\n'.join([(a if (a or a==0) else epsilon) + "," + (b if (b or b==0) else epsilon) + right_arrow + (c if (c or c==0) else epsilon) for (a,b,c) in labels])
    
def _graphviz_edge_label_format_nfa(labels):
      epsilon = "\u03B5"
      return ",".join([(str(a) if (a or a==0) else epsilon) for (a,b,c) in labels])

def _to_graphviz_pda(m, edge_label_format):
    f = Digraph('finite_state_machine', filename='fsm.gv')
    f.attr(rankdir='LR')

    f.attr('node', shape='point')
    f.node('')

    f.attr('node', shape='doublecircle')
    for n in m.acceptStates:
        f.node(str(n))

    f.attr('node', shape='circle')
    for n in m.states.difference(m.acceptStates):
        f.node(str(n))

    label = {}
    for (q,a,b) in m.transition:
        for (r,c) in m.transition[q,a,b]:
            label[q,r] = label[q,r]+[(a,b,c)] if (q,r) in label else [(a,b,c)]

    f.edge('', str(m.startState))
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

def to_graphviz(m):
    from ..automata import PDA, AP, DFA, AFD, NFA, AFN, TM, MT, MTNTM
    
    if type(m) in [PDA,AP]: 
        return _to_graphviz_pda(m, _graphviz_edge_label_format_pda)
    if type(m) in [DFA,AFD,NFA,AFN]: 
        return _to_graphviz_pda(m, _graphviz_edge_label_format_nfa)
    if type(m) in [TM,MT,MTNTM]: 
        return _to_graphviz_tm(m)


def _snapshot_pda(m,args):
    from ..automata import PDA, AP
    
    q,h,stack = args

    g = to_graphviz(m)
    g.node(str(q),color='gray',style='filled')

    with g.subgraph(name='cluster_0') as c:
        tape = ['<TD BORDER="0">  </TD>']*2 + [f'<TD>{c}</TD>' for c in list(m.input_string)] + ['<TD BORDER="0">  </TD>']
        head = ['<TD BORDER="0">  </TD>']*(len(tape))
        head[h+2] = '<TD BORDER="0">&#x25BC;</TD>'
        tape[0] = f'<TD>{q}</TD>'
        
        if type(m) in [PDA,AP]:
            if len(stack) >= 2: stack = [f'<TD>{c}</TD>' for c in stack[::-1]]  
            if len(stack) == 1: stack = ['<TD BORDER="0">  </TD>',f'<TD>{stack[0]}</TD>'] 
            if len(stack) == 0: stack = ['<TD BORDER="0">  </TD>','<TD>  </TD>']
            # if len(stack) == 0: stack = ['<TD BORDER="0">  </TD>','<TD BORDER="0">&#8213;</TD>']
        else:
            stack = ['','']
        
        snap_label  = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'''
        snap_label += ''.join([f'''<TR><TD BORDER="0" COLSPAN="{len(tape)}"></TD>{td}</TR>''' for td in stack[:-2]])
        snap_label += '''<TR>{}{}</TR>'''.format("".join(head),stack[-2])
        snap_label += '''<TR>{}{}</TR>'''.format("".join(tape),stack[-1])
        # snap_label += '''<TR><TD BORDER="0">{}</TD><TD BORDER="0"></TD><TD BORDER="0" COLSPAN="{}">{}</TD><TD BORDER="0"></TD><TD BORDER="0">{}</TD></TR>'''.format("state",len(tape)-3,"tape","stack" if type(m) in [PDA,AP] else "")
        snap_label += '''</TABLE>>'''
        c.node('snapshot', shape='none', margin='0', label=snap_label)            
        c.attr(label='Snapshot')        

    g.edge('snapshot','',style='invisible',dir='none')       

    return g


def _snapshot_tm(M,args):
    q,heads,tapes = args       
    
    tape_size = max(map(len,tapes))

    td_string = [[] for i in range(len(tapes)*2)]
    for t in td_string[ ::2]: t += ['<TD BORDER="0">  </TD>']*(tape_size+2)
    for t in td_string[1::2]: t += ['<TD BORDER="0">  </TD>']*2 + ['<TD>  </TD>']*(tape_size)

    for i,h in enumerate(heads): 
        td_string[2*i][h+2] = '<TD BORDER="0">&#x25BC;</TD>'
    for i,t in enumerate(tapes): 
        for j,c in enumerate(t):
                td_string[2*i+1][j+2] = '<TD>  </TD>' if c == M.default['blank'] else f'<TD>{c}</TD>'
    td_string[1][0] = f'<TD>{q}</TD>'

    g = to_graphviz(M)
    g.node(str(q),color='gray',style='filled')

    with g.subgraph(name='cluster_0') as c:
        snap_label  = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'''
        snap_label += ''.join(['<TR>{}</TR>'.format("".join(tr)) for tr in td_string])
        # snap_label += '''<TR><TD BORDER="0">{}</TD><TD BORDER="0"></TD><TD BORDER="0" COLSPAN="{}">{}</TD></TR>'''.format("state",tape_size,"tape" if len(tapes) == 1 else "tapes")
        snap_label += '''</TABLE>>'''                
        c.node('snapshot', shape='none', margin='0', label=snap_label)            
        c.attr(label='Snapshot')  

    g.edge('snapshot','',style='invisible',dir='none')
    
    return g

def snapshot(M):
    from ..automata import PDA, AP, DFA, AFD, NFA, AFN, TM, MT, MTNTM
    
    if type(M) in [DFA,AFD]: 
        return [_snapshot_pda(M,t[-1]) for t in M.traces][0]
    if type(M) in [NFA,AFN,PDA,AP]: 
        return [_snapshot_pda(M,t[-1]) for t in M.traces]
    if type(M) in [TM,MT]: 
        return [_snapshot_tm(M,t[-1][:3]) for t in M.traces][0]
    if type(M) in [MTNTM]: 
        return [_snapshot_tm(M,t[-1][:3]) for t in M.traces]

def interactive(M):
    import ipywidgets as widgets
    from time import sleep

    M.reset()

    a = widgets.Text(description='Input:',placeholder='Enter input string',value='')
    b = widgets.Button(description='Clear')
    c = widgets.Button(description='Step-by-step')
    d = widgets.Button(description='Run')
    e = widgets.FloatSlider(description='Speed:',min=0.1,max=3.01,value=1.0)
    f = widgets.IntSlider(description='Max. steps:',min=1,max=500,value=200,)

    ui  = display(widgets.VBox([widgets.HBox([a,b]),widgets.HBox([c,d,e,f])]), display_id=True)
    out = display(snapshot(M),display_id=True)

    def set_input(s): M.reset(s); out.update(snapshot(M));
    def clear_input(s): a.value = ""
    def step_click(s): M.step() and out.update(snapshot(M))
    def run_click(s): 
        max_steps = f.value
        while(M.step() and max_steps):
            max_steps = max_steps-1
            sleep(0.8*(1/e.value))
            out.update(snapshot(M))

    a.layout.width='750px'
    b.on_click(clear_input)
    c.on_click(step_click)
    d.on_click(run_click)
    widgets.interactive(set_input, s=a);
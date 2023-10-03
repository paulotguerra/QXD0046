from graphviz import Digraph

def _graphviz_edge_label_format_pda(labels=[]):
    epsilon, right_arrow = "\u03B5", "\u2192"
    return '\n'.join([(a if (a or a==0) else epsilon) + "," + (b if (b or b==0) else epsilon) + right_arrow + (c if (c or c==0) else epsilon) for (a,b,c) in labels])
    
def _graphviz_edge_label_format_nfa(labels):
    epsilon = "\u03B5"
    return ",".join([(str(a) if (a or a==0) else epsilon) for (a,b,c) in labels])

def _graphviz_edge_label_format_tm(labels):
    epsilon, right_arrow = "\u03B5", "\u2192"
    a,b,d = ','.join(labels[0]), ','.join(labels[1]), ','.join(labels[2])
    return f"{a} {right_arrow} {b}, {d}" if labels else ""

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

def _to_graphviz_tm(tm, subrotines):
        epsilon = "\u03B5"
        rightarrow = "\u2192"
        edge_label_format = _graphviz_edge_label_format_tm
 
        node = {'':{'label':'', 'shape':'point'}}
        for n in tm.states: node[n] = {'label':f'{n}', 'shape':'circle'}
        for n in tm.acceptStates: node[n] = {'label':f'{n}', 'shape':'doublecircle'}

        edge = {(k[0],v[0]):{'label':''} for k in tm.transition for v in tm.transition[k]}
        for k,v in [(k,v) for k in tm.transition for v in tm.transition[k]]:
            q,a,r,b,d = k[0], k[1:], v[0], v[1:len(k)], v[len(k):]
            edge[q,r]['label'] += edge_label_format((a,b,d)) + "\n"
        edge['',f'{tm.startState}']= {'label':''}

        if subrotines == 'collapse':
            collapsed = {f'{m}_{s}' for m in tm._subroutine for s in tm._subroutine[m].states}
            start_state_map = {f'{m}_{tm._subroutine[m].startState}':f'{m}' for m in tm._subroutine}
            accept_state_map = {f'{m}_{s}':f'{m}' for m in tm._subroutine for s in tm._subroutine[m].acceptStates}    
            for n in collapsed: 
                node.pop(n)
            for n in tm._subroutine: 
                node[n] = {'label':f'{n}', 'shape':'rectangle'}
            for q,r in [(q,r) for (q,r) in edge if r in start_state_map]:
                edge[q,start_state_map[r]] = edge[q,r]
            for q,r in [(q,r) for (q,r) in edge if q in accept_state_map]:
                edge[accept_state_map[q],r] = edge[q,r]
            for q,r in [(q,r) for (q,r) in edge if q in collapsed or r in collapsed]:
                edge.pop((q,r))

        f = Digraph('turing_machine', filename='tm.svg')
        f.attr(rankdir='LR')
        for n in node:
            f.node(f'{n}', label=node[n]['label'], shape=node[n]['shape']) 
        
        for (q,r) in edge:
            f.edge(f'{q}',f'{r}',label=edge[q,r]['label'])

        if subrotines == 'expand':
            for m in tm._subroutine:
                with f.subgraph(name=f'cluster_{m}') as c:
                    [c.node(f'{m}_{q}') for q in tm._subroutine[m].states]
                    c.attr(label=str(m))
 
        return f

def to_graphviz(m, subrotines='collapse'):
    from ..automata import PDA, AP, DFA, AFD, NFA, AFN, TM, MT, MTNTM
    
    if type(m) in [PDA,AP]: 
        return _to_graphviz_pda(m, _graphviz_edge_label_format_pda)
    if type(m) in [DFA,AFD,NFA,AFN]: 
        return _to_graphviz_pda(m, _graphviz_edge_label_format_nfa)
    if type(m) in [TM,MT,MTNTM]: 
        return _to_graphviz_tm(m, subrotines)


def _snapshot_pda(m,info):
    from ..automata import PDA, AP
    
    q,h,stack = info

    g = to_graphviz(m)
    g.node(str(q),style='filled')

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


def _snapshot_tm(M, info, subrotines):
    q,heads,tapes = info       
    
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

    g = to_graphviz(M, subrotines)
    
    highlight = str(q)        
    if subrotines == 'collapse':
        collapsed_states = {f'{m}_{s}' for m in M._subroutine for s in M._subroutine[m].states}
        if highlight in collapsed_states: 
            highlight = highlight.split('_')[0]    
    g.node(highlight, style='filled')

    with g.subgraph(name='cluster_0') as c:
        snap_label  = '''<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">'''
        snap_label += ''.join(['<TR>{}</TR>'.format("".join(tr)) for tr in td_string])
        # snap_label += '''<TR><TD BORDER="0">{}</TD><TD BORDER="0"></TD><TD BORDER="0" COLSPAN="{}">{}</TD></TR>'''.format("state",tape_size,"tape" if len(tapes) == 1 else "tapes")
        snap_label += '''</TABLE>>'''                
        c.node('snapshot', shape='none', margin='0', label=snap_label)            
        c.attr(label='Snapshot')  

    g.edge('snapshot','',style='invisible',dir='none')
    
    return g

def snapshot(M, subrotines='expand'):
    from ..automata import PDA, AP, DFA, AFD, NFA, AFN, TM, MT, MTNTM
    
    if type(M) in [DFA,AFD]: 
        return [_snapshot_pda(M,t[-1]) for t in M.traces][0]
    if type(M) in [NFA,AFN,PDA,AP]: 
        return [_snapshot_pda(M,t[-1]) for t in M.traces]
    if type(M) in [TM,MT]: 
        return [_snapshot_tm(M,t[-1][:3],subrotines) for t in M.traces][0]
    if type(M) in [MTNTM]: 
        return [_snapshot_tm(M,t[-1][:3],subrotines) for t in M.traces]

def interactive(M):
    import ipywidgets as widgets
    from time import sleep

    M.reset()

    a = widgets.Text(description='Input:',placeholder='Enter input string',v='')
    b = widgets.Button(description='Clear')
    c = widgets.Button(description='Step-by-step')
    d = widgets.Button(description='Run')
    e = widgets.FloatSlider(description='Speed:',min=0.1,max=3.01,value=1.0)
    f = widgets.IntSlider(description='Max. steps:',min=1,max=500,value=200,)
    g = widgets.Dropdown(options=['collapse', 'expand', 'hide'], value='collapse', description='Subroutines:', disabled=False)

    ui  = display(widgets.VBox([widgets.HBox([a,b,c,d,]),widgets.HBox([e,f,g])]), display_id=True)
    out = display(snapshot(M,g.value),display_id=True)

    def set_input(s): M.reset(s); out.update(snapshot(M,g.value));
    def clear_input(s): a.v = ""
    def step_click(s): M.step() and out.update(snapshot(M,g.value))
    def subrotines_onchange(s): out.update(snapshot(M,g.value))
    def run_click(s): 
        max_steps = f.value
        while(M.step() and max_steps):
            max_steps = max_steps-1
            sleep(0.8*(1/e.value))
            out.update(snapshot(M,g.value))

    a.layout.width='450px'
    b.on_click(clear_input)
    c.on_click(step_click)
    d.on_click(run_click)
    widgets.interactive(set_input, s=a)
    widgets.interactive(subrotines_onchange, s=g)
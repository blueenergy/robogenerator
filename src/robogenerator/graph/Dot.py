"""
Dot - generate graphics in dot language
"""

import os.path
from types import MethodType, FunctionType

def node(n, fsm):
    try: # FSM modules written by PyModel Analyzer have frontier attribute etc.
        frontier = fsm.frontier
        finished = fsm.finished
        deadend = fsm.deadend
        runstarts = fsm.runstarts

    except AttributeError: # FSM modules written by hand may not have these
        frontier = list()
        finished = list()
        deadend = list()
        runstarts = list()
    return '%s [ style=filled, shape=ellipse, peripheries=%s, fillcolor=%s' % \
        (n, 2 if n in fsm.accepting else 1, # peripheries
         'orange' if n in frontier else # high priority, analysis inconclusive
         'yellow' if n in deadend else
         'green' if n in finished else
         'lightgray' if n == fsm.initial or n in runstarts else #lowest priority
         'white') # other states

def state(n, fsm, noStateTooltip):
    if noStateTooltip:
        return '%s ]' % node(n,fsm)
    else:
        return '%s,\n      tooltip="%s" ]' % (node(n,fsm), fsm.states[n])


def quote_string(x): # also appears in Analyzer
    if isinstance(x,tuple):
        return str(x)
    else:
        return "'%s'" % x if isinstance(x, str) else "%s" % x

def rlabel(result):
    return '/%s' % quote_string(result) if result != None else ''

def get_transition_line_color(fsm,t):
    try:
        if t in fsm.tested_transitions:
            return 'green'
        else:
            return 'red'
    except AttributeError:
        return 'black'


def transition(t, style,fsm):
    current, (a, args, result), next = t
    name_str = a.__name__ if type(a) in [MethodType, FunctionType] else a
    transition = current,(name_str,args), next
    action = '%s%s%s' % (name_str, args, rlabel(result))
    if style == 'name':
        label = '%s' % name_str
    elif style == 'none':
        label = '' 
    else: # 'action'
        label = action
    return '%s -> %s [ label="%s", tooltip="%s",color="%s"]' % \
        (current, next, label, action,get_transition_line_color(fsm,transition))

def dotfile(fname, fsm, style, noStateTooltip):
    f = open(fname, 'w')
    f.write('digraph %s {\n' % os.path.basename(fname).partition('.')[0])
    f.write('\n  // Nodes\n')
    try: # FSM modules written by PyModel Analyzer have states attribute
        f.writelines([ '  %s\n' % state(n,fsm,noStateTooltip) for n in fsm.states ])    
    except: # FSM modules written by hand may not have states attribute
        nodes = set([current for (current,trans,next) in fsm.graph] 
                    + [next for (current,trans,next) in fsm.graph])
        print nodes
        f.writelines([ '  %s ]\n' % node(n,fsm) for n in nodes ])    
    f.write('\n  // Transitions\n')
    print fsm.graph
    print 'graph output finished'
    f.writelines([ '  %s\n' % transition(t, style,fsm) for t in fsm.graph ])
    f.write('}\n')
    f.close()

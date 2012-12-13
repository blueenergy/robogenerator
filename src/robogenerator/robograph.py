#!/usr/bin/env python
"""
Robogenerator Graphics - generate graphics from Robogenerator FSM
"""

import graph.GraphicsOptions as GraphicsOptions
from graph.Dot import dotfile
import os
from util import add_to_env_variable

def get_all_possible_transitions(state_list):
    all_transitions = []
    for state in state_list:
        current_state = state['name']
        if state.has_key('actions'):
            for action in state['actions']:
                aname = action[0]
                args = action[1]
                model_result = action[-2]
                next_state = action[-1]
                all_transitions.append((current_state,(aname,args,model_result),next_state))
    return all_transitions

def generate_state_machine_graph(fsm, fbasename):
    fname = '%s.dot' % fbasename
    fsm.graph = get_all_possible_transitions(fsm.state_graph)
    dotfile(fname, fsm,'','')
    command = 'dot -Tpng %s > %s.png' % (fname, fbasename)
    print command
    add_to_env_variable('PATH',os.path.dirname(os.path.abspath(__file__)))
    os.system(command)


def main():
    (options, args) = GraphicsOptions.parse_args()
    if not args or len(args) > 2: # args must include one FSM module
        GraphicsOptions.print_help()
        exit()
    else:
        fsm = __import__(args[0])
        fbasename = options.output if options.output else args[0]
        fname = '%s.dot' % fbasename
        fsm.graph = get_all_possible_transitions(fsm.state_graph)
        
        dotfile(fname, fsm, options.transitionLabels, options.noStateTooltip)
        command = 'dot -Tpng %s > %s.png' %(fname,fbasename)
        print command
        add_to_env_variable('PATH',os.path.dirname(os.path.abspath(__file__)))
        os.system(command)
        import Image
        im = Image.open('%s.png'%fbasename)
        im.show()

if __name__ == '__main__':
    main ()

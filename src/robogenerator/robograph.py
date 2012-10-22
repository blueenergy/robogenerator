#!/usr/bin/env python
"""
PyModel Graphics - generate graphics from pymodel FSM
"""

import graph.GraphicsOptions as GraphicsOptions
from graph.Dot import dotfile

def get_all_possible_transitions(state_list):
    all_transitions = []
    for state in state_list:
        current_state = state['name']
        if state.has_key('actions'):
            for action in state['actions']:
                aname = action[0]
                args = action[1:-2]
                model_result = action[-2]
                next_state = action[-1]
                all_transitions.append((current_state,(aname,args,model_result),next_state))
    return all_transitions


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

if __name__ == '__main__':
    main ()

"""
ActionNameCoverage: choose the action name which has been used least
"""

import random

# Tester state is a bag of action names: { aname : n of times used }

coverage = dict()

def SelectAction(enabled):
    """
    Choose the action symbol which has been used the least number of times.
    If more than one action has been used that many times, choose randomly.
    """
    if not enabled: # empty 
        return (None, None,None)
    else:
        coverage.update(dict([(aname,0) 
                            for (aname,args,result,next) in enabled 
                            if aname not in coverage])) # multiple occurs OK
        least = min([coverage[action[0]] 
                   for action in enabled]) 
        aleast = [(aname,args,result,next) for (aname,args,result,next) in enabled 
                                 if coverage[aname] == least]
        aname,args,result,next_state = random.choice(aleast)
        coverage[aname] += 1
        return aname,args,result,next_state


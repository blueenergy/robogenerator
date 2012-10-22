import random
coverage = []
def SelectAction(actions):
    if not actions: # empty 
        return (None, None,None)

    for action in actions:
        if action not in coverage:
            coverage.append(action)
            return action[0],action[1],action[-1]
    action = random.choice(actions)
    
    return action[0],action[1],action[2],action[-1]
    #return None,None,None

        
documentation ='''The case is to do Trial Service test  in cost-effective way'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
resource ='IpaMml.html'
library ="state_change_library.py"
library = library.replace('\\','/')

parameters_template = {'unit_type': ["DMCU","RSMU"],
                       'restart_mode':['OPT'],
                       'state':['WO-EX']
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
parameters = parameters_template
output_filename ='NEW Trial CI Test Case.txt'
case_name_template = 'Trial CI Test Case'


def create_trial(state):
    print 'create_trial'

def modify_trial(dest_trial_type):
    pass

def cancel_trial():
    pass
def cut_over():
    pass
def reverse_cutover():
    pass
def trial_complete():
    pass

def system_should_be_in_state(state):
    pass


idle_state=omu_trial_state=core_trial_state=base_trial_state=cutover_complete_state=trial_complete_state ={}

idle_state = {'name':'idle_state',
          'step':(system_should_be_in_state,'IDLE'),
          'actions':[(create_trial,('omu_trial',),None,'omu_trial_state'),
                    (create_trial,('core_trial',),None,'core_trial_state'),
		            (create_trial,('base_trial',),None,'base_trial_state')]
          }

omu_trial_state = {'name':'omu_trial_state',
          'step':(system_should_be_in_state,'omu_trial_state'),
          'actions':[(modify_trial,('CORE',),None,'core_trial_state'),
                    (modify_trial,('BASE',),None,'base_trial_state'),
		            (cancel_trial,(' ',),None,'idle_state')]
          }

core_trial_state = {'name':'core_trial_state',
          'step':(system_should_be_in_state,'core_trial_state'),
          'actions':[(modify_trial,('BASE',),None,'base_trial_state'),
		             (cancel_trial,(' ',),None,'idle_state')]
          }
base_trial_state = {'name':'base_trial_state',
          'step':(system_should_be_in_state,'base_trial_state'),
          'actions':[(cancel_trial,(' ',),None,'idle_state'),
		             (cut_over,('OTO',),None,'cutover_complete_state'),
					 (cut_over,('TOT',),None,'cutover_complete_state')]
          }

cutover_complete_state = {'name':'cutover_complete_state',
          'step':(system_should_be_in_state,'cutover_complete_state'),
          'actions':[(trial_complete,(' ',),None,'trial_complete_state'),
                     (reverse_cutover,('TOT',),None,'core_trial_state')]
          }

trial_complete_state = {'name':'trial_complete_state',
          'step':(system_should_be_in_state,'trial_complete_state')
          }


state_graph = [idle_state,omu_trial_state,core_trial_state,base_trial_state,cutover_complete_state,trial_complete_state]

def is_valid_combination(row):
    
    n=len(row)
    if n>=len(parameters):
        return True
    return True


accepting = state_graph
initial = 'idle_state'

def find_all_paths(graph, start, end, path=[]):

    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths
#print find_all_paths(graph, 'A', 'C')

#graph = get_all_possible_transitions(state_graph)

if __name__=='__main__':
    pass
    '''
    #print wo_ex_state['actions'][0][0].__name__
    #state = StateModel(wo_ex_state)
    #state = StateModel(data_driving)
    #print state.name
    #print state.get_step_name()+'  '+'  '.join(state.get_step_argument())
    #print state_graph[state.get_random_next_state()]
    
    #print StateModel(data_driving).get_step_name()
    #print type(wo_ex_state['actions'][0]['action']) == type(is_valid_combination)
    #print data_driving['step']['action']
    #States = [StateModel(state) for state in state_graph]
    #print States[0].name
    #print dir(States[0])
    #print States[0].get_step_name()
    #print States[0].get_random_next_state()
    #print len(States)
    '''

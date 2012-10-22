
# pma.py ZDT
# 10 states, 12 transitions, 10 accepting states, 0 finished and 0 deadend states

# actions here are just labels, but must be symbols with __name__ attribute

def Recv(): pass

# states, key of each state here is its number in graph etc. below

states = {
   'system_idle_state' : {'ZDT': 'system_idle_state'},
   'preloading' : {'ZDT': 'preloading'},
   'assessment_complete' : {'ZDT': 'assessment_complete'},
   'sys_lockdown' : {'ZDT': 'sys_lockdown'},
   'compress_complete' : {'ZDT': 'compress_complete'},
   'zdt_configuration_complete' : {'ZDT': 'zdt_configuration_complete'},
   'pre_cutover_complete' : {'ZDT': 'pre_cutover_complete'},
   'cutover_complete' : {'ZDT': 'cutover_complete'},
   'post_cutover_complete' : {'ZDT': 'post_cutover_complete'},
   'resource_balance_complete' : {'ZDT': 'resource_balance_complete'},
}

# initial state, accepting states, frontier states, deadend states

initial = 0
accepting = ['system_idle_state', 'preloading', 'assessment_complete', 'sys_lockdown', 'compress_complete', 'zdt_configuration_complete', 'pre_cutover_complete', 'cutover_complete', 'post_cutover_complete', 'resource_balance_complete']
frontier = []
finished = []
deadend = []
runstarts = ['system_idle_state']

# finite state machine, list of tuples: (current, (action, args, result), next)

graph = (
  ('system_idle_state', (Recv, ('preloading_command',), None), 'preloading'),
  ('system_idle_state', (Recv, ('assessment_command',), None), 'assessment_complete'),
  ('preloading', (Recv, ('assessment_command',), None), 'assessment_complete'),
  ('assessment_complete', (Recv, ('sys_lockdown_command',), None), 'sys_lockdown'),
  ('sys_lockdown', (Recv, ('resource_compress_command',), None), 'compress_complete'),
  ('compress_complete', (Recv, ('create_zdt_command',), None), 'zdt_configuration_complete'),
  ('zdt_configuration_complete', (Recv, ('pre_cutover_complete_command',), None), 'pre_cutover_complete'),
  ('pre_cutover_complete', (Recv, ('cutover_command',), None), 'cutover_complete'),
  ('cutover_complete', (Recv, ('cutover_to_origin_command',), None), 'pre_cutover_complete'),
  ('cutover_complete', (Recv, ('post_cutover_command',), None), 'post_cutover_complete'),
  ('post_cutover_complete', (Recv, ('resource_balance_command',), None), 'resource_balance_complete'),
  ('resource_balance_complete', (Recv, ('zdt_complete_command',), None), 'system_idle_state'),
)

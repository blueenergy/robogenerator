from sip_service_lib import *
documentation ='''The case is to do SIP Service test  in cost-effective way'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
library ="sip_service_lib.py"
library = library.replace('\\','/')

output_filename ='SIP_Service_Test.html'
case_name_template = 'SIP Service Test'

idle_state=init_state=calling_state=base_trial_state=terminating_state=cancel_state =ring_state ={}

idle_state = {'name':'idle_state',
          'step':(state_should_be,'idle_state'),
          'actions':[(receive_message,('${OFFHOOK_SIGNAL}',),None,'init_state')]}
		  
init_state = {'name':'init_state',
          'step':(state_should_be,'init_state'),
          'actions':[(receive_message,('${CALLING_SIGNAL}',),None,'calling_state')]
          }
calling_state = {'name':'calling_state',
          'step':(state_should_be,'calling_state'),
          'actions':[(receive_message,('${TIMEOUTB}',),None,'terminating_state'),
                     (receive_message,('${TIMEOUTA}',),None,'terminating_state'),
		    (receive_message,('${CALL_PROCEEDING}',),None,'ring_state'),
		    (receive_message,('${REJECT}',),None,'cancel_state')]
          }
terminating_state = {'name':'terminating_state',
          'step':(state_should_be,'terminating_state'),
           'actions':[(receive_message,('${200_BYE}',),None,'idle_state')]}

cancel_state = {'name':'cancel_state',
          'step':(state_should_be,'cutover_complete_state'),
          'actions':[(receive_message,('${200_Cancel}',),None,'wait_response_state')]
          }

ring_state = {'name':'ring_state',
          'step':(state_should_be,'ring_state'),
           'actions':[(receive_message,('${200}',),None,'ready_state'),
					(receive_message,('${REJECT}',),None,'idle_state'),
					(receive_message,('${CANCEL}',),None,'cancel_state')]
          }


ready_state = {'name':'ready_state',
          'step':(state_should_be,'ready_state'),
           'actions':[(receive_message,('${BYE}',),None,'idle_state')]
          }

wait_response_state = {'name':'wait_response_state',
          'step':(state_should_be,'wait_response_state'),
           'actions':[(receive_message,('${487_Invite}',),None,'idle_state')]
          }

state_graph = [idle_state,init_state,calling_state,terminating_state,cancel_state,ring_state,ready_state,wait_response_state]


accepting = state_graph
initial = state_graph[0]['name']

#graph = get_all_possible_transitions(state_graph)

if __name__=='__main__':
    pass


#from state_change_library import wait_unit_in_required_state,change_unit_state_and_check_result
#import  areaci_common

documentation ='''The case is to change unit state in all kinds of states'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
test_setup = 'Select One DMCU'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
resource ='IpaMml.html'
library ="state_change_library.py"
library = library.replace('\\','/')

parameters_template = {'unit_type': ["DMCU-0"]
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
#parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)
parameters = parameters_template
output_filename ='NEW_Change_Unit_State_Test.txt'
case_name_template = 'change unit State '

def unit_should_be_in_state(unit_name,state):
    pass

def restart_unit(unit):
    pass

def change_unit_state_and_check_result(unit_name,state):
    pass

def wait_unit_in_required_state(unit_name,state):
    pass



wo_ex_state=bl_id_state=bl_re_state=te_ex_state=se_ou_state=se_nh_state=te_re_state=wo_re_state ={}


wo_ex_state = {'name':'wo_ex_state',
          'step':(unit_should_be_in_state,'DMCU-0','WO-EX'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','BL'),None,'bl_id_state'),
                    (change_unit_state_and_check_result,('DMCU-0','TE'),None,'te_re_state')]
          }

bl_id_state = {'name':'bl_id_state',
          'step':(unit_should_be_in_state,'DMCU-0','BL-ID'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','TE'),None,'te_ex_state'),
                     (change_unit_state_and_check_result,('DMCU-0','WO'),None,'wo_ex_state'),
                     (restart_unit,('DMCU-0',),None,'bl_re_state')]
          }
bl_re_state = {'name':'bl_re_state',
          'step':(unit_should_be_in_state,'DMCU-0','BL-RE'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','TE'),None,'te_re_state'),
                     (wait_unit_in_required_state,('DMCU-0','BL_ID'),None,'bl_id_state')]
          }

te_ex_state = {'name':'te_ex_state',
          'step':(unit_should_be_in_state,'DMCU-0','TE-EX'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','SE'),None,'se_ou_state'),
                     (change_unit_state_and_check_result,('DMCU-0','WO'),None,'wo_re_state')]
          }

se_ou_state = {'name':'se_ou_state',
          'step':(unit_should_be_in_state,'DMCU-0','SE-OU'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','SE'),None,'se_nh_state'),
                     (change_unit_state_and_check_result,('DMCU-0','TE'),None,'te_re_state')]
          }
se_nh_state = {'name':'se_nh_state',
          'step':(unit_should_be_in_state,'DMCU-0','SE-NH'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','SE'),None,'se_ou_state')]
          }

te_re_state = {'name':'te_re_state',
          'step':(unit_should_be_in_state,'DMCU-0','TE-RE'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','SE'),None,'se_ou_state'),
                     (wait_unit_in_required_state,('DMCU-0','TE-EX'),None,'te_ex_state')]
          }

wo_re_state = {'name':'wo_re_state',
          'step':(unit_should_be_in_state,'DMCU-0','WO-RE'),
          'actions':[(change_unit_state_and_check_result,('DMCU-0','TE'),None,'te_re_state'),
                     (wait_unit_in_required_state,('DMCU-0','WO-EX'),None,'wo_ex_state')]
          }

state_graph = [wo_ex_state,bl_id_state,bl_re_state,te_ex_state,se_ou_state,se_nh_state,te_re_state,wo_re_state]

accepting = state_graph
initial = 'idle_state'


def is_valid_combination(row):
    
    n=len(row)
    if n>=len(parameters):
        return True

        # not core unit state is wo and is 2N unit,only restart unit with mode OPT,TOT,DSK
        
    return True


    

if __name__=='__main__':



    import random
    actions =[(change_unit_state_and_check_result,'SE','se_ou_state')]
    action = random.choice(actions)
    #print action
    func_list =[change_unit_state_and_check_result,wait_unit_in_required_state]
    print func_list[0]('ICSU-0')
    a= 1
    if a == 2:
        print 2
    elif a == 1:
        print 'value is 1'
        
    




        
        
  




        

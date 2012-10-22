from state_change_library import wait_unit_in_required_state,change_unit_state_and_check_result
#import  areaci_common 
documentation ='''The case is to change unit state in all kinds of states'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
resource ='IpaMml.html'
library ="state_change_library.py"
library = library.replace('\\','/')

parameters_template = {'unit_type': ["DMCU"]
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
#parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)
parameters = parameters_template
output_filename ='NEW_Change_Unit_State_Test.txt'
subcase_tag_template = 'element-${element_type}  SFUType-${sfutype}  Pairwise '
case_name_template = 'change unit State '

case_step_template = '''Verify Unit State Change  ${unit_type}'''
#keyword_template = '''Vefiry Unit Restart'''
#print parameters

def get_test_step_from_action_name(action_name):
    if action_name =='WAIT':
        return 'wait_unit_in_required_state  ${next_state_name}\n'
    else:
        return 'change_unit_state_and_check_result  ${next_state_name}\n'


def change_unit_state(state):
    pass
def wait_unit_in_required_state(state_name):
    pass
def unit_should_be_in_state(state):
    pass
wo_ex_state = {'name':'WO-EX',
          'guarding':{'action':unit_should_be_in_state,'arguments':'WO-EX'},
          'actions':({'action':change_unit_state,'arguments':'BL','next_state':bl_id_state},
                     {'action':change_unit_state,'arguments':'TE','next_state':te_re_state})
          }
bl_id_state = {'name':'BL-ID',
          'guarding':(unit_should_be_in_state,'BL-ID'),
          'actions':({'action':change_unit_state,'arguments':'TE','next_state':te_ex_state},
                     {'action':change_unit_state,'arguments':'WO','next_state':wo_ex_state})
          }
bl_re_state = {'name':'BL-RE',
          'guarding':(unit_should_be_in_state,'BL-RE'),
          'actions':({'action':change_unit_state,'arguments':'TE','next_state':te_re_state},
                     {'action':wait_unit_in_required_state,'arguments':'','next_state':bl_id_state})
          }

te_ex_state = {'name':'TE-EX',
          'guarding':(unit_should_be_in_state,'TE-EX'),
          'actions':({'action':change_unit_state,'arguments':'SE','next_state':se_ou_state},
                     {'action':change_unit_state,'arguments':'WO','next_state':wo_re_state})
          }

se_ou_state = {'name':'SE-OU',
          'guarding':(unit_should_be_in_state,'SE-OU'),
          'actions':({'action':change_unit_state,'arguments':'SE','next_state':se_nh_state},
                     {'action':change_unit_state,'arguments':'TE','next_state':te_re_state})
          }
se_nh_state = {'name':'SE-NH',
          'guarding':(unit_should_be_in_state,'SE-NH'),
          'actions':({'action':(change_unit_state,'SE'),'next_state':se_ou_state})
          }

te_re_state = {'name':'TE-RE',
          'guarding':(unit_should_be_in_state,'TE-RE'),
          'actions':({'action':change_unit_state,'arguments':'SE','next_state':se_ou_state},
                     {'action':wait_unit_in_required_state,'arguments':'TE-EX','next_state':te_ex_state},
                     {'action':change_unit_state,'arguments':'SE','next_state':se_ou_state})
          }

wo_re_state = {'name':'WO-RE',
          'guarding':(unit_should_be_in_state,'WO-RE'),
          'actions':({'action':(change_unit_state,'TE'),'next_state':te_re_state},
                     {'action':(wait_unit_in_required_state,'WO-EX'),'next_state':wo_ex_state})
          }

state_graph = [wo_ex_state,bl_id_state,bl_re_state,te_ex_state,se_ou_state,se_nh_state,te_re_state,wo_re_state]
starting_state_name = wo_ex_state









def is_valid_combination(row):
    
    n=len(row)
    if n>=len(parameters):

        # not core unit state is wo and is 2N unit,only restart unit with mode OPT,TOT,DSK
        if row['unit_type'] in ['OMU','RSMU']:
            return False
        
    return True


    

if __name__=='__main__':

    pass




        
        
  




        

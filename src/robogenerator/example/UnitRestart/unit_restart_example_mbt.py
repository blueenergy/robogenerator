import sys
import os

documentation ='''The case is to Restart all kinds of units with required state
'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
test_setup ='Clear Test Env And Start Moni Msg'
test_teardown = 'get alarm recovery history log bblog and message after test'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
resource ='IpaMml.html'
library ="\\resources\\unit_restart_lib.py"
library = library.replace('\\','/')

parameters_template = {'unit_type': [ "ICSU","NPGEP"]
             , 'state':[ "WO-EX","SP-EX"]
             , 'restart_mode':[ "OPT","TOT"]         
             }
#parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)
parameters = parameters_template
output_filename ='NEW_Restart_all_kinds_of_Unit_Test.txt'
subcase_tag_template = 'Pairwise '
case_name_template = 'restart ${unit_type} in required ${state} with ${restart_mode} mode'
case_name_template = 'restart unit in required state with required mode'
#print parameters

def verify_unit_restart(unit_type,state,restart_mode):
    pass

def restart_unit_with_mode():
    pass
idle_state = {'name':'idle_state',
          'step':(restart_unit_with_mode,'${unit_type}','${state}','${restart_mode}'),
		  'actions':[(restart_unit_with_mode,('unit_type','state','restart_mode'),None,'idle_state')]
          }

state_graph = [idle_state]
def is_valid_combination(row):
    """
    Should return True if combination is valid and False otherwise.
    
    Test row that is passed here can be incomplete.
    To prevent search for unnecessary items filtering function
    is executed with found subset of data to validate it.
    """
    
    n=len(row)
    if n>=len(parameters):

        # not core unit state is wo and is 2N unit,only restart unit with mode OPT,TOT,DSK
        if row['state'] =="WO-EX" and row['unit_type'] in ['OMU','RSMU'] and row['restart_mode'] in ["ZXCA","ZXDG","ALARM1023","ALARM1012","KILLPRB","ZXCB","REBOOT"]:
            return False
        
    return True

accepting = state_graph
initial = 'idle_state'



if __name__=='__main__':

    pass




        
        
  




        

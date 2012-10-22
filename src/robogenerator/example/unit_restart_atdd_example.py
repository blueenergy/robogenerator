import sys
import os
resource_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append('%s/resources/areaci'%resource_path)
from areaci_const import IO_unit_types,CORE_unit_types,Hot_Redundancy_unit_types,\
                         SN_unit_types,Nplus1_unit_types,Non_Redundancy_unit_types,\
                         Chorus_unit_types,DMX_unit_types,Unit_has_BL_type_list,Hierarchy_unit_types
import  areaci_common 
documentation ='''The case is to Restart all kinds of units with required state
'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
test_setup ='Clear Test Env And Start Moni Msg'
test_teardown = 'get alarm recovery history log bblog and message after test'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
resource ='IpaMml.html'
library ="%s\\resources\\unit_restart_lib.py"%resource_path
library = library.replace('\\','/')


parameters_template = {'unit_type': [ "ICSU","NPGEP","OMU","RSMU","NPS1P"]
             , 'state':[ "WO-EX","SP-EX","TE-EX","BL-ID"]
             , 'restart_mode':[ "OPT","TOT","DSK","ZXCA","ZXDG","ALARM1023","ALARM1012","KILLPRB","ZXCB","REBOOT" ]
             , 'element_type':["RNC","MGW"]
             , 'sfutype':["SF20H"]             
             }
#parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)
parameters = parameters_template
output_filename ='NEW_Restart_all_kinds_of_Unit_Test.txt'
subcase_tag_template = 'element-${element_type}  SFUType-${sfutype}  Pairwise '
case_name_template = 'restart all kings of unit in diffrent state with required mode'

case_step_template = '''${unit_type}  ${state}  ${restart_mode}'''
keyword_template = '''Vefiry Unit Restart'''
#print parameters


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


    

if __name__=='__main__':

    pass




        
        
  




        

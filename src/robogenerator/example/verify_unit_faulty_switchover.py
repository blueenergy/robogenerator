import sys
import os
resource_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append('%s/resources/areaci'%resource_path)
from areaci_const import IO_unit_types,CORE_unit_types,Hot_Redundancy_unit_types,\
                         SN_unit_types,Nplus1_unit_types,Non_Redundancy_unit_types,\
                         Chorus_unit_types,DMX_unit_types,Unit_has_BL_type_list,Hierarchy_unit_types
import  areaci_common

'''
1. TBU Fault swo if needed, need to discuss with people
2. SWO only once
3. random select one kind of MXU pair to test
4. IWSEP/IWSTP to be decided
5.  filter 2N unit only in case validation function

'''


documentation ='''The case is to faulty switchover all kinds of units with required state
'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
test_setup='Clear Test Env And Start Moni Msg'
test_teardown = 'get alarm recovery history log bblog and message after test'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req  element-${element_type}  SFUType-${sfutype}'''
resource ='IpaMml.html'
library ="%s\\resources\\unit_switchover_lib.py"%resource_path
library = library.replace('\\','/')

parameters_template = {'unit_type': [ "RSMU","MXU"]
             , 'switch_over_mode':[ 'REBOOT','KILLPRB','ZXCA','ZXDG','ZXCB','ZXCS/CT','ALARM1023','ALARM1012','SETFLTY' ]
             , 'element_type':["RNC","MGW"]
             , 'sfutype':["SF20H"]             
             }
parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)
output_filename ='FLTY_SWO_all_kinds_of_Unit.txt'
case_name_template = 'verify ${unit_type} switchover with ${switch_over_mode}'

case_step_template = '''Verify Unit Flty Switch Over  ${unit_type}  ${switch_over_mode}'''
#print parameters
keyword_template = '''Verify Unit Flty Switch Over'''


def is_valid_combination(row):
    """
    Should return True if combination is valid and False otherwise.
    
    Test row that is passed here can be incomplete.
    To prevent search for unnecessary items filtering function
    is executed with found subset of data to validate it.
    """
    
    n=len(row)
    if n>=len(parameters):

        # will not do control SWO when unit is not 2N or N+1 unit
        if row['unit_type'] not in (Hot_Redundancy_unit_types + Nplus1_unit_types):
            return False
        #plug unit is IW1S1 and IW8S1,these not test
        if row['unit_type'] in ['IWSEP','IWSTP']:
            return False
        if row['switch_over_mode'] in ['ZXCS/CT']:
        #CCP1D_A piu is not considered
            return False
        if row['unit_type'] in ['TBU'] and row['switch_over_mode'] in ['REBOOT','KILLPRB','ZXCB']:
            return False
        
    return True


    

if __name__=='__main__':
    '''
    robogenerator  ./verify_unit_faulty_switchover -ip 10.68.187.147 -g dfs -o verify_unit_faulty_switchover.txt
    robogenerator  ./verify_unit_faulty_switchover -ip 10.68.187.147 -g random -t 20 -o verify_unit_faulty_switchover.txt
    python ../../SSAreaCI/robogenerator.py ./verify_unit_faulty_switchover -ip 10.68.187.147 -g random -t 5 -o verify_unit_faulty_switchover.txt
    '''

    print (Hot_Redundancy_unit_types + Nplus1_unit_types)




        
        
  




        

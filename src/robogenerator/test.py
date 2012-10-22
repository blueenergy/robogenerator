documentation ='test in MBT'
test_setup ='Clear Test Env And Start Moni Msg'
test_teardown = 'get alarm recovery history log bblog and message after test'
force_tags ='''team-Alpha  phase-RT  req-PRS_None_Req  QL-6'''
resource ='IpaMml.html'



parameters = {'cpu_load': [ "HIGH","LOW"]
             , 'feature_switch':[ "ON","OFF"]
             , 'license_status':[ "ON","OFF"]
             , 'expected_result':["TBD"]             
             }

output_filename ='NEW_Restart_all_kinds_of_Unit_Test.txt'
case_name_template = 'Do some feature test'

case_step_template = '''Do some feature test  ${cpu_load}  ${feature_switch}  ${license_status}  ${expected_result}'''


class testObject():
    def __init__(self,name):
        pass
def is_valid_combination(row):
    """
    Should return True if combination is valid and False otherwise.
    
    Test row that is passed here can be incomplete.
    To prevent search for unnecessary items filtering function
    is executed with found subset of data to validate it.
    """
    
    n=len(row)
    if n>=len(parameters):
        return True

        
    return True

def update_expected_result(row):

    if row['cpu_load'] == 'HIGH' and row['feature_switch']=='ON' and row['license_status']=='ON':
        row['expected_result']='alarm_reported'
    else:
        row['expected_result']='alarm_not_reported'

if __name__=='__main__':
    output='''ZDDS:ICSU,1;

LOADING PROGRAM VERSION 7.74-0

WELCOME TO SERVICE TERMINAL DIALOGUE

0016-MAN>ZAUL


/*** SYNTAX ERROR: 16718 ***/
/*** THE SESSION IS TO BE CLOSED ***/

COMMAND EXECUTED
'''
    import re
    res = re.search('\*\*\* ((SYNTAX|SEMANTIC) ERROR|UNKNOWN COMMAND)', output)
    test = testObject('shuyolin')
    test.name = 'testname'
    test.sex = 'male'
    print test,dir(test)
    print getattr(test,'sex')
    print getattr(test,'name')


    

    

    

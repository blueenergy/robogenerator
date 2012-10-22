from IpaMml.helper import _run_keyword as kw
from robot.libraries.BuiltIn import BuiltIn

builtin = BuiltIn()
def _unit_should_be_in_state(unit_name,state):
    res = kw('Get units',unit_name)
    builtin.should_be_equal_as_strings(res[0].state, state)
    
def _restart_unit(unit):
    kw('Restart unit')
    
    
def _change_unit_state(unit_name,state,mode='',answer='N'):
    unit_type,unit_index = unit_name.split('-')
    command_string = 'ZUSC:%s,%s:%s::%s;' %(unit_type,unit_index,state,mode)
    print command_string
    result = kw('Execute MML',command_string,answer)
    print result


def _change_unit_state_anyway(unit_name,state):
    try:
        _change_unit_state(unit_name,state)
    except:
        print 'exception happened ,%s'
        result = _change_unit_state(unit_name,state,'FCD','Y')
        print result
        
def change_unit_state_and_check_result(unit_name,state):
    _change_unit_state_anyway(unit_name,state)
    kw('Unit Should Be In State',unit_name,state)

def wait_unit_in_required_state(unit_name,state):
    kw('Wait Until Units Are In State',unit_name,'both','Not Care','3min',state)

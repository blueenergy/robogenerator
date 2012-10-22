documentation ='''The case is to test drink effect on people depend on type of drink and amount'''

suite_setup ='Prepare to Drink'
suite_teardown='Finish Drink'
test_setup ='Clear Own Stomach'
test_teardown = 'collect blood pressure and  pulse during drink'
force_tags ='''owner-shuyolin  phase-RT  req-PRS_None_Req'''
resource ='Resource.html'
#library ='#{RESOURCE_PATH}/*.py'

parameters_template = {'drink_type': [ "water","wine","beer","cocacola","juice","whitewine"]
             , 'amount':[ 1,2,3,4]
             , 'appliance':['bottle','cup','goblet','mug']
             , 'expected_result':["EMPTY"]        
             }
#'expected_result':["drunken","stomachache","health","full","tipsy"] 
parameters = parameters_template
output_filename ='NEW_Restart_all_kinds_of_Unit_Test.txt'
#case_name_template = 'drink ${amount} ${appliance} of ${drink_type} and expected_result is ${expected_result}'
case_name_template = 'people drink test'
case_step_template = '''${drink_type}  ${amount}  ${appliance}  ${expected_result}'''
keyword_template = '''people drink test'''
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
        if row['drink_type'] =='wine' and row['appliance'] != 'goblet':
            return False
        if row['drink_type'] == 'beer' and row['appliance'] != 'mug':
            return False
        if row['drink_type'] == 'water' and row['appliance'] != 'bowl':
            return False
        if row['drink_type'] == 'cocacola' and row['appliance'] not in ['bottle']:
            return False
        if row['drink_type'] == 'whitewine' and row['appliance'] not in ['cup']:
            return False
        if row['drink_type'] == 'juice' and row['appliance'] not in ['cup']:
            return False 

    return True


def update_expected_result(row):
    if row['drink_type'] in ['wine']:
        if row['amount'] == 4:
            row['expected_result'] = 'drunken'
        else:
            row['expected_result'] = 'tipsy'

        
    elif row[ 'drink_type'] in ['beer'] and row ['amount'] == 4:
        row['expected_result'] = 'stomachache'


    elif row[ 'drink_type'] in ['whitewine']:
        if row ['amount'] == 1:
            row['expected_result'] = 'health'
            
        elif row ['amount'] == 2:
            row['expected_result'] = 'tipsy'
            
        elif row ['amount'] == 3:
            row['expected_result'] = 'drunken'
        else:
           row['expected_result'] = 'headache' 
     
        
    elif row[ 'drink_type'] in ['water'] and row ['amount'] >= 4:
        row['expected_result'] = 'full'

    else:
        row['expected_result'] = 'health'

if __name__=='__main__':

    pass



        
        
  




        

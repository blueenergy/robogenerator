documentation ='''The case is to do login test'''
suite_setup ='Open Browser  ${LOGIN_PAGE_URL}   googlechrome'
suite_teardown='Close Browser'
test_setup ='Go to  ${LOGIN_PAGE_URL}'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''

library ="SeleniumLibrary"

variables ='''
${USERNAME_FIELD}  username_field
${PASSWORD_FIELD}  password_field
${LOGIN_BUTTON}    LOGIN
${VALID_USERNAME}  demo
${VALID_PASSWORD}  mode
${LOGIN_PAGE_URL}  http://localhost:7272/html/
'''
keyword_table ='''
Submit Credentials
  Input Text      ${USERNAME_FIELD}  ${USERNAME}
  Input Password  ${PASSWORD_FIELD}  ${PASSWORD}
  Click Button  ${LOGIN_BUTTON}
'''


parameters_template = {'username': ['demo','mode','invalid123','${EMPTY}']
             , 'password':['mode','demo','password123','${EMPTY}']            
             }
parameters = parameters_template
output_filename ='NEW_LOGIN_Test.txt'

case_name_template = 'TestCase'


def get_case_steps(action_name,row):

    welcome_page_state = {'name':'welcome_page',
              'step':'Welcome Page Check'
              }
    error_page_state = {'name':'error_page',
              'step':'Error Page Check'
              }
    
    login_page_state = {'name':'login_page',
              'step':'Login Page Check',
              'actions':{'Submit Credentials':welcome_page_state if row['username']=='demo' and row['password']=='mode' else error_page_state}
              }


    state_graph = [login_page_state,welcome_page_state,error_page_state]
    starting_state_name = 'login_page'
    for state in state_graph:
        print state['step']
        print state['actions']['Submit Credentials']['step']

def is_valid_combination(row):
     
    n=len(row)
    if n>=len(parameters):
        return True
    return True


    

if __name__=='__main__':

    pass




        
        
  




        

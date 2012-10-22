
documentation ='''The case is to do file behavior test  in cost-effective way'''
suite_setup ='Connect to SUT'
suite_teardown='Disconnect from SUT'
force_tags ='''owner-shuyolin  team-AreaCI  phase-RT  requirement-area-SS  req-PRS_None_Req'''
test_setup ='Connect to SUT'
test_teardown='Disconnect from SUT'

output_filename ='file_behavior.html'
case_name_template = 'file behavior'

parameters = {'filename': ["test_file"]            
             }
#parameters = areaci_common.update_parameters_according_to_enviorment(parameters_template)


def state_should_be():
    pass
def delete():
    pass
def create():
    pass

def select_all():
    pass

def invert_selection():
    pass
zero_file=one_selected_file=one_unselected_file={}

zero_file = {'name':'zero_file',
          'actions':[(invert_selection,('',),None,'zero_file'),
                     (create,('${filename}',),None,'one_selected_file'),
                     (select_all,('',),None,'zero_file')]}
		  
one_selected_file = {'name':'one_selected_file',
          'actions':[(invert_selection,('',),None,'one_unselected_file'),
                     (delete,('${filename}',),None,'zero_file'),
                     (select_all,('',),None,'one_selected_file')]
          }
one_unselected_file = {'name':'one_unselected_file',
          'actions':[(invert_selection,('',),None,'one_selected_file'),
                     (select_all,('',),None,'one_selected_file')]
          }


state_graph = [zero_file,one_selected_file,one_unselected_file]


accepting = state_graph
initial = 'zero_file'

#graph = get_all_possible_transitions(state_graph)

if __name__=='__main__':
    pass


from __future__ import with_statement
from string import Template
import random
from dynamic_transition import generate_sequence_map
#
   
class CaseGenerator(object):
    def __init__(self,case_instance,data_instance):
        self.case_instance = case_instance
        self.data_instance = data_instance
                
    def write_case_header(self,out):
        print self.case_instance.documentation
        out.write('*** Settings ***\n')
        out.write('''Documentation  %s\n''' % self.case_instance.documentation)
        out.write('Suite Setup  %s\n' % self.case_instance.suite_setup)
        out.write('Suite Teardown  %s\n' % self.case_instance.suite_teardown)
        out.write('Test Setup  %s\n' % self.case_instance.test_setup)
        out.write('Test teardown  %s\n' % self.case_instance.test_teardown)
        if self.case_instance.force_tags:
            if self.data_instance.max_combinations:
                kwargs = self.data_instance.max_combinations[0]
                force_tags = Template(self.case_instance.force_tags).substitute(**kwargs)
            else:
                force_tags = self.case_instance.force_tags
            out.write('Force Tags  %s\n' % force_tags)
        out.write('Resource  %s\n' % self.case_instance.resource)
        out.write('Library  %s\n' % self.case_instance.library)
        
    def write_case_column_header(self,out,case_step_template,style):

        if style == 'normal':
            #args = case_step_template.replace('${', '').replace('}', '').split('  ')[1:]
            #column_hearder = '  '.join(args)
            out.write('*** Test Cases ***  step\n')
        else:
            args = case_step_template.replace('${', '').replace('}', '').split('  ')[:]
            column_hearder = '  '.join(args)
            out.write('*** Test Cases ***  %s\n' % column_hearder)
        
    def write_atdd_case_content(self,out,valid_combinations, case_step_template, case_tag_template,tag_written_flag):

        for line in valid_combinations:
            kwargs = line
            tags = Template(case_tag_template).substitute(**kwargs) if case_tag_template else None
            if tags and not tag_written_flag:
                out.write('    [Tags]  %s\n' % tags)
                tag_written_flag = True

            step = Template(case_step_template).substitute(**kwargs)
            out.write('    %s\n' % step)
    
    
    def write_normal_data_driven_case_content(self, out, valid_combinations, case_name_template, case_step_template, case_tag_template):
        for line in valid_combinations:
            kwargs = line
            tags = Template(case_tag_template).substitute(**kwargs) if case_tag_template else None
            testcase_name = Template(case_name_template).substitute(**kwargs)
            steps = Template(case_step_template).substitute(**kwargs)
            out.write('%s\n' % testcase_name)
            if tags:
                out.write('    [Tags]  %s\n' % tags)
            for step in steps.splitlines():
                out.write('    %s\n' % step.strip())

class DataDrivenCaseGenerator(CaseGenerator):
    
    def __init__(self,case_instance,data_instance,case_style):
        CaseGenerator.__init__(self, case_instance, data_instance)
        self.case_style = case_style
    
    def generate_case(self,output_filename,case_count):
        if self.case_style =='normal':
            self.generate_normal_style_case(output_filename,case_count)
        elif self.case_style =='atdd':
            self.generate_atdd_style_case(output_filename,case_count)

    def generate_normal_style_case(self,output_filename,case_count):
        self.data_instance.generate_combinations(case_count)
        valid_combinations = self.data_instance.update_combination()
        name_template = self.case_instance.case_name_template
        step_template = self.case_instance.case_step_template
        tag_template = self.case_instance.subcase_tag_template
        
        with open(output_filename, 'w') as out:

            self.write_case_header(out)
            self.write_case_column_header(out,step_template,'normal')
            self.write_normal_data_driven_case_content(out, valid_combinations, name_template, step_template, tag_template)
            
    def generate_atdd_style_case(self,output_filename,case_count):
        self.data_instance.generate_combinations(case_count)
        valid_combinations = self.data_instance.update_combination()
        step_template = '  '.join(self.case_instance.case_step_template.split('  ')[1:])
        tag_template = self.case_instance.subcase_tag_template
        tag_written_flag = False
        testcase_name = self.case_instance.case_name_template
        template_keyword = self.case_instance.case_step_template.split('  ')[0]
        
        with open(output_filename, 'w') as out:
            self.write_case_header(out)
            self.write_case_column_header(out,step_template,'atdd')
            out.write('%s\n'%testcase_name)
            out.write('    [Template]  %s\n' %template_keyword)
            print valid_combinations
            self.write_atdd_case_content(out,valid_combinations,step_template,tag_template,tag_written_flag)
                
                
class StateMachineCaseGenerator(CaseGenerator):
    def __init__(self,case_instance,data_instance,state_graph):
        CaseGenerator.__init__(self, case_instance, data_instance)
        self.state_graph = state_graph
        self.state_name_list = [state.name for state in self.state_graph]
        #print self.state_name_list
        self.all_transitions = self.get_all_possible_transitions()
        print ' All possibles transitions to be tested is %s' %len(self.all_transitions)
        print self.all_transitions
        self.all_possible_path = generate_sequence_map(self.all_transitions)
        print ' All possibles paths to be tested is %s' %len(self.all_possible_path)
        self.tested_transitions =[]
        
    def record_tested_transitions(self,transition):
        if transition not in self.tested_transitions:
            self.tested_transitions.append(transition)
            
    def get_tested_transitions(self):
        return self.tested_transitions
    
    def get_tested_nodes(self):
        tested_nodes =[]

        for transition in self.tested_transitions:
            tested_nodes.append(transition[0])
            tested_nodes.append(transition[-1])
        return set(tested_nodes)
            
            
    def print_diff_with_all_transitions(self,tested_transitions):
        print tested_transitions
        print self.all_transitions
        diff = set(self.all_transitions).difference(set(tested_transitions))
        if diff:
            print "following transitions not covered"
            for transition in diff:
                print transition
        else:
            print "all possible transitions have been tested"


    def get_kwargs(self):
        if hasattr(self.data_instance, 'max_combinations'):
            kwargs = random.choice(self.data_instance.max_combinations)
        else:
            kwargs = {}
        return kwargs

    def get_state_by_name(self,name):
        for state in self.state_graph:
            if state.name == name:
                return state
        return None
        
        
    def get_all_possible_transitions(self):
        all_transitions = []
        for state in self.state_graph:
            #print state
            current_state = state.name
            actions = state.available_actions()
            for (aname,args,model_result,next_state) in actions:
                action_name = aname if type(aname) == type(' ') else aname.__name__
                all_transitions.append((current_state,(action_name,args),next_state))
        #print all_transitions
        return all_transitions
    
    def generate_case(self,output_filename,case_count,nsteps,strategy,case_style=''):

        
        if strategy == 'DataDriven':
            if case_style == 'normal':
                self.generate_normal_data_driven_case(output_filename,case_count)
            else:
                self.generate_atdd_data_driven_case(output_filename,case_count)
        
        elif strategy =='ShortestPath':
            from graph_algorithm.shortest_path import compute_cpp_optimal_route
            
            
            self.optimized_transitions = compute_cpp_optimal_route(self.state_name_list,self.all_transitions)
            print "Shortest path to cover all transition has %s transitions to cover" % len(self.optimized_transitions)
            for transition in self.optimized_transitions:
                #print transition
                self.record_tested_transitions(transition)
            self.generate_mbt_case_by_transitions(output_filename,self.optimized_transitions)
        elif strategy in ['StateCoverage','ActionNameCoverage','DynamicRandom']:
            self.generate_dynamic_mbt_style_case(output_filename,case_count,nsteps,strategy)
        else:
            raise Exception,"not supported strategy name"
    



    def write_transition_to_case(self, required_transitions, out):
        for transition in required_transitions:
            state = self.get_state_by_name(transition[0])
            state.write_steps(out)
            action_name, action_argument = transition[1][0], transition[1][1]
            #print action_argument
            case_step = action_name + '  ' + '  '.join(action_argument)
            out.write('  %s\n' % case_step)

    def generate_mbt_case_by_transitions(self,output_filename,required_transitions):

        with open(output_filename, 'w') as out:
            self.write_case_header(out)
            out.write('*** Test Cases ***  \n')

            valid_combinations = self.data_instance.max_combinations
            #case_name = '%s\n'%self.case_instance.case_name_template
            if len(valid_combinations)>=1:
                for valid_combination in valid_combinations:
                    print '***********'
                    print valid_combination
                    case_name = Template(self.case_instance.case_name_template).substitute(**valid_combination)
                    out.write(case_name)
                    case_setup = Template(self.case_instance.test_setup).substitute(**valid_combination)
                    out.write('  [Setup]  %s\n' % case_setup)
                    self.write_transition_to_case(required_transitions, out)
            else:
                out.write(self.case_instance.case_name_template)
                case_setup = self.case_instance.test_setup
                out.write('  [Setup]  %s\n' % case_setup)
                self.write_transition_to_case(required_transitions, out)
                
    def generate_normal_data_driven_case(self,output_filename,case_count):

        starting_state_name = self.state_graph[0].name
        starting_state = self.get_state_by_name(starting_state_name)
        step_template = '\n'.join(starting_state.get_steps())
        with open(output_filename, 'w') as out:
            self.write_case_header(out)
            self.write_case_column_header(out,step_template,'normal')
            self.data_instance.generate_combinations(case_count)
            valid_combinations = self.data_instance.update_combination()
            #print len(valid_combinations)
            name_template = self.case_instance.case_name_template
            tag_template = self.case_instance.subcase_tag_template
            self.write_normal_data_driven_case_content(out, valid_combinations, name_template, step_template, tag_template)



    def generate_atdd_data_driven_case(self,output_filename,case_count):

        
        case_count = case_count
        state_name = self.state_graph[0].name
        state = self.get_state_by_name(state_name)
        name_template = self.case_instance.case_name_template
        step_template = '  '.join(state.get_step_argument())
        tag_template = self.case_instance.subcase_tag_template

        self.data_instance.generate_combinations(case_count)
        
        valid_combinations = self.data_instance.update_combination()

        subcase_tag_written = False
        with open(output_filename, 'w') as out:
            self.write_case_header(out)
            self.write_case_column_header(out,step_template,'atdd')
            out.write('%s\n'%name_template)
            template ='    [Template]  %s' %state.get_step_name()
            out.write('%s\n'%template)
            self.write_atdd_case_content(out,valid_combinations,step_template, tag_template, subcase_tag_written)


    def get_transitions_according_to_strategy(self,starting_state,strategy,max_step_count):
        state = starting_state
        test_step_count = 0
        transitions =[]
        while test_step_count < max_step_count:
            action = state.get_next_action(strategy)
            if action:
                transition = (state.name,(action.name,action.argument),action.next_state_name)
                transitions.append(transition)
                self.record_tested_transitions(transition)
                state =  self.get_state_by_name(action.next_state_name)
            else:
                break
            test_step_count += 1
        return transitions
    
    

    def generate_dynamic_mbt_style_case(self,output_filename,case_count,nsteps,strategy):
        
        
        starting_state_name = self.state_graph[0].name
        starting_state = self.get_state_by_name(starting_state_name)
        max_step_count = nsteps if nsteps else 50

        required_transitions = self.get_transitions_according_to_strategy(starting_state,strategy,max_step_count)
        self.print_diff_with_all_transitions(self.tested_transitions)
        self.generate_mbt_case_by_transitions(output_filename,required_transitions)
            

            


        



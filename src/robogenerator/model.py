
from data_algorithm.dfs_pairs import get_valid_dfs_dict_combinations
from data_algorithm.random_pairs import get_valid_random_combinations
from data_algorithm.all_pairs import get_all_pairs
import random
import os
import pickle 
from types import MethodType, FunctionType
from string import Template
import strategy.ActionNameCoverage as ActionNameCoverage
import strategy.StateCoverage as StateCoverage
import strategy.RandomCoverage as RandomCoverage
class DataModel(object):
    def __init__(self,config,algorithm):
        self.parameters = getattr(config,'parameters',None)
        self.algorithm = algorithm

        self.config = config
        self._validation_method = getattr(config,'is_valid_combination',lambda x: True)
        self._update_method = getattr(config,'update_expected_result',lambda t:t)
        if self.parameters:
            self.max_combinations = self.get_max_combinations()
        else:
            self.max_combinations =[]
        self.hostip = getattr(config,'hostip',None)
        self.filename = getattr(config,'filename',None)
        

        #print type(self.combinations)
        
            
    def update_combination(self):
        for combination in self.all_combination:
            #print combination.values()
            #print 'we got here'
            self._update_method(combination)
            #print '*****'
            #print combination.values()
        #print self.combinations
        return self.all_combination
    
    def get_max_combinations(self):
        return get_valid_dfs_dict_combinations(self.parameters,self._validation_method)
    

    def generate_combinations(self,case_count=1):
        
        
        
        if self.algorithm=='dfs':
            self.all_combination = get_valid_dfs_dict_combinations(self.parameters,self._validation_method)
            
        elif self.algorithm=='smart-random':
            cache_filename,previously_tested = self.get_cachefile_name_and_previously_tested()
            self.all_combination = get_valid_random_combinations(self.parameters,self._validation_method,case_count,previously_tested)
            self.cleanup_cache_file_if_all_combinations_tested(self.all_combination, cache_filename, previously_tested)
            
        elif self.algorithm=='random':

            self.all_combination = get_valid_random_combinations(self.parameters,self._validation_method,case_count)

        elif self.algorithm=='pairwise':
            attrs = self.parameters.keys()
            #print parameters,type(parameters)
            self.parameters[attrs[0]]= random.sample(self.parameters[attrs[0]],len(self.parameters[attrs[0]]))
            self.all_combination = get_all_pairs(self.parameters,self._validation_method)
            #print all_combination
            #print 'We got here'
        else:
            raise Exception,' Not supported algorithm'

        return self.all_combination
    def get_cachefile_name_and_previously_tested(self):
        if self.hostip:
            cache_filename = '%s_%s_previously_tested' % (self.hostip,self.filename)
        else:
            cache_filename = '%s_previously_tested' % self.filename
        #path = os.path.dirname(os.path.abspath(__file__))
        path = self.config.cachedir
        files = os.listdir(path)

        if cache_filename in files:
            f = open(os.path.join(path,cache_filename), 'r')
            previously_tested = pickle.load(f)
            f.close()
        else:
            previously_tested = []
        print "case count tested and recorded in cache file %s is %s" % (cache_filename, len(previously_tested))
        return cache_filename,previously_tested

    def cleanup_cache_file_if_all_combinations_tested(self, all_combination, cache_filename, previously_tested):
        plan_to_be_tested = [row.values() for row in all_combination]
        have_tested = plan_to_be_tested + previously_tested
        print "case actually will be tested in this round is %s" % len(plan_to_be_tested)
        print ' max combinations is %s' % len(self.get_max_combinations())
        if len(have_tested) >= len(self.max_combinations):
            have_tested = []
            print 'history cleared'
        path = self.config.cachedir
        f = open(os.path.join(path,cache_filename), 'w')
        pickle.dump(have_tested, f)
        f.close()


class StateModel(object):
    def __init__(self,state):
        self.state = state
        #print type(self.state)
        self.name = state['name']
        self._actions = state['actions'] if state.has_key('actions') else []
        #self.step= state['step'][0]
    def get_step_name(self):
        step = self.state['step']
        if type(step[0]) in [MethodType, FunctionType]:
            return ' '.join(step[0].__name__.split('_'))
        return step[0]
    def get_step_argument(self):
        return self.state['step'][1:]
    
    def write_steps(self,out,kwargs={}):
        case_steps = self.get_steps()
        for case_step in case_steps:
            case_step = Template(case_step).safe_substitute(**kwargs)
            out.write('  %s\n'%case_step)
        
    def get_steps(self):
        
        def processing_single_step(step, step_list):
            if type(step[0]) in [MethodType, FunctionType]:
                step_name = ' '.join(step[0].__name__.split('_'))
                step_argument = step[1:]
                step_list.append(step_name + '  ' + '  '.join(step_argument))
            else:
                step_name = step[0]
                step_argument = step[1:]
                step_list.append(step_name + '  ' + '  '.join(step_argument))

        step_list =[]

        step = self.state['step'] if self.state.has_key('step') else []
        if type(step) == type([]):
            for substep in step:
                processing_single_step(substep, step_list)
        elif type(step) == type(()):
            processing_single_step(step, step_list)

        return step_list

    
    
    def __name__(self):
        return self.state['name']
    

    def available_actions(self):
        result = []

        for raw_action in self._actions:

            if Action(raw_action).is_available():
                result.append(raw_action)
        return result
    
    def get_next_action(self,strategy):
        if strategy =='StateCoverage':
            select_action = StateCoverage.SelectAction
        elif strategy == 'ActionNameCoverage':
            select_action = ActionNameCoverage.SelectAction
        elif strategy =='DynamicRandom':
            select_action = RandomCoverage.SelectAction
        else:
            raise Exception,'unsupported action to select'
        
        next_action = select_action(self.available_actions())
        return Action(next_action)
        

class Action(tuple):

    def __init__(self, tuple_info):
        self.name = tuple_info[0].__name__ if type(tuple_info[0]) in [MethodType, FunctionType] else tuple_info[0]
        self.next_state_name = tuple_info[-1]
        self.argument = tuple_info[1] 
        self.condition = tuple_info[2]

    def is_available(self):
        if not self.condition:
            return True
        if self.condition and callable(self.condition) and self.condition():
            return True
        else:
            return False


    def write_step(self,out,kwargs={}):
        
        case_step = self.name+'  '+'  '.join(self.argument)

        case_step = Template(case_step).safe_substitute(**kwargs)
        #print case_step
        out.write('  %s\n'%case_step)



class CaseModel(object):
    def __init__(self,config):
        self.parameters = getattr(config,'parameters',None)
        self.documentation = getattr(config,'documentation',None)
        self.get_case_hearder_info(config)
        self.case_name_template = config.case_name_template
        self.subcase_tag_template = getattr(config,'subcase_tag_template',None)
        self.case_step_template =  getattr(config,'case_step_template',None)
        self.keyword_template = getattr(config,'keyword_template',None)
        
    def get_case_hearder_info(self, config):

        self.suite_setup = getattr(config,'suite_setup', None)
        self.suite_teardown = getattr(config, 'suite_teardown', None)
        self.test_setup = getattr(config, 'test_setup', None)
        self.test_teardown = getattr(config, 'test_teardown', None)
        self.force_tags = getattr(config, 'force_tags', None)
        self.resource = getattr(config, 'resource', None)
        self.library = getattr(config, 'library', None)


'''
        
class State(object):

    def __init__(self, name, steps, actions):
        self.name = name
        self.steps = steps or []
        self._actions = actions or []

    @property
    def actions(self):
        result = []
        names = set()
        for action in self._actions:
            if action.is_available() and action.name not in names:
                result.append(action)
                names.add(action.name)
        return result

    def write_steps_to(self, output):
        for step in self.steps:
            output.write(step+'\n')

    def write_to(self, output):
        if self.steps:
            output.write('  %s\n' % self.name)
        

class Action(object):

    def __init__(self, name, next_state, condition=None):
        self.name = name
        self._next_state_name = next_state
        self.condition = condition

    def set_machine(self, machine):
        self._machine = machine
        if not self.next_state:
            raise AssertionError('Invalid end state "%s" in '\
                                 'action "%s"!' %
                                 (self._next_state_name, self.name))

    @property
    def next_state(self):
        return self._machine.find_state_by_name(self._next_state_name)

    def is_available(self):
        if not self.condition:
            return True
        if self.condition == 'otherwise':
            return True
        return self.condition.is_valid(value_mapping=self._machine.variable_value_mapping)

    def write_to(self, output):
        if self.name:
            output.write('  %s\n' % self.name)
        self.next_state.write_to(output)
        

'''






if __name__=='__main__':
    #kw('Connect to IPA','10.68.145.148')
    #result = get_all_kind_of_pair_units()
    #print result
    #kw('Disconnect from IPA')
    pass

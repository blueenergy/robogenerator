import unittest
from PathModel import PathCollection 
class TransitionTestCase(unittest.TestCase):
    def test_transition_1(self):
        transition_1 = [('Idle','OFFHOOK','Init')]
        expected_result = [[('Idle','OFFHOOK','Init')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_1))

        
    def test_transition_2(self):
        transition_2 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','CALLING','Calling')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_2))
        
    def test_transition_3(self):
        transition_3 = [('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating')]
        expected_result = [[('Calling','TIMEOUTB','Terminating')],[('Calling','TIMEOUTA','Terminating')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_3))
        
    def test_transition_4(self):
        transition_4 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTB','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTA','Terminating')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_4))

    def test_transition_5(self):
        transition_5 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating'),
                        ('Calling','NORMAL','Ring')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTB','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTA','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','NORMAL','Ring')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_5))
        
    def test_transition_6(self):
        transition_6 = [('Idle','OFFHOOK','Init'),('Init','ONHOOK','Idle')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','ONHOOK','Idle')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_6))
        
    def test_transition_7(self):
        transition_7 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating'),
                        ('Calling','NORMAL','Ring'),('Calling','REJECT','Cancel')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTB','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTA','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','NORMAL','Ring')],
                            [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','REJECT','Cancel')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_7))
    def xtest_transition_8(self):
        transition_7 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating'),
                        ('Calling','NORMAL','Ring'),('Calling','REJECT','Cancel'),('Cancel','200CANCEL','WaitResponse')]
        expected_result = [[('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTB','Terminating')],
                            [('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTA','Terminating')],
                            [('OFFHOOK','Init'),('CALLING','Calling'),('NORMAL','Ring')],
                            [('OFFHOOK','Init'),('CALLING','Calling'),('REJECT','Cancel'),('200CANCEL','WaitResponse')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_7))
        
    def xtest_transition_9(self):
        transition_9 = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating'),
                        ('Calling','NORMAL','Ring'),('Calling','REJECT','Cancel'),('Cancel','200CANCEL','WaitResponse'),
                        ('WaitResponse','487INVITE','Idle')]
        expected_result = [(['OFFHOOK','CALLING','TIMEOUTB'],'Terminating'),(['OFFHOOK','CALLING','TIMEOUTA'],'Terminating'),
                           (['OFFHOOK','CALLING','NORMAL'],'Ring'),(['OFFHOOK','CALLING','REJECT','200CANCEL','487INVITE'],'Idle')]
        self.assertEqual(expected_result,generate_sequence_map(transition_9))
        
        
    def xtest_transition_a(self):
        transition_a = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating'),
                        ('Calling','NORMAL','Ring'),('Calling','REJECT','Cancel'),('Cancel','200CANCEL','WaitResponse'),
                        ('WaitResponse','487INVITE','Idle'),('Ring','200','Ready'),('Ring','REJECT','Idle'),
                        ('Ring','CANCEL','Cancel'),('Ready','BYE','Idle')]
        expected_result = [[('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTB','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','TIMEOUTA','Terminating')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling''NORMAL','Ring'),('Ring','200','Ready'),('Ready','BYE','Idle')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','NORMAL','Ring'),('Ring','REJECT','Idle')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','NORMAL','Ring'),
                             ('Ring','CANCEL','Cancel'),('Cancel','200CANCEL','WaitResponse'),('WaitResponse','487INVITE','Idle')],
                           [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),('Calling','REJECT','Cancel'),
                             ('Cancel','200CANCEL','WaitResponse'),('WaitResponse','487INVITE','Idle')]]
        
        actual_result = generate_sequence_map(transition_a)
        for sub_expected_result,sub_actual_result in zip(expected_result,actual_result):
            if sub_expected_result != sub_actual_result:
                for sub_sub_expected_result,sub_sub_actual_result in zip(sub_expected_result[0],sub_actual_result[0]):
                    if sub_sub_expected_result != sub_sub_actual_result:
                        print sub_sub_expected_result,'***',sub_sub_actual_result
                        break
        self.assertEqual(expected_result,generate_sequence_map(transition_a))
    def test_transition_loop_1(self):
        transition_loop_1 = [('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S1'),('S2','M3','S3')]
        expected_result = [[('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S1'),('S1','M1','S2'),('S2','M3','S3')],\
                           [('S0','M0','S1'),('S1','M1','S2'),('S2','M3','S3')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_loop_1))
        
    def xtest_transition_loop_2(self):
        transition_loop_2 = [('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S3'),('S3','MX','S1'),('S3','M4','S4')]
        expected_result = [[('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S3'),('S3','MX','S1'),('S1','M1','S2'),('S2','M2','S3'),('S3','M4','S4')],\
                           [('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S3'),('S3','M4','S4')]]
        self.assertEqual(expected_result,generate_sequence_map(transition_loop_2))


class GroupTransitionTestCase(unittest.TestCase):
    
    def test_transition_two_start_key(self):
        transition_two_start_key = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling')]
        expected_result = {'Idle':[('OFFHOOK','Init')],'Init':[('CALLING','Calling')]}
        self.assertEqual(expected_result,group_transition_by_begin_state(transition_two_start_key))
        
    def test_transition_one_start_key(self):
        transition_one_start_key = [('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating')]
        expected_result = {'Calling':[('TIMEOUTB','Terminating'),('TIMEOUTA','Terminating')]}
        self.assertEqual(expected_result,group_transition_by_begin_state(transition_one_start_key))
        
    def test_transition_two_path(self):
        transition_two_path = [('Idle','OFFHOOK','Init'),('Init','CALLING','Calling'),\
                        ('Calling','TIMEOUTB','Terminating'),('Calling','TIMEOUTA','Terminating')]
        expected_result = {'Idle':[('OFFHOOK','Init')],'Init':[('CALLING','Calling')],\
                           'Calling':[('TIMEOUTB','Terminating'),('TIMEOUTA','Terminating')]}
        self.assertEqual(sorted(expected_result),sorted(group_transition_by_begin_state(transition_two_path)))
        


def group_transition_by_begin_state(transitions):
    transition_group = {}
    for s,m,e in transitions:
        if s not in transition_group:
            transition_group[s] = [(m,e)]
        else:
            transition_group[s].append((m,e))
    return transition_group
        
def get_start_and_terminating_state_list(transitions):
    start_count = {}
    end_count = {}
    for s,m,e in transitions:
        if s not in start_count:
            start_count[s] = 1
        else:
            start_count[s] += 1
        if e not in end_count:
            end_count[e] = 1
        else:
            end_count[e] += 1
    #print start_count, end_count
    #start_state_list = [s for s in start_count if s not in end_count]
    start_state_list = [transitions[0][0]]
    print start_state_list
    terminating_state_list = [e for e in end_count if e == start_state_list[0] or e not in start_count]
    #terminating_state_list = [e for e in end_count if e not in start_count]
    print terminating_state_list

    return start_state_list,terminating_state_list
    

def get_all_path_for_one_state(all_path, num_of_path, state, transition_group, terminating_state_list):
    #print state,'*** %s' %all_path
    #print num_of_path
    #print state,'&&&',transition_group[state]
    #print all_path
    #cur_path = [x for x in all_path[-1][0]]
    #if all_path.check_circle_exist():
    #    all_path.close_path()
    #    return num_of_path

    for m,e in transition_group[state]:
        if e in terminating_state_list:
            all_path.close_path((state,m,e))
            #if all_path[-1][1]:
            #    all_path.append((cur_path+[(m,e)]))#create a new path, and close it
            #else:
            #    all_path[-1] = (cur_path+[(m,e)])#close a path which is under exploration
            #print state,all_path
        else:
##            if all_path[-1][1]:
##                all_path.append((cur_path+[(m,e)]))#create a new path
##            else:
##                all_path[-1][0].append((m,e))#append current state, and search continued
##            #print state,e,'*** %s' %all_path
            if all_path.check_circle_exist():
                #print 'circles found'

                continue
            all_path.extend_path((state,m,e))
            #num_of_path += 1
            num_of_path = get_all_path_for_one_state(all_path, num_of_path,e,transition_group, terminating_state_list)
    #if not all_path[-1][1]:
    #    all_path[-1][0].pop()
    #print '***'
    #print num_of_path


    all_path.end_state_search()
    return num_of_path


def generate_repeated_path(all_path,circles,repeat_times):
    pass
    
    
def generate_sequence_map(transitions):
    start_state_list,terminating_state_list = get_start_and_terminating_state_list(transitions)

    transition_group = group_transition_by_begin_state(transitions)
    #print transition_group['S3']
    #print terminating_state_list
    #print transition_group
    #print start_state_list,terminating_state_list
    s = start_state_list[0]
    all_path = PathCollection()
    num_of_path = 0
    #print transition_group[starting_state]
    for m,e in transition_group[s]:
        #all_path[num_of_path][0].append(m)
        if e in terminating_state_list:
            all_path.open_path((s,m,e))
            all_path.close_path()
            
        else:
            all_path.open_path((s,m,e))
            #num_of_path += 1
            num_of_path = get_all_path_for_one_state(all_path, num_of_path, e, transition_group, terminating_state_list)
        #print all_path
    #print all_path
    '''
    print all_path.circles
    original_path = all_path[0]
    for circle in all_path.circles:
        print circle[0]
        print circle
        index = all_path[0].index(circle[0])
        print index
        print '&&&&&&&&&&&'
        print all_path[0]
        original_path.insert(1, circle)

        for transition in circle:
            original_path.insert(index,transition)

        all_path.append(original_path)
    print all_path
    '''
    #message_list = [transition[1] for transition in transitions]
    #end_state_list = transitions[-1][2]
    #return [(x[0],x[1]) for x in all_path if x[1]]
    return all_path

if __name__ == '__main__':
    unittest.main()
    #transition_loop_2 = [('S0','M0','S1'),('S1','M1','S2'),('S2','M2','S3'),('S3','MX','S1'),('S3','M4','S4')]
    #result = generate_sequence_map(transition_loop_2)
    #print '***********'
    #print result

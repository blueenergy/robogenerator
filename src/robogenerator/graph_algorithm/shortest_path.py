
#import graph_algorithm.CPP as CPP
import random
import glob
import shutil
import os
'''
def compute_cpp_optimal_route(state_name_list,all_possible_transitions):
    G = CPP(len(state_name_list))
    print state_name_list
    for transition in all_possible_transitions:
        start = state_name_list.index(transition[0])
        end = state_name_list.index(transition[-1])
        arc_label = '%s->%s' %(start,end)
        G.addArc(arc_label,start,end,1)
        
    G.solve()
    G.printCPT(0)
    #print "Cost = %s"%G.cost()
    optimal_route = G.getAllTransitions()
    optimized_transition =[]
    for sub_route in optimal_route:
        start_state = state_name_list[sub_route[1]]
        end_state = state_name_list[sub_route[2]]
        sub_transition_list = [tran for tran in all_possible_transitions if tran[0] == start_state and tran[-1] == end_state]
        if len(sub_transition_list)>=3:
            raise Exception, 'multiple transition between two node exist %s' %sub_transition_list
        else:
            optimized_transition.append(random.choice(sub_transition_list))
    #print len(optimized_transition)
    return optimized_transition

'''




def get_current_java_version():
    java_version_info = os.getenv('JAVA_HOME','')

    if java_version_info.count('1.7') > 0:
        java_version = '1.7'
    elif java_version_info.count('1.6') > 0:
        java_version = '1.6'
    else:
        raise Exception, 'java seems not installed, pls install java at first to run this algorithm'
    return java_version

def compute_cpp_optimal_route(state_name_list,all_possible_transitions):

    arcs =[str(len(state_name_list))]
    print state_name_list
    for transition in all_possible_transitions:
        start = str(state_name_list.index(transition[0]))
        end = str(state_name_list.index(transition[-1]))
        arc_label = '%s->%s' %(start,end)
        arc =' '.join([arc_label,start,end,'1'])
        arcs.append(arc)
    #import subprocess
    from subprocess import list2cmdline
    import os
    current_path = os.path.abspath('.')

    os.chdir(os.path.dirname(__file__))
    java_version = get_current_java_version()
    os.chdir(java_version)
    command_args = ['java','CPP']
    command_args.extend(arcs)
    #p = subprocess.Popen(command_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    res = os.popen(list2cmdline(command_args))
    optimal_route =[]
    print '*******************'
    
    #print command_args
    #print ''.join(p.stdout.readlines())
    for line in res:
        temp = line.split()
        print temp
        if len(temp) == 7:
            optimal_route.append((temp[2],temp[4],temp[6]))


    optimized_transition =[]
    for sub_route in optimal_route:
        start_state = state_name_list[int(sub_route[1])]
        end_state = state_name_list[int(sub_route[2])]
        sub_transition_list = [tran for tran in all_possible_transitions if tran[0] == start_state and tran[-1] == end_state]
        if len(sub_transition_list)>3:
            raise Exception, 'multiple transition between two node exist %s' %sub_transition_list
        else:
            optimized_transition.append(random.choice(sub_transition_list))
    print len(optimized_transition)
    print optimized_transition
    os.chdir(current_path)
    return optimized_transition


if __name__=='__main__':
    java_version = get_current_java_version()

    files_to_copied = glob.glob('%s/*.class'%java_version)
    for class_file in files_to_copied:

        base_name = os.path.basename(class_file)
        shutil.copyfile(class_file, base_name)
    
    from subprocess import list2cmdline
    command_args =['java', 'CPP', '8', '"0->1 0 1 1"', '"0->6 0 6 1"', '"1->3 1 3 1"', '"1->0 1 0 1"',\
                    '"1-2 1 2 1"', '"2->6 2 6 1"', '"2->1 2 1 1"', '"3->4 3 4 1"', '"3->7 3 7 1"', '"4->5 4 5 1"',\
                '"4->6 4 6 1"', '"5->4 5 4 1"', '"6->4 6 4 1"', '"6->3 6 3 1"', '"7->6 7 6 1"', '"7->0 7 0 1"']
    
    command_args =['java', 'CPP', '8', '0->1 0 1 1', '0->6 0 6 1', '1->3 1 3 1', '1->0 1 0 1',\
                '1-2 1 2 1', '2->6 2 6 1', '2->1 2 1 1', '3->4 3 4 1', '3->7 3 7 1', '4->5 4 5 1',\
            '4->6 4 6 1', '5->4 5 4 1', '6->4 6 4 1', '6->3 6 3 1', '7->6 7 6 1', '7->0 7 0 1']
    #p = subprocess.Popen(command_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    #print '*******************'
    #print command_args
    #print ''.join(p.stdout.readlines())
    import os
    command_string = ' '.join(command_args)
    
    command_string = list2cmdline(command_args)
    print command_string
    '''
    #res = os.system(command_string)
    res = os.popen(command_string).readlines()
    print res
    '''



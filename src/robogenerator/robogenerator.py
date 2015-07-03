from __future__ import with_statement
import sys
import os
from generator import StateMachineCaseGenerator,DataDrivenCaseGenerator
from model import CaseModel,DataModel,StateModel
from robograph import generate_state_machine_graph

class RoboMachineParsingException(Exception):
    pass

def get_config_from_py_config_file(config_file):
    if config_file.endswith('py'):
        #config_file = config_file.split('.')[0]
        config_file = config_file.rstrip('.py')
    if config_file.count(os.sep):

        _g_module = config_file.split(os.sep)[-1]
        sys.path.append(config_file.split(_g_module)[0])
        config = __import__(_g_module)
        config.filename = _g_module
        
        #config_file_path = os.path.splitext(__file__)
        #print config_file_path
    else:
        #print config_file
        config = __import__(config_file)
        config.filename = config_file

    
    return config

def get_config_from_txt_config_file(config_file):
    #from robomachine_model import RoboMachine
    from robomachine.parsing import parse
    try:
        with open(config_file, 'r') as inp:
            machine = parse(inp.read())
    except IOError, e:
        sys.exit(unicode(e))
    except RoboMachineParsingException, e:
        sys.exit(1)
    pass
def main():
    import argparse
    parser = argparse.ArgumentParser(description='RoboGenerator 0.2 - a test data generator for Robot Framework',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('input', type=str, help='input file')

    parser.add_argument('--host', '-ip', type=str, default=None,
                        help='Pate IP address (default is None)')
    parser.add_argument('--variable','-v', type=str, default=None,
                        help='unit type to do operation',action='append')
    parser.add_argument('--output', '-o', type=str, default=None,
                        help='output file (default is input file with NEW prefix)')
    parser.add_argument('--tests_max', '-t',
                         type=int, default=1,
                         help='''maximum number of test to generate,
                         only useful in random strategy''')
    parser.add_argument('--percentage', '-p',
                         type=str, default=None,
                         help='''percentage of data combination to select,
                         only useful in random strategy''')
    parser.add_argument('--nsteps', '-n',
                         type=int, default=None,
                         help='maximum number of steps allowed in generated case \n'+\
                         'only useful in MBT style cases,default is 50')
    parser.add_argument('--strategy',
                         type=str, default='DynamicRandom',
                         help='used test generation strategy in MBT(default DynamicRandom)\n'+\
                         'StateCoverage = Select least covered State to test\n'+\
                         'ActionNameCoverage = Select least covered Action Name To cover\n'+\
                         'DynamicRandom = Randomly select next State but try to avoid already tested,\n'+
                         'if all possible transitions tested, randomly select one of them\n'+
                         'ShortestPath = cover all possible transition in least cost total path,need jython support\n')
    parser.add_argument('--style', '-s',
                         type=str, default='normal',choices =['normal','atdd'],
                         help='diffrent case style to choose\n'+
                          'only useful in data driven model cases'+ 
                          'atdd for template keyword like cases')
    parser.add_argument('--cachedir', '-c',
                         type=str, default=None,
                         help='''directory in server to store tested combinations''')

    parser.add_argument('--generation_algorithm', '-g',
                         type=str, default='pairwise', choices=['dfs', 'random','smart-random','pairwise'],
                         help='data driven generation algorithm (default pairwise)\n'+
                               'dfs = depth first search \n'+
                               'pairwise = Generate test in pairwise algorithm\n'+
                               'random = generate tests randomly\n'+
                               'smart-random = generate test randomly and\n'+ 
                               "don't repeat case already tested in last several rounds\n")
    
    parser.add_argument('--graph',
                         type=str, default=None,choices=['yes','no'],
                         help='''directory in server to store tested combinations''')
    
    args = parser.parse_args()
    print args.variable
    if args.host:
        os.environ['HOSTIP']= args.host
        
    config = get_config_from_py_config_file(args.input)
    
    if args.host:
        config.hostip = args.host
    
    output = args.output or config.output_filename
    algorithm = args.generation_algorithm
    nsteps = args.nsteps
    strategy = args.strategy
    case_count = args.tests_max
    percentage = args.percentage
    case_style = args.style
    graph_option = args.graph
    if not args.cachedir:
        if os.sep =='\\':
            config.cachedir = os.environ['APPDATA']+'\\'+'robogenerator'
        else:
            config.cachedir = os.environ['HOME']+'/'+'.robogenerator'
        
    else:
        config.cachedir = args.cachedir
    if not os.path.exists(config.cachedir):
        os.makedirs(config.cachedir)
        

    case_instance = CaseModel(config)
    data_instance = DataModel(config,algorithm)
    
    if getattr(config,'parameters',None) and not data_instance.get_max_combinations():
        return
    if percentage:
        #print 'calculate percentage'
        case_count = len(data_instance.get_max_combinations())* int(percentage)/100
    #state_instance = StateModel(config)
    
    output_format = output.split('.')[-1]
    output_filename = output.split('.')[0]
    raw_output = output_filename + '.' + 'txt'
    parameters = getattr(config,'parameters',None)
    if args.variable :
        for varible in args.variable:
            key = varible.split(':')[0]
            value = varible.split(':')[1].split()
            parameters[key] = value
    #print parameters
    state_graph = getattr(config,'state_graph',None)

    if state_graph:
        #print 'mbt only'
        state_instance_graph = [StateModel(state) for state in config.state_graph]
        #print state_instance_graph
        casegenerator = StateMachineCaseGenerator(case_instance,data_instance,state_instance_graph)
        casegenerator.generate_case(raw_output,case_count,nsteps,strategy,case_style)
        if graph_option:
            config.frontier =[]
            config.finished =casegenerator.get_tested_nodes()
            config.deadend =[]
            config.runstarts =[]
            config.tested_transitions = casegenerator.get_tested_transitions()
            generate_state_machine_graph(config,config.filename)
            from PIL import Image
            im = Image.open('%s.png'%config.filename)
            im.show()
    elif parameters:
        #print 'data-driven only '
        casegenerator = DataDrivenCaseGenerator(case_instance,data_instance,case_style)
        casegenerator.generate_case(raw_output,case_count)
    else:
        raise Exception,'no stat_graph or no parameters defined'
    

    print 'Case Generation Succeeded'
    if output_format != 'txt':
        from tidy import tidy_cli

        command_string = '--inplace --format %s %s' % (output_format, raw_output) #print command_string
        command_string_list = command_string.split(' ') 

        retcode = tidy_cli(command_string_list)
    

if __name__=='__main__':
    main()
    




    

 






        
        
  




        

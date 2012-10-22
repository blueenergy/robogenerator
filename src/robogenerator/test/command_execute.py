
from robot.libraries.OperatingSystem import OperatingSystem
os = OperatingSystem()
print dir()
def execute_command(model_filename,algorithm,case_no,strategy,style):
    #command_string = 'python ../runner.py %s -g %s -t %s --strategy %s'%(model_filename,algorithm,case_no,strategy)
    command_string = 'python ../runner.py %s'%model_filename
    if algorithm:
        command_string +=' -g %s'%algorithm
    if case_no:
       command_string +=' -t %s'%case_no
    if  strategy:
        command_string +=' --strategy %s'%strategy
        
    if  style:
        command_string +=' --strategy %s'%style
        
    print command_string
    rc,output = os.run_and_return_rc_and_output(command_string)
    return rc,output



if __name__=='__main__':
    rc,output = execute_command('..\\example\\FileBehavior\\file_behavior','','','ShortestPath')
    print rc,output
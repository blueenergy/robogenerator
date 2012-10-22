import subprocess

arcs =["4","aa 0 1 1","bb 0 2 1","cc 1 2 1","dd 1 3 1","ee 2 3 1","ff 3 0 1"]

#print len(arcs)
#print arcs
command_args = ['java','CPP']
command_args.extend(arcs)
#print command_args
p = subprocess.Popen(command_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
result =[]
for line in p.stdout.readlines():
    temp = line.split()
    #print temp
    if len(temp) == 7:
        result.append((temp[2],temp[4],temp[6]))
    #print line,
print result
retval = p.wait()
print retval

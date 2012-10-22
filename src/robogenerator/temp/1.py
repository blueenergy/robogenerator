'''
import pickle
f = open('1.txt','r')
combinations = pickle.load(f)
f.close()
print len(combinations)
temp_list =[]
for combination in combinations:
    print combination
    if combination in temp_list:
        raise Exception,'duplication happended %s' %combination
    temp_list.append(combination)
'''
a,b,c =(lambda t:t.split('-'))('a-b-c')
print a,b,c
class demo(object):
    def __init__(self,name):
        pass
    
    def print_something(self,info):
        print 'infomation is %s' %info
        print self.__str__
        
    def test_class(self):
        a=demo('lsy')
        a.print_something('hello world')
demo('lsy').test_class()
demo('lsy').print_something('hi world')
a=6
while a!=7:
    print 'info is correct'
    break
        

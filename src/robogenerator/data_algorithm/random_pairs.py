
def get_random_combination(parameters):

    new_line ={}
    import random
    r = random.Random()
    for sublist in parameters:
        new_line[sublist]=r.choice(parameters[sublist])
    return new_line

'''
def get_random_combination_with_count(parameters,count):
    i = 0
    all_combination=[]
    while i<count:
        new_line = get_random_combination(parameters)
        all_combination.append(new_line)
        i+=1
    return all_combination
'''     
    
def get_valid_random_combinations(parameters,filter_func = lambda x:True,case_count=1,previously_tested=[]):
    valid_combinations=[]
    valid_case_count = 0
    i =0
    #print previously_tested
    #print len(previously_tested)


    while valid_case_count<case_count and i < 10000:
        i+=1
        new_line = get_random_combination(parameters)
        #print filter_func,type(filter_func)
        if filter_func(new_line) and new_line not in valid_combinations and new_line.values() not in previously_tested :
            valid_combinations.append(new_line)
            #print new_line
            valid_case_count+=1

    return valid_combinations
        
if __name__=='__main__':
    parameters=[[],[],[],[]]
    parameters[0]=["ICSU","NPS1","NPS1P","NPGE","NPGEP","ISU"]
    parameters[1]=["WO-EX","SP-EX"]
    
    parameters[2]=["OPT","TOT","DSK"]
    parameters[3]=["RNC","MGW"]
    #parameters[4]=["SF20H","SF10"]
    #result = dfs_pair(parameters)
    #print len(result),result
    '''

    parameters[0]=["ICSU","NPS1"]
    parameters[1]=["WO-EX","SP-EX"]
    result = two_arrary_computation(parameters[0],parameters[1])
    for line in result:
        print line

    temp1= [['OMU','WO-EX'],['OMU','SP-EX'],['ICSU','WO-EX'],['ICSU','SP-EX']]
    temp2= ['OPT','TOT']
    result = two_arrary_computation(temp1,temp2)
    for line in result:
        print line
    

    result = get_random_combination(parameters)
    print result

    result = get_random_combination_with_count(parameters,10)
    print result
    '''
 


    result = get_valid_random_combinations(parameters,50)
    print result
    print len(result)



    '''
    result = get_valid_combinations(parameters,is_valid_combination)
    print result
    '''



    

  




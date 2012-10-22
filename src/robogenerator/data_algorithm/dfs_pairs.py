

def dfs_pairs(parameters):
    if len(parameters)==2:
        return two_arrary_computation(parameters[0],parameters[1])
    else:
        return two_arrary_computation(dfs_pairs(parameters[0:-1]),parameters[-1])




def two_arrary_computation(list0,list1):

    
    for element_0 in list0:
        for element_1 in list1:
            if isinstance(element_0,(basestring,int)):
                new_line = [element_0,element_1]
                yield new_line
            elif isinstance(element_0,list):
                new_line = element_0+[element_1]
                yield new_line

def get_valid_dfs_combinations(parameters,filter_func = lambda x:True):
    valid_combinations=[]
    result = dfs_pairs(parameters)
    for line in result:
        if filter_func(line):
            valid_combinations.append(line)
    return valid_combinations


def get_valid_dfs_dict_combinations(parameters_dict,filter_func = lambda x:True):
    if len(parameters_dict) ==1:
        return [parameters_dict]
    parameters_list = parameters_dict.values()
    #print list_parameters
    list_combinations = dfs_pairs(parameters_list)
    #print list_combinations
    attr_list = parameters_dict.keys()
    dict_combination_list =[]
    for list_combination in list_combinations:

        dict_combination ={}
        for key,value in zip(attr_list,list_combination):
            dict_combination[key] = value
            
        if filter_func(dict_combination):
            dict_combination_list.append(dict_combination)

    return dict_combination_list
if __name__=='__main__':
    parameters=[[],[],[],[],[]]
    parameters[0]=["ICSU","NPS1","NPS1P","NPGE","NPGEP","ISU"]
    parameters[1]=["WO-EX","SP-EX"]
    
    parameters[2]=["OPT","TOT","DSK"]
    parameters[3]=["RNC","MGW"]
    parameters[4]=["SF20H","SF10"]
    #result = dfs_pair(parameters)
    #print len(result),result
    '''
    parameters[0]=["ICSU","NPS1"]
    parameters[1]=["WO-EX","SP-EX"]
    result = two_arrary_computation(parameters[0],parameters[1])
    print len(result)
    temp1= [['OMU','WO-EX'],['OMU','SP-EX'],['ICSU','WO-EX'],['ICSU','SP-EX']]
    temp2= ['OPT','TOT']
    result = two_arrary_computation(temp1,temp2)
    '''

    

  




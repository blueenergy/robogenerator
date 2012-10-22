import metacomm.combinatorics.all_pairs2
all_pairs = metacomm.combinatorics.all_pairs2.all_pairs2


def get_all_pairs(parameters,validity_check_function='',previously_tested=[[]]):
    attrs = parameters.keys()
    print parameters
    pair_wise = all_pairs( parameters,validity_check_function,previously_tested)
    all_combination =[]
    for line in pair_wise:
        if line not in all_combination:
            all_combination.append(line)
        else:
            print 'Duplication happened, %s' %line
    #print len(all_combination)
    all_dict_combination =[]
    for combination in all_combination:
        dict_combination ={}
        for key,value in zip(attrs,combination):
            dict_combination [key] = value
        all_dict_combination.append(dict_combination)
    return all_dict_combination
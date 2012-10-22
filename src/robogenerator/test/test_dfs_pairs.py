import unittest
import sys
sys.path.append('../')
from dfs_pairs import get_valid_dfs_combinations,get_valid_dfs_dict_combinations
old_parameters = {'unit_type': [ "DMCU"]
             , 'state':[ "WO-EX"]
             , 'restart_mode':[ "OPT","TOT","DSK"]
             ,'restart_level':["master","slave"]
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
class DfsPairsTestCase(unittest.TestCase):
    def test_list_dfs_pairs_1(self):
        parameters_1 = [[ "DMCU"],["WO-EX"]]
        expected_result = [["DMCU","WO-EX"]]
        self.assertEqual(expected_result,get_valid_dfs_combinations(parameters_1))
    def test_list_dfs_pairs_2(self):
        parameters_1 = [[ "DMCU","TCU"],["WO-EX"]]
        expected_result = [["DMCU","WO-EX"],["TCU","WO-EX"]]
        self.assertEqual(expected_result,get_valid_dfs_combinations(parameters_1))

        
class DfsDictPairsTestCase(unittest.TestCase):
    def test_dict_dfs_pairs_1(self):
        parameters_1 = {'unit_type':["DMCU"],'state':["WO-EX"]}
        expected_result = [{'unit_type':"DMCU",'state':"WO-EX"}]
        self.assertEqual(expected_result,get_valid_dfs_dict_combinations(parameters_1))
        
    def test_dict_dfs_pairs_2(self):
        parameters = {'unit_type':['DMCU','TCU'],'state':["WO-EX"]}
        expected_result = [{'unit_type':"DMCU",'state':"WO-EX"},{'unit_type':"TCU",'state':"WO-EX"}]
        self.assertEqual(expected_result,get_valid_dfs_dict_combinations(parameters))

    def test_dict_dfs_pairs_3(self):
        parameters = {'unit_type':['DMCU','TCU'],'state':["WO-EX","SP-EX"]}
        expected_result = [{'unit_type':"DMCU",'state':"WO-EX"},{'unit_type':"DMCU",'state':"SP-EX"},
                           {'unit_type':"TCU",'state':"WO-EX"},{'unit_type':"TCU",'state':"SP-EX"}]
        self.assertEqual(expected_result,get_valid_dfs_dict_combinations(parameters))



    
if __name__ == '__main__':
    unittest.main()

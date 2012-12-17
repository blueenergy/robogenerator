import unittest
import sys
sys.path.append('../')
from data_algorithm.all_pairs import get_all_pairs
old_parameters = {'unit_type': [ "DMCU"]
             , 'state':[ "WO-EX"]
             , 'restart_mode':[ "OPT","TOT","DSK"]
             ,'restart_level':["master","slave"]
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
class PairwiseTestCase(unittest.TestCase):
    def test_pairwise_pairs_1(self):
        parameters_1 = {'unit_type': [ "DMCU"],'state':[ "WO-EX"]}
        expected_result = [{'unit_type': "DMCU",'state':"WO-EX"}]
        self.assertEqual(expected_result,get_all_pairs(parameters_1))
        
        
    def test_pairwise_pairs_2(self):
        parameters = {'a':['pikku_a', 'iso_a'],
               'b':['foo', 'bar']}
        expected_result = [{'a': "pikku_a",'b':"foo"},{'a': "iso_a",'b':"foo"}
                           ,{'a': "iso_a",'b':"bar"},{'a': "pikku_a",'b':"bar"}]
        self.assertEqual(expected_result,get_all_pairs(parameters))



if __name__ == '__main__':
    unittest.main()

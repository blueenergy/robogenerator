import unittest
import sys
sys.path.append('../')
from random_pairs import get_random_combination
old_parameters = {'unit_type': [ "DMCU"]
             , 'state':[ "WO-EX"]
             , 'restart_mode':[ "OPT","TOT","DSK"]
             ,'restart_level':["master","slave"]
             , 'element_type':["RNC"]
             , 'sfutype':["SF20H"]             
             }
class RandomPairsTestCase(unittest.TestCase):
    def test_random_pairs_1(self):
        parameters_1 = {'unit_type': [ "DMCU"],'state':[ "WO-EX"]}
        expected_result = {'unit_type': "DMCU",'state':"WO-EX"}
        self.assertEqual(expected_result,get_random_combination(parameters_1))



if __name__ == '__main__':
    unittest.main()

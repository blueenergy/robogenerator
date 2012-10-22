import unittest
class PathCollectionTestCase(unittest.TestCase):

    def setUp(self):
        self.pc = PathCollection()
        
    def xtest_empty(self):
        empty_path = PathCollection()
        self.assertEqual([],empty_path)

    '''

    def test_open_a_path(self):
        all_path = PathCollection()
        transition = ('OFFHOOK','Init')
        all_path.open_a_path(transition)
        self.assertEqual([[('OFFHOOK','Init')]],all_path)
        
        
    '''
    def xtest_close_path_before_open(self):

        transition = ('Idle','OFFHOOK','Init')
        self.pc.close_path(transition)
        self.assertEqual([],self.pc)
        
    def xtest_open_then_close(self):
        self.pc.open_path(('Idle','OFFHOOK','Init'))
        self.pc.close_path(('Init','CALLING','Calling'))
        self.assertEqual([[('Idle','OFFHOOK','Init'), ('Init','CALLING','Calling')]],self.pc)

    def xtest_close_current(self):
        self.pc.open_path(('Idle','OFFHOOK','Init'))
        self.pc.close_path()
        self.assertEqual([[('Idle','OFFHOOK','Init')]],self.pc)

    def xtest_extend_without_close(self):
        self.pc.open_path(('Idle','OFFHOOK','Init'))
        self.pc.extend_path(('Init','CALLING','Calling'))
        self.assertEqual([],self.pc)

    def xtest_extend_then_close(self):
        self.pc.open_path(('OFFHOOK','Init'))
        self.pc.extend_path(('CALLING','Calling'))
        self.pc.close_path(('TIMEOUTB','Terminating'))
        self.assertEqual([[('OFFHOOK','Init'), ('CALLING','Calling'),('TIMEOUTB','Terminating')]],self.pc)
        
    def xtest_open_then_close_close(self): 
        self.pc.open_path(('m1','S1'))
        self.pc.close_path(('m21','S21'))
        self.pc.close_path(('m22','S22'))
        self.assertEqual([[('m1','S1'),('m21','S21')],\
                          [('m1','S1'),('m22','S22')]],self.pc)

    def xtest_open_extend_then_close_close(self):
        self.pc.open_path(('m1','S1'))
        self.pc.extend_path(('m21','S21'))
        self.pc.close_path(('m3','S3'))
        self.pc.end_state_search()
        self.pc.close_path(('m22','S22'))
        self.assertEqual([[('m1','S1'),('m21','S21'),('m3','S3')],\
                          [('m1','S1'),('m22','S22')]],self.pc)

    def xtest_extend_path_3(self):
 
        all_path = PathCollection()
        all_path.close_path(('OFFHOOK','Init'))

        all_path.extend_path(('CALLING','Calling'))
        all_path.extend_path(('TIMEOUTB','Terminating'))
        all_path.extend_path(('TIMEOUTA','Terminating'))
        all_path.extend_path(('NORMAL','Ring'))
        all_path.extend_path(('200','Ready'))
        self.assertEqual([[('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTB','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTA','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('NORMAL','Ring'),('200','Ready')]],all_path)
        
    def xtest_extend_path_4(self):
 
        all_path = PathCollection()
        all_path.close_path(('OFFHOOK','Init'))
 
        all_path.extend_path(('CALLING','Calling'))
        all_path.extend_path(('TIMEOUTB','Terminating'))
        all_path.extend_path(('TIMEOUTA','Terminating'))
        all_path.extend_path(('NORMAL','Ring'))
        all_path.extend_path(('200','Ready'))
        all_path.extend_path(('BYE','Idle'))
        self.assertEqual([[('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTB','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTA','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('NORMAL','Ring'),('200','Ready'),('BYE','Idle')]],all_path)

    def xtest_extend_path_5(self):
 
        all_path = PathCollection()
        all_path.close_path(('OFFHOOK','Init'))
 
        all_path.extend_path(('CALLING','Calling'))
        all_path.extend_path(('TIMEOUTB','Terminating'))
        all_path.extend_path(('TIMEOUTA','Terminating'))
        all_path.extend_path(('NORMAL','Ring'))
        all_path.extend_path(('REJECT','IDLE'))
        self.assertEqual([[('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTB','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('TIMEOUTA','Terminating')],\
                          [('OFFHOOK','Init'),('CALLING','Calling'),('NORMAL','Ring'),('REJECT','IDLE')]],all_path)
        
    def xtest_check_circle_exist_path_minimal_circle(self):
        self.pc.open_path(('S0','M1','E1'))
        self.pc.extend_path(('E1','M2','E2'))
        self.pc.extend_path(('E2','M3','E1'))
        self.pc.extend_path(('E1','M2','E2'))
        
        self.assertTrue(self.pc.check_circle_exist())
        self.assertEqual([('E1','M2','E2'),('E2','M3','E1')],self.pc.get_circles())

    def test_check_circle_exist_path_big_circle(self):
        self.pc.open_path(('S0','M1','E1'))
        self.pc.extend_path(('E1','M2','E2'))
        self.pc.extend_path(('E2','M3','E4'))
        self.pc.extend_path(('E4','M4','E1'))
        self.pc.extend_path(('E1','M2','E2'))
        #print self.pc.current_path
        self.assertTrue(self.pc.check_circle_exist())
        self.assertEqual([('E1','M2','E2'),('E2','M3','E4'),('E4','M4','E1')],self.pc.get_circles())

    def xtest_check_circle_exist_path_two_independant_minimal_circle(self):
        self.pc.open_path(('S0','M0','S1'))
        self.pc.extend_path(('S1','MX','S0'))
        self.pc.extend_path(('S0','M0','S1'))
        self.pc.extend_path(('S1','M1','S2'))
        self.pc.extend_path(('S2','MX','S1'))
        self.pc.extend_path(('S1','M1','S2'))
        self.assertTrue(self.pc.check_circle_exist())
        #print self.pc.circles
        self.assertEqual([[('S0','M0','S1'),('S1','MX','S0')],[('S1','M1','S2'),('S2','MX','S1')]],self.pc.circles)
        
    def test_check_circle_exist_path_two_independant_middle_circle(self):
        self.pc.open_path(('S0','M0','S1'))
        self.pc.extend_path(('S1','MX','S0'))
        self.pc.extend_path(('S0','M0','S1'))
        self.pc.extend_path(('S1','M1','S2'))
        self.pc.extend_path(('S2','M2','S3'))
        self.pc.extend_path(('S3','M3','S4'))
        self.pc.extend_path(('S4','MX','S2'))
        self.pc.extend_path(('S2','M2','S3'))
        self.pc.extend_path(('S3','M3','S4'))
        self.pc.extend_path(('S4','M4','S5'))
        self.assertTrue(self.pc.check_circle_exist())
        print '************'
        print self.pc.circles
        print len(self.pc.get_circles())
        print '&&&&&&&&&&&&&'
        '''
        self.assertEqual([[('S0','M0','S1'),('S1','MX','S0')],\
                          [('S2','M2','S3'),('S3','M3','S4'),('S4','MX','S2')]],self.pc.circles)

        '''
        
        
    '''
    def test_close_path_2(self):
        original_path=[]
        m='OFFHOOK';e='Init'
        all_path = PathCollection()
        all_path.close_a_path(m,e)
        all_path.close_a_path(m,e)
        self.assertEqual([('OFFHOOK','Init')],all_path)
    '''
        
        
        
class PathCollection(list):
    def __init__(self):
        self.current_path = None
        self.circles = []
        
    def get_circles(self):

        duplicated_item = self.current_path[-1]
        #print self.current_path.index(duplicated_item)
        circles = self.current_path[self.current_path.index(duplicated_item):-1]

        return circles

    def get_temp_circles(self,path):

        duplicated_item = path[-1]
        circles = path[path.index(duplicated_item):-1]

        return circles

    def check_circle_exist(self):
        #print self.current_path
        check_result = False
        temp_path =[]
        #print self.current_path
        for subpath in self.current_path:
            temp_path.append(subpath)
            if temp_path[-1] in temp_path[0:-1]:
                self.circles.append(self.get_temp_circles(temp_path))
                check_result = True
        return check_result

    def open_path(self, transition):
        self.current_path = [(transition)]
        
    def extend_path(self, transition):
        #print transition
        #print self[-1][-1][-1]
        self.current_path.append(transition)
        #self.append(self[-1][:-1]+[transition])

    def close_path(self, transition=None):
        if not self.current_path:
            return
        
        if transition:
            self.append(self.current_path + [transition])
        else:
            self.append(self.current_path)
        self.current_path = self[-1][:-1]

    def end_state_search(self):
        self.current_path.pop()
    



if __name__ == '__main__':
    unittest.main()

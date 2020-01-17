'''
Created on 17-Jan-2020

@author: Srinivas Gunti
'''
import unittest
from main.model import Minesweeper


class ModelTest(unittest.TestCase):

    def setUp(self):
        self.model33 = Minesweeper(3)
        
    def testGetNeighborsCorners(self):
        '''
        +---+---+---+
        |o0 |x1 | 2 |
        +---+---+---+
        |x3 |x4 | 5 |
        +---+---+---+
        | 6 | 7 | 8 |
        +---+---+---+
        etc
        '''
        model = self.model33
        self.assertListEqual([1,3,4], list(model.get_neighbors(0)))
        self.assertListEqual([1,4,5], list(model.get_neighbors(2)))
        self.assertListEqual([3,4,7], list(model.get_neighbors(6)))
        self.assertListEqual([4,5,7], list(model.get_neighbors(8)))

    def testGetNeighborsEdges(self):
        '''
        +---+---+---+
        |x0 |o1 |x2 |
        +---+---+---+
        |x3 |x4 |x5 |
        +---+---+---+
        | 6 | 7 | 8 |
        +---+---+---+
        etc
        '''
        model = self.model33

        self.assertListEqual([0,2,3,4,5], list(model.get_neighbors(1)))
        self.assertListEqual([0,1,4,6,7], list(model.get_neighbors(3)))
        self.assertListEqual([1,2,4,7,8], list(model.get_neighbors(5)))
        self.assertListEqual([3,4,5,6,8], list(model.get_neighbors(7)))
        
    def testGetNeighborsCenter(self):
        '''
        +---+---+---+
        |x0 |x1 |x2 |
        +---+---+---+
        |x3 |o4 |x5 |
        +---+---+---+
        |x6 |x7 |x8 |
        +---+---+---+
        etc
        '''
        model = self.model33
        self.assertListEqual([0,1,2,3,5,6,7,8], list(model.get_neighbors(4)))



        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
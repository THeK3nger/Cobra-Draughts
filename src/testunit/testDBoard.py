'''
Created on Jul 29, 2011

@author: davide
'''
import unittest
from draughtscore.DBoard import DBoard
from draughtscore.DAction import DAction


class TestDBoard(unittest.TestCase):


    def setUp(self):
        self.board = DBoard()

    def tearDown(self):
        del self.board

    def testSetBitMap(self):
        self.board.set_bitmap(0, 1, 'DUMMY')
        self.assertEqual(self.board.get_piece(0, 1), 'DUMMY', "DUMMY Isn't where it should...")

    def testIsFree(self):
        self.assert_(self.board.is_free(4, 1))
        self.assert_(not self.board.is_free(0, 1))
        
    def testGetPiece(self):
        self.board.set_bitmap(0, 1, 'DUMMY')
        self.assertEqual(self.board.get_piece(0, 1), 'DUMMY', "DUMMY Isn't where it should...")
        
    def testApply(self):
        piece = self.board.get_piece(0, 1)
        action = DAction('MOVE', (0,1), (4,1))
        self.board.apply(action)
        self.assertEqual(self.board.get_piece(4,1), piece, "Wrong Move Effect.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
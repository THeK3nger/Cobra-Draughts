'''
Created on Jul 29, 2011

@author: Davide Aversa
'''
import unittest
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cobradraughts.core.DBoard import DBoard
from cobradraughts.core.DAction import DAction


class TestDBoard(unittest.TestCase):

    def setUp(self):
        self.board = DBoard()

    def tearDown(self):
        del self.board

    def testSetBitMap(self):
        '''Check correct behavior of set_bitmap method.'''
        self.board.set_bitmap(0, 1, 'DUMMY')
        self.assertEqual(self.board.get_piece(0, 1), 'DUMMY', "DUMMY Isn't where it should...")

    def testIsFree(self):
        '''Check if is_free recognizes free squares as free squares.'''
        self.assert_(self.board.is_free(4, 1))
        self.assert_(not self.board.is_free(0, 1))

    def testGetPiece(self):
        '''Check if get_piece returns right piece.'''
        self.board.set_bitmap(0, 1, 'DUMMY')
        self.board.set_bitmap(4, 3, 'DUMMY')
        self.assertEqual(self.board.get_piece(0, 1), 'DUMMY', "DUMMY Isn't where it should...")
        self.assertEqual(self.board.get_piece(4, 3), 'DUMMY', "DUMMY Isn't where it should...")

    def testApply(self):
        '''Check if apply_action applies action in a correct way.'''
        piece = self.board.get_piece(0, 1)
        action = DAction('MOVE', (0, 1), (4, 1))
        self.board.apply_action(action)
        self.assertEqual(self.board.get_piece(4, 1), piece, "Wrong Move Effect.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

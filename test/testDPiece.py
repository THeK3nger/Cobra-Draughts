'''
Created on Jul 29, 2011

@author: Davide Aversa
'''
import unittest
from draughtscore.DBoard import DBoard
from draughtscore.DAction import DAction


class TestDPiece(unittest.TestCase):
    
    def setUp(self):
        self.board = DBoard()
        self.piece = self.board.get_piece(0, 1)
        
    def tearDown(self):
        del self.piece
        del self.board

    def testPromotion(self):
        '''Check for piece promotion.'''
        self.piece.promote()
        self.assert_(self.piece.is_king, "Piece DO NOT PROMOTE!")
        
    def testDemotion(self):
        '''Check for piece demotion.'''
        self.piece.promote()
        self.piece.demote()
        self.assert_(not self.piece.is_king, "Piece DO NOT DEMOTE!")
        
    def testGetFeatures(self):
        '''Check for piece features.'''
        self.assert_(not self.piece.is_king, "Piece Must Not Be King.")
        flist = self.piece.get_features()
        print(flist)
        self.assert_('BACK' in  flist, "BACK is not in list!")
        self.assert_('PIECE' in  flist, "PIECE is not in list!")
        self.piece.promote()
        flist = self.piece.get_features()
        self.assert_(self.piece.is_king, "Piece Must Be King.")
        self.assert_('KBACK' in  flist, "KBACK is not in list!")
        self.assert_('KING' in  flist, "KING is not in list!")
    
    def testMove(self):
        '''Test Move. It's not a legal move but don't matter.'''
        target_pos = (5, 6)
        self.piece.move(5, 6)
        self.assertEqual(self.piece.position, target_pos)
        self.assert_(self.board.is_free(0, 1))
        self.assertEqual(self.piece, self.board.get_piece(5, 6))
    
    def testCaptured(self):
        '''Check the piece capture.'''
        self.piece.captured()
        self.assert_(self.board.is_free(0, 1))
        
    def testActionPromotion(self):
        '''Check promotion action.'''
        action = DAction('MOVE', (0, 1), (9, 1), promote=True)
        self.board.apply_action(action)
        self.assert_(self.piece.is_king)
        
    def testPossibleAction(self):
        '''Check if possible_action find all possible actions.'''
        action = self.piece.possible_action()
        self.assertEqual(len(action), 0, "Action list should be empty.")
        # TODO: Maybe can I expand this test. 
        # It is a bit optimistic... :D 

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

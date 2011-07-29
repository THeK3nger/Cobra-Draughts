'''
Created on Jul 29, 2011

@author: davide
'''
import unittest
from draughtscore.DAction import DAction


class TestDAction(unittest.TestCase):


    def setUp(self):
        self.action_move = DAction('MOVE',(0,1),(1,2))
        self.action_move_bis = DAction('MOVE',(0,1),(1,2))
        self.action_promote = DAction('MOVE',(0,1),(1,2),promote=True)
        self.action_capture = DAction('CAPTURE',(0,1),(2,3),captured='DUMMY')


    def tearDown(self):
        del self.action_move
        del self.action_promote
        del self.action_capture

    def testUndo(self):
        undo_move = self.action_move.undo()
        undo_promote = self.action_promote.undo()
        undo_capture = self.action_capture.undo()
        self.assertEqual(undo_move.destination, self.action_move.source, "Wrong Move Destination.")
        self.assertEqual(undo_move.source, self.action_move.destination, "Wrong Move Source.")
        self.assert_(undo_promote.promote)
        self.assertEqual(undo_capture.captured,'DUMMY')
    
    def testEquality(self):
        self.assertEqual(self.action_move, self.action_move_bis, "Woops! Not Equal.")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
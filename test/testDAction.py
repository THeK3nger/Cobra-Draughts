'''
Created on Jul 29, 2011

@author: Davide Aversa
'''
import unittest
import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cobradraughts.core.DAction import DAction


class TestDAction(unittest.TestCase):

    def setUp(self):
        self.action_move = DAction('MOVE', (0, 1), (1, 2))
        self.action_move_bis = DAction('MOVE', (0, 1), (1, 2))
        self.action_promote = DAction('MOVE', (0, 1), (1, 2), promote=True)
        self.action_capture = DAction('CAPTURE', (0, 1), (2, 3), captured='DUMMY')
        self.action_chain = DAction('CAPTURE', (0, 1), (1, 2))
        self.action_chain.next = DAction('CAPTURE', (1, 2), (2, 3))
        self.action_chain.next.next = DAction('CAPTURE', (2, 3), (3, 4))

    def tearDown(self):
        del self.action_move
        del self.action_promote
        del self.action_capture

    def testUndo(self):
        '''Check if undo returns a well-formed undo-action.'''
        undo_move = self.action_move.undo()
        undo_promote = self.action_promote.undo()
        undo_capture = self.action_capture.undo()
        self.assertEqual(undo_move.destination, self.action_move.source, "Wrong Move Destination.")
        self.assertEqual(undo_move.source, self.action_move.destination, "Wrong Move Source.")
        self.assertTrue(undo_promote.promote)
        self.assertEqual(undo_capture.captured, 'DUMMY')

    def testUndoChain(self):
        '''Check if undo returns well-formed undo action FOR CHAIN-CAPTURES.'''
        undo_chain = self.action_chain.undo()
        step0, step1, step2, step3 = (0, 1), (1, 2), (2, 3), (3, 4)
        self.assertEqual(undo_chain.source, step3, "Error in Step 3")
        self.assertEqual(undo_chain.destination, step2, "Error in Step 3")
        self.assertEqual(undo_chain.next.source, step2, "Error in Step 2")
        self.assertEqual(undo_chain.next.destination, step1, "Error in Step 2")
        self.assertEqual(undo_chain.next.next.source, step1, "Error in Step 1")
        self.assertEqual(undo_chain.next.next.destination, step0, "Error in Step 1")
        self.assertEqual(undo_chain.next.next.next, None, "Error in Termination")

    def testEquality(self):
        '''Check equality of two pieces.'''
        self.assertEqual(self.action_move, self.action_move_bis, "Woops! Not Equal.")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()

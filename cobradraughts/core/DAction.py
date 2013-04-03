#    This file is part of CobraDraughts.
#
#    CobraDraughts is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    CobraDraughts is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with CobraDraughts.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on Jul 21, 2011

@author: Davide Aversa
@version: 1.1

DAction module contains DAction class and related stuff.
'''

__author__ = "Davide Aversa"
__copyright__ = "Copyright 2011-2013"
__credits__ = ["Davide Aversa", ]
__license__ = "GPLv3"
__version__ = "1.1"
__maintainer__ = "Davide Aversa"
__email__ = "thek3nger@gmail.com"
__status__ = "Production"


class DAction(object):
    '''
    This Class represent an Action on the Draughts Board.

    Exists three type of action:
        * MOVE : Standard Move
        * CAPTURE : Capture Enemy Piece - Can be a Chain Capture.
        * UNDO : Undo Move
    '''

    def __init__(self, atype, source, destination, captured=None, promote=False):
        '''
        Constructor

        ARGS:
            @param atype: Action Type (Can be CAPTURE, MOVE or UNDO)
            @param source: Tuple (row,column) of starting position.
            @param destination: Tuple (row,column) of ending position.
            @param captured: Captured piece (if atype is CAPTURE).
        '''
        self.type = atype
        self.source = source
        self.destination = destination
        self.captured = captured
        self.promote = promote
        self.next = None  # Next Capture if `CAPTURE` is a Chain-Capture.

    def _append_capture(self, action):
        '''
        Append an item in Chain-Captures at the end of chain.

        ARGS:
            @param action: Action to append.
        '''
        p = self
        while p.next:
            p = p.next
        p.next = action

    def undo(self):
        '''
        Create Undo Action from current Action.

        RETURN:
            @return: Undo Action
        '''
        raw_undo = DAction('UNDO', self.destination, self.source, self.captured, self.promote)

        if self.next is None:  # Last element.
            return raw_undo

        undo_rest = self.next.undo()  # Invert chain tail.
        undo_this = raw_undo          # Invert current step.
        undo_rest._append_capture(undo_this)
        return undo_rest

    def copy(self):
        return DAction(self.type, self.source, self.destination, self.captured, self.promote)

    def __len__(self):
        return 1 + len(self.next) if self.next else 1

    def __eq__(self, other):
        if other is None:
            return False
        if self.type != other.type:
            return False
        if self.source != other.source:
            return False
        if self.destination != other.destination:
            return False
        if self.captured != other.captured:
            return False
        return True

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "%s :: <%d , %d> -> <%d , %d> { %s }" % (self.type, self.source[0],
                                                        self.source[1], self.destination[0],
                                                        self.destination[1],
                                                        str(self.next))

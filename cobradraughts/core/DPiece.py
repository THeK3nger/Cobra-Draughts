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

DPiece module contains DPiece class and related stuff.
'''

from cobradraughts.core.DAction import DAction

__author__ = "Davide Aversa"
__copyright__ = "Copyright 2011"
__credits__ = ["Davide Aversa", ]
__license__ = "GPLv3"
__version__ = "1.1"
__maintainer__ = "Davide Aversa"
__email__ = "thek3nger@gmail.com"
__status__ = "Production"


class DPiece(object):
    '''
    This class represent a Draughts Piece.
    '''

    def __init__(self, board, row, column, color):
        '''
        Constructor

        @param board: Board in which this piece exists.
        @param row: Starting Row.
        @param column: Starting Column.
        @param color: Piece color (LIGHT or DARK).
        '''
        self.board = board
        self.position = (row, column)
        self.is_king = False
        self.color = color

    def promote(self):
        '''
        Promote a Piece.
        '''
        self.is_king = True

    def demote(self):
        '''
        Promote a Piece.
        '''
        self.is_king = False

    def get_features(self):
        '''
        Get Features List. See DBoard total score for all Features List.
        '''
        features_list = []
        color = self.color
        row, column = self.position
        if not self.is_king:
            features_list = ['PIECE']
            if row < 4:
                if color == 'LIGHT':
                    features_list = ['PIECE', 'FRONT']
                else:
                    features_list = ['PIECE', 'BACK']
            if row >= 6:
                if color == 'LIGHT':
                    features_list = ['PIECE', 'BACK']
                else:
                    features_list = ['PIECE', 'FRONT']
            if (2 <= row < 8) and (2 <= column < 8):
                features_list.append('CENTER')
        else:
            features_list = ['KING']
            if row < 4:
                if color == 'LIGHT':
                    features_list = ['KING', 'KFRONT']
                else:
                    features_list = ['KING', 'KBACK']
            if row >= 6:
                if color == 'LIGHT':
                    features_list = ['KING', 'KBACK']
                else:
                    features_list = ['KING', 'KFRONT']
            if (2 <= row < 8) and (2 <= column < 8):
                features_list.append('KCENTER')
        return features_list

    def move(self, nrow, ncolumn):
        '''
        Move this piece.

        This method DO NOT perform any move control so, please, use
        valid move.

        ARGS:
            @param nrow: Destination Row
            @param ncolumn: Destination Column
        '''
        new_position = (nrow, ncolumn)
        self.board.set_bitmap(self.position[0], self.position[1], None)  # Update Bitmap
        self.board.set_bitmap(nrow, ncolumn, self)  # TODO: Is better update this on Dboard?
        self.position = new_position

    def captured(self):
        '''
        If a piece is captured by another piece then this one must disappear from
        board bitmap.
        '''
        self.board.set_bitmap(self.position[0], self.position[1], None)

    def _check_promote(self, drow):
        '''
        Check if, in one action, piece become King.
        '''
        if not self.is_king:
            if (self.color == 'LIGHT' and drow == 0) or (self.color == 'DARK' and drow == 9):
                return True
        return False

    def _possible_action_piece(self):
        '''
        Check for piece possible actions.
        '''
        ## Frequent Look-Up Avoiding
        ##
        is_free = self.board.is_free
        board = self.board
        ##

        move = []
        row, col = self.position
        capture = False  # True if piece can capture enemy piece
        if self.color == 'LIGHT':
            dr = -1  # Move UP
        else:
            dr = 1   # Move DOWN

        for dc in (-1, 1):
            if is_free(row + dr, col + dc):
                if not capture:
                    prom = self._check_promote(row + dr)
                    move.append(DAction('MOVE', (row, col), (row + dr, col + dc), promote=prom))
            elif is_free(row + 2 * dr, col + 2 * dc):
                obstruction = board.get_piece(row + dr, col + dc)
                if obstruction.color != self.color:
                    prom = self._check_promote(row + 2 * dr)
                    move.append(DAction('CAPTURE', (row, col), (row + 2 * dr, col + 2 * dc), obstruction, prom))
                    capture = True
        if capture:
            move_new = []
            for m in move:
                if m.type == 'CAPTURE':
                    # Check for chain captures.
                    board.apply_action(m)
                    next_steps = self.possible_action()
                    board.undo_last()
                    if next_steps and next_steps[0].type == 'CAPTURE':
                        for step in next_steps:
                            tmp = m.copy()
                            tmp.next = step
                            move_new.append(tmp)
                    else:
                        move_new.append(m)
            return move_new
        else:
            return move

    def _possible_action_king(self):
        '''
        Check King possible actions.
        '''
        ## Frequent Look-Up Avoiding
        ##
        is_free = self.board.is_free
        board = self.board
        ##

        move = []
        row, col = self.position
        capture = False
        direction = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        for dir in direction:
            trow = row + dir[0]
            tcol = col + dir[1]
            while is_free(trow, tcol):
                if not capture:
                    move.append(DAction('MOVE', (row, col), (trow, tcol)))
                trow += dir[0]
                tcol += dir[1]
            if board.is_free(trow + dir[0], tcol + dir[1]):
                obstruction = board.get_piece(trow, tcol)
                if obstruction.color != self.color:
                    move.append(DAction('CAPTURE', (row, col), (trow + dir[0], tcol + dir[1]), obstruction))
                    capture = True
        if capture:
            move_new = []
            for m in move:
                if m.type == 'CAPTURE':
                    # Check for chain captures.
                    board.apply_action(m)
                    next_steps = self.possible_action()
                    board.undo_last()
                    if next_steps and next_steps[0].type == 'CAPTURE':
                        for step in next_steps:
                            tmp = m.copy()
                            tmp.next = step
                            move_new.append(tmp)
                    else:
                        move_new.append(m)
            return move_new
        return move

    def possible_action(self):
        '''
        List all possible action for the piece.
        '''
        if self.is_king:
            return self._possible_action_king()
        else:
            return self._possible_action_piece()

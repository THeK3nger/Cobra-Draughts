'''
Created on Jul 21, 2011

@author: Davide Aversa
'''
from draughtscore.DAction import DAction

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
        if not self.is_king : 
            features_list.append('PIECE')
            if self.position[0] < 4 :
                if self.color == 'LIGHT' :
                    features_list.append('FRONT')
                else :
                    features_list.append('BACK')
            if self.position[0] >= 6 :
                if self.color == 'LIGHT':
                    features_list.append('BACK')
                else :
                    features_list.append('FRONT')
            if (2 <= self.position[0] < 8) and (2 <= self.position[1] < 8) :
                features_list.append('CENTER')
        else :
            features_list.append('KING')
            if self.position[0] < 4 :
                if self.color == 'LIGHT' :
                    features_list.append('KFRONT')
                else :
                    features_list.append('KBACK')
            if self.position[0] >= 6 :
                if self.color == 'LIGHT':
                    features_list.append('KBACK')
                else :
                    features_list.append('KFRONT')
            if (2 <= self.position[0] < 8) and (2 <= self.position[1] < 8) :
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
        self.board.set_bitmap(self.position[0], self.position[1], None) #Update Bitmap
        self.board.set_bitmap(nrow, ncolumn, self) #TODO: Is better update this on Dboard?
        self.position = new_position
            
    def captured(self):
        '''
        If a piece is captured by another piece then this one must disappear from 
        board bitmap. 
        '''
        self.board.set_bitmap(self.position[0], self.position[1], None)
        
    def _check_promote(self,drow):
        '''
        Check if, in one action, piece become King.
        '''
        if not self.is_king :
            if (self.color == 'LIGHT' and drow == 0) or (self.color == 'DARK' and drow == 9) :
                return True
        return False
            
    def _possible_action_piece(self):
        '''
        Check for piece possible actions.
        '''
        move = []
        row, col = self.position
        capture = False # True if piece can capture enemy piece.
        if self.color == 'LIGHT' :
            dr = -1 #Move UP
        else :
            dr = 1  #Move DOWN
            
        for dc in (-1, 1) :
            if self.board.is_free(row + dr, col + dc) :
                if not capture :
                    prom = self._check_promote(row + dr)
                    move.append(DAction('MOVE', (row, col), (row + dr, col + dc),promote=prom))
            elif self.board.is_free(row + 2 * dr, col + 2 * dc) :
                obstruction = self.board.get_piece(row + dr, col + dc)
                if obstruction.color != self.color :
                    prom = self._check_promote(row + 2 * dr)
                    move.append(DAction('CAPTURE', (row, col), (row + 2 * dr, col + 2 * dc), obstruction, prom))
                    capture = True
        if capture :
            move_new = []
            for m in move :
                if m.type == 'CAPTURE' :
                    move_new.append(m)
            return move_new
        else :
            return move

    def _possible_action_king(self):
        '''
        Check King possible actions.
        '''
        move = []
        row, col = self.position
        capture = False
        direction = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        for dir in direction :
            trow = row + dir[0]
            tcol = col + dir[1]
            while self.board.is_free(trow, tcol) :
                if not capture :
                    move.append(DAction('MOVE', (row, col), (trow, tcol)))
                trow += dir[0]
                tcol += dir[1]
            if self.board.is_free(trow + dir[0], tcol + dir[1]) :
                obstruction = self.board.get_piece(trow, tcol)
                if obstruction.color != self.color :
                    move.append(DAction('CAPTURE', (row, col), (trow + dir[0], tcol + dir[1]), obstruction))
                    capture = True
        if capture :
            move_new = []
            for m in move :
                if m.type == 'CAPTURE' :
                    move_new.append(m)
            return move_new
        return move
                
    def possible_action(self):
        '''
        List all possible action for the piece.
        '''
        if self.is_king :
            return self._possible_action_king()
        else :
            return self._possible_action_piece()
            
    
                

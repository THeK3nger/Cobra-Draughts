'''
Created on Jul 21, 2011

@author: Davide Aversa
'''
from draughtscore.DPiece import DPiece

class DBoard(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor. Inizialize an empty draughts board with 
        all the pieces in starting position.
        '''
        self.light_pieces = []
        self.dark_pieces = []
        self.bitmap = [None] * 50 # None = empty
        self.movelist = []
        
        # Add 20 Dark Piece in starting position.
        row = 0
        column = 1
        delta = 1
        for _ in range(20) :
            new_piece = DPiece(self, row, column, 'DARK')
            self.dark_pieces.append(new_piece)
            self.set_bitmap(row, column, new_piece)
            column += 2 
            if column > 9 :
                column -= (10 + delta)
                row += 1
                delta = -delta
        
        # Add 20 Light Piece in starting position.
        row = 6
        column = 1
        delta = 1
        for _ in range(20) :
            new_piece = DPiece(self, row, column, 'LIGHT')
            self.light_pieces.append(new_piece)
            self.set_bitmap(row, column, new_piece)
            column += 2 
            if column > 9 :
                column -= (10 + delta)
                row += 1
                delta = -delta
                
    def __cord2idx(self, row, column):
        '''
        Transform coordinate of the black-square in board into
        index in bitmap map.
        
        ARGS:
            @param row: Row.
            @param column: Column.
        
        RETURNS:
            @return: Index of <row,column> square in bitmap.
        '''
        idx = 5 * row
        if row % 2 == 0 :
            idx += (column - 1) / 2
        else :
            idx += column / 2
        return idx
            
    def set_bitmap(self, row, column, value):
        '''
        Set bitmap to value.
        
        ARGS:
         @param row: Row.
         @param column: Column.
         @param value: New value of bitmap.  
        '''
        self.bitmap[self.__cord2idx(row, column)] = value
        
    def is_free(self, row, column):
        '''
        Check if <row,column> square is empty.
        
        ARGS:
            @param row: Row.
            @param column: Column.
        
        RETURN:
            @return: True if square is free and on board.
        '''
        if (0 <= row < 10) and (0 <= column < 10) :
            idx = self.__cord2idx(row, column)
            if self.bitmap[idx] == None :
                return True
            else :
                return False
        else :
            return False
        
    def get_piece(self, row, column):
        '''
        Get piece in <row,column> square if any.
        
        ARGS:
            @param row: Row.
            @param column: Column.
            
        RETURN:
            @return: Reference to Piece in <row,column>
        '''
        return self.bitmap[self.__cord2idx(row, column)]
    
    def apply(self, action):
        '''
        Apply an action to the board.
        
        ARGS:
            @param action: Action to apply. 
        '''
        # If ACTION is UNDO-type DO NOT add to undo-list.
        if action.type != 'UNDO' :
            self.movelist.append(action)
            
        # Get Source and Destination.
        srow, scol = action.source
        drow, dcol = action.destination
        
        # Get Piece in Source.
        piece = self.get_piece(srow, scol)
        
        if piece == None : #If no piece is in source->ERROR.
            raise Exception("NO PIECE IN SOURCE!")
        
        piece.move(drow, dcol) #Move piece in destination.
        
        # Check Promotion
        if action.promote :
            piece.promote()
        
        if action.type == 'CAPTURE' :
            # If action is CAPTURE-type get captured piece. 
            captured = action.captured
            captured.captured() #Remove captured piece from board.
            if captured.color == 'LIGHT' : #... and fron right list.
                self.light_pieces.remove(captured)
            else :
                self.dark_pieces.remove(captured)
        elif action.type == 'UNDO' :
            # If action in UNDO-type 
            captured = action.captured
            if captured != None : # if exist captured piece then re-add.
                self.set_bitmap(captured.position[0], captured.position[1], captured)
                if captured.color == 'LIGHT' :
                    self.light_pieces.append(captured)
                else :
                    self.dark_pieces.append(captured)
            # Demote check! If source is a promote location and is_king
            # then piece must be demoted.
            if action.promote :
                piece.demote()
        
    def all_move(self, color):
        '''
        Get all possible move for a player
        
        ARGS:
            @param color: Player color.
        
        RETURN:
            @return: List of all possible action. 
        '''
        move = []
        capture = False
        if color == 'LIGHT' :
            for piece in self.light_pieces :
                move = move + piece.possible_action();
        else :
            for piece in self.dark_pieces :
                move = move + piece.possible_action();
                
        # Check if `move` contains a CAPTURE-action.
        for m in move :
            if m.type == 'CAPTURE' :
                capture = True
        
        # If this action exist then NO OTHER ACTIONS are allowed.
        # So we remove all action that are not CAPTURE-type.
        if capture :
            move_new = []
            for m in move :
                if m.type == 'CAPTURE' :
                    move_new.append(m)
            return move_new
        else :
            return move
                
    def board_score(self, weights):
        '''
        Static Evalutation Function for Draughts Board.
        
        ARGS:
            @param weights: Dictionary of Weights for each feature.
        
        RETURN:
            @return: The board score.
        '''
        vlight = {'PIECE':0,
          'KING':0,
          'BACK':0,
          'KBACK':0,
          'CENTER':0,
          'KCENTER':0,
          'FRONT':0,
          'KFRONT':0,
          'MOB':0}
        
        vdark = vlight.copy()
        
        # For each piece, for each feature add the total counter.
        for piece in self.light_pieces :
            features = piece.get_features()
            for f in features :
                vlight[f] += 1
        for piece in self.dark_pieces :
            features = piece.get_features()
            for f in features :
                vdark[f] += 1
                
        score_light = 0
        score_dark = 0
        for key in vlight.keys() : # Calculate weighted sum of features.
            score_light += vlight[key] * weights[key]
            score_dark += vdark[key] * weights[key]
        
        return score_light - score_dark # Return difference.
    
    def undo_last(self):
        '''
        Undo last action.
        '''
        # Get Last Action.
        last = self.movelist.pop()
        undo = last.undo() # Make undo action from this.
        self.apply(undo) # Apply Undo.
            
    def __str__(self):
        string = ""
        for row in range(10) :
            for column in range(10) :
                if ((row % 2 == 0) != (column % 2 == 0)) :
                    idx = self.__cord2idx(row, column)
                    if self.bitmap[idx] == None :
                        string += '.'
                    elif self.bitmap[idx].color == 'DARK' :
                        if self.bitmap[idx].is_king :
                            string += '#'
                        else :
                            string += 'X'
                    else :
                        if self.bitmap[idx].is_king :
                            string += '$'
                        else :
                            string += 'O'
                else :
                    string += '.'
            string += '\n'
        return string

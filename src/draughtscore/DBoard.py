'''
Created on Jul 21, 2011

@author: Davide Aversa
'''
from draughtscore.DPiece import DPiece

class DBoard(object):
    '''
    Class for Draughts board.
    '''
    
    def __init__(self):
        '''
        Constructor. Initialize an empty draughts board with 
        the pieces in starting position.
        '''
        self.light_pieces = []
        self.dark_pieces = []
        self.bitmap = [None] * 50 # None = empty
        self.movelist = []
        
        # Add 20 Dark Piece in starting position.
        row = 0
        column = 1
        delta = 1
        for _ in xrange(20) :
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
        for _ in xrange(20) :
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
        # If row%2 == 0 (column-1)/2 else column/2
        # This should be equivalent...
        return 5 * row + column / 2
            
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
        if row < 0 or row >= 10 :
            return False
        if column < 0 or column >= 10 :
            return False
 
        if self.bitmap[self.__cord2idx(row, column)] :
            return False
        
        return True
        
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
    
    def apply(self, action, chain=False):
        '''
        Apply an action to the board.
        
        Note that in Chain-Capture *only* the first step must be recorded
        in board undo-stack. So use the `chain` flag to apply chain next
        steps.
        
        ARGS:
            @param action: Action to apply. 
            @param chain: True if action is one step of a chain action.
        '''
        # If ACTION is UNDO-type DO NOT add to undo-list.
        if action.type != 'UNDO' and not chain :
            self.movelist.append(action)
            
        # Get Source and Destination.
        srow, scol = action.source
        drow, dcol = action.destination
        
        # Get Piece in Source.
        piece = self.get_piece(srow, scol)
        
        if piece == None : #If no piece is in source->ERROR.
            raise Exception("NO PIECE IN SOURCE!")
        
        piece.move(drow, dcol) #Move piece in destination.
        
        # Check Promotion: Promote only if `action` is a final-step.
        if action.promote and not action.next :
            piece.promote()
        
        if action.type == 'CAPTURE' or action.type == 'CHAIN' :
            # If action is CAPTURE-type get captured piece. 
            captured = action.captured
            captured.captured() #Remove captured piece from board.
            if captured.color == 'LIGHT' : #... and from right list.
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
        
        # If chain-capture (or chain-undo) apply next step.
        if action.next :
            self.apply(action.next, chain=True) # Record only the first step.
        
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
                break
        
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
        Static Evaluation Function for Draughts Board.
        
        ARGS:
            @param weights: Dictionary of Weights for each feature.
        
        RETURN:
            @return: The board score.
        '''
        ## Avoid Frequent Look-Up
        ##
        get_features = DPiece.get_features
        ##
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
            features = get_features(piece)
            for f in features :
                vlight[f] += 1
                
        for piece in self.dark_pieces :
            features = get_features(piece)
            for f in features :
                vdark[f] += 1
            
        score_light = sum([vlight[key] * weights[key] for key in weights.iterkeys()])
        score_dark = sum([vdark[key] * weights[key] for key in weights.iterkeys()])
        
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
        for row in xrange(10) :
            for column in xrange(10) :
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

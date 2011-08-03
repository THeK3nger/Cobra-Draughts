'''
Created on Jul 21, 2011

@author: Davide Aversa
'''
from draughtscore.DBoard import DBoard
import random

class DraughtsBrain(object):
    '''
    Class AI for Draughts.
    
    Use Min-Max with Alpha-Beta Prune.
    '''

    def __init__(self, weights, horizon, weights_bis=None):
        '''
        Constructor
            
        ARGS:
            @param weights: Weights for board Static-Evaluation-Function.
            @param horizon: Max level for the search algorithm. 
            @param weights_bis: Weights for the dark-side AI. 
        '''
        self.weights = weights
        self.horizon = horizon
        
        self.move = 0
        self.board = DBoard()
        self.turn = 'LIGHT'
        
        self.gameover = False
        self.winner = None
        self.nocapturecounter = 0 # Move without a capture.
        
        self.verbose = False
        
        if weights_bis == None :
            self.weights_bis = self.weights
        else :
            self.weights_bis = weights_bis            
    
    def reset(self):
        self.move = 0
        self.board = DBoard()
        self.turn = 'LIGHT'
        self.gameover = False
        self.nocapturecounter = 0
    
    def switch_turn(self):
        '''
        Switch current in-game player.
        '''
        if self.turn == 'LIGHT' :
            self.turn = 'DARK'
        else :
            self.turn = 'LIGHT'
    
    def _switch_player(self, player):
        '''
        Switch player tag.
        
        ARGS:
            @param player: Current player.
        
        RETURN:
            @return: Next Player.
        '''
        if player == 'LIGHT' :
            return 'DARK'
        else :
            return 'LIGHT'
               
    def run_self(self):
        '''
        Execute "selfish" AI vs. AI match.
        '''
        self.gameover = False
        while not self.gameover and self.nocapturecounter < 100 :
            bestmove = self.best_move()
            if not bestmove :
                self.winner = self._switch_player(self.turn) # No valid move!
                break
            self.apply_move(bestmove)
            if self.verbose : 
                print(self.board)
                print(self.board.board_score(self.weights))
        if not self.gameover : # So, too-much noncapture.
            self.winner = 'DRAW'
        return self.winner
                
    def apply_move(self, action):
        '''
        Apply an action to board.
        
        ARGS:
            @param action: Action that it's going to be executed.
        '''
        self.board.apply(action)
        self.move += 1
        if len(self.board.light_pieces) == 0 :
            self.gameover = True
            self.winner = 'DARK'
        elif len(self.board.dark_pieces) == 0 :
            self.gameover = True
            self.winner = 'LIGHT'
        else :
            self.switch_turn()
            if action.type != 'CAPTURE' :
                self.nocapturecounter += 1
            else :
                self.nocapturecounter = 0        
                
    ########
    ## AI ##
    ########
    
    def best_move(self):
        '''
        Find the next best move according current player state.
        
        This method use the Min-Max algorithm wit Alpha-Beta pruning system
        to minimize the number of explored nodes.
        
        RETURN:
            @return: One of the best move.
        '''
        if len(self.board.all_move(self.turn)) == 0 :
            self.gameover = True
            self.winner = self._switch_player(self.turn)
            return None
            
        self.path = []
        if self.turn == 'LIGHT' :
            value = self.alphabeta(-float('inf'), float('inf'), self.horizon, self.turn, self.weights)
        else :
            value = self.alphabeta(-float('inf'), float('inf'), self.horizon, self.turn, self.weights_bis)
        
        bestmoves = []
        
        for element in self.path :
            if element[1] == value : # Find path with value equal to best-value.
                bestmoves.append(element[0])
        else :
            if len(bestmoves) == 0 and len(self.path) != 0 : # If path is not empty return first value.
                print("Woops!")
                return self.path[0][0] # WARNING: This code should never be executed.
        
        selected_move = random.choice(bestmoves) # Select randomly a move among the best ones.
        return selected_move
                
    def alphabeta(self, alpha, beta, level, player, weights):
        '''
        THE GLORIOUS ALPHA-BETA ALGORITHM. GLORIFY HIM.
        
        ARGS:
            @param aplha: Current Alpha Value.
            @param beta: Current Beta Value.
            @param level: Current Level.
            @param player: Current Player.
            @param weights: Set of weights to use. TODO: Can remove this?
        
        RETURN    
        '''
        if level == 0 :
            value = self.board.board_score(weights)
            self.path.append((self.board.movelist[self.move], value))
            return value
        if player == 'LIGHT' :
            moves = self.board.all_move(player)
            v = -float('inf')
            for mov in moves :
                self.board.apply(mov)
                v = max(v, self.alphabeta(alpha, beta, level - 1, self._switch_player(player), weights))
                self.board.undo_last()
                if beta <= v :
                    return v
                alpha = max(alpha, v)
            if len(moves) == 0 :
                self.path.append((self.board.movelist[self.move], v))
            return v
        else :
            moves = self.board.all_move(player);
            v = float('inf')
            for mov in moves :
                self.board.apply(mov)
                v = min(v, self.alphabeta(alpha, beta, level - 1, self._switch_player(player), weights))
                self.board.undo_last()
                if v <= alpha :
                    return v
                beta = min(beta, v)
            if len(moves) == 0 :
                self.path.append((self.board.movelist[self.move], v))
            return v
        
                
        

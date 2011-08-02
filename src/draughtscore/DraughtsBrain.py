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


    def __init__(self, type, weights, horizon, weights_bis=None):
        '''
        Constructor
        
        There are two match type:
            * AI -> AI vs AI
            * PLAYER -> AI vs Player
            
        ARGS:
            @param type: Match type.
            @param weights: Weights for board Static-Evaluation-Function.
            @param horizon: Max level for the search algorithm. 
            @param weights_bis: Weights for the dark-side AI. 
        '''
        self.type = type
        self.weights = weights
        self.horizon = horizon
        
        self.move = 0
        self.board = DBoard()
        self.turn = 'LIGHT'
        if weights_bis == None :
            self.weights_bis = self.weights
        else :
            self.weights_bis = weights_bis
        
    def run(self):
        '''
        Start the match according to type.
        '''
        if self.type == 'PLAYER' :
            self.run_player()
        elif self.type == 'AI' :
            self.run_ai()
    
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
    
    def best_move(self):
        '''
        Find the next best move according current player state.
        
        This method use the Min-Max algorithm wit Alpha-Beta pruning system
        to minimize the number of explored nodes.
        
        RETURN:
            @return: One of the best move.
        '''
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
            
    def ask_move(self):
        '''
        Get move from human user.
        '''
        pass
    
    def run_ai(self):
        '''
        Execute AI vs AI match.
        '''
        gameover = False
        win = 0
        no_capt_count = 0
        while not gameover and no_capt_count < 80 :
            bestmove = self.best_move()
            if not bestmove :
                break
            self.apply_move(bestmove)
            if len(self.board.light_pieces) == 0 :
                gameover = True
                win = -1
            elif len(self.board.dark_pieces) == 0 :
                gameover = True
                win = 1
            else :
                self.switch_turn()
                if bestmove.type != 'CAPTURE' :
                    no_capt_count += 1
                else :
                    no_capt_count = 0
            print(self.board)
        print win
            
    
    def run_player(self):
        '''
        Execute Human vs AI match.
        
        TODO: Human Interaction
        '''
        gameover = False
        while not gameover :
            if self.turn == 'LIGHT' :
                pass
                #self.ask_move()
                
    def apply_move(self, action):
        '''
        Apply an action to board.
        
        ARGS:
            @param action: Action that it's going to be executed.
        '''
        self.board.apply(action)
        self.move += 1
                
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
        
                
        

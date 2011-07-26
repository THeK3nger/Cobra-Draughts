'''
Created on Jul 21, 2011

@author: davide
'''
from draughtscore.DBoard import DBoard

class DraughtsBrain(object):
    '''
    Class AI for Draughts.
    
    Use Min-Max with Alpha-Beta Prune.
    '''


    def __init__(self, type, weights, horizon, weights_bis=None):
        '''
        Constructor
        
        Two Type:
            * AI -> AI vs AI
            * PLAYER -> AI vs Player
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
        if self.type == 'PLAYER' :
            self.run_player()
        elif self.type == 'AI' :
            self.run_ai()
    
    def switch_turn(self):
        if self.turn == 'LIGHT' :
            self.turn = 'DARK'
        else :
            self.turn = 'LIGHT'
    
    def switch_player(self, player):
        if player == 'LIGHT' :
            return 'DARK'
        else :
            return 'LIGHT'
    
    def best_move(self):
        self.path = []
        if self.turn == 'LIGHT' :
            value = self.alphabeta(-float('inf'), float('inf'), self.horizon, self.turn, self.weights)
        else :
            value = self.alphabeta(-float('inf'), float('inf'), self.horizon, self.turn, self.weights_bis)
        for element in self.path :
            if element[1] == value :
                print(self.turn + " :: " + str(element[0]))
                return element[0]
            
    def ask_move(self):
        pass        
    
    def run_ai(self):
        gameover = False
        win = 0
        no_capt_count = 0
        while not gameover and no_capt_count < 80 :
            move = self.best_move()
            self.apply_move(move)
            if len(self.board.light_pieces) == 0 :
                gameover = True
                win = -1
            elif len(self.board.dark_pieces) == 0 :
                gameover = True
                win = 1
            else :
                self.switch_turn()
                if move.type != 'CAPTURE' :
                    no_capt_count += 1
                else :
                    no_capt_count = 0
            print(self.board)
            
    
    def run_player(self):
        gameover = False
        while not gameover :
            if self.turn == 'LIGHT' :
                possible_move = self.board.all_move('LIGHT')
                #self.ask_move()
                
    def apply_move(self, action):
        self.board.apply(action)
        self.move += 1
                
    def alphabeta(self, alpha, beta, level, player, weights):
        if level == 0 :
            value = self.board.board_score(weights)
            self.path.append((self.board.movelist[self.move], value))
            return value
        if player == 'LIGHT' :
            moves = self.board.all_move(player)
            v = -float('inf')
            for mov in moves :
                self.board.apply(mov)
                v = max(v, self.alphabeta(alpha, beta, level - 1, self.switch_player(player), weights))
                self.board.undo_last()
                if beta <= v :
                    self.current_best = mov
                    return v
                alpha = max(alpha, v)
            return v
        else :
            moves = self.board.all_move(player);
            v = float('inf')
            for mov in moves :
                self.board.apply(mov)
                v = min(v, self.alphabeta(alpha, beta, level - 1, self.switch_player(player), weights))
                self.board.undo_last()
                if v <= alpha :
                    self.current_best = mov
                    return v
                beta = min(beta, v)
            return v
        
                
        

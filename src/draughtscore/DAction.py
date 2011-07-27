'''
Created on Jul 21, 2011

@author: Davide Aversa
'''

class DAction(object):
    '''
    This Class represent an Action on the Draughts Board.
    
    Exists three type of action:
        * MOVE : Standard Move
        * CAPTURE : Capture Enemy Piece
        * UNDO : Undo Move
        TODO: Chain (?)
    '''


    def __init__(self, type, source, destination, captured=None, promote=False):
        '''
        Constructor
        
        ARGS:
            @param type: Action Type
            @param source: Tuple (row,column) of starting position.
            @param destination: Tuple (row,column) of ending position.
            @param captured: Captured piece (if type is CAPTURE).
        '''
        self.type = type
        self.source = source
        self.destination = destination
        self.captured = captured
        self.promote = promote
        
    def undo(self):
        '''
        Create Undo Action from current Action.
        
        @return: Undo Action
        '''
        return DAction('UNDO', self.destination, self.source, self.captured, self.promote)
    
    def __eq__(self, other):
        if self.type != other.type :
            return False
        if self.source != other.source :
            return False
        if self.destination != other.destination :
            return False
        if self.captured != other.captured :
            return False
        return True
        
    
    def __str__(self):
        return "%s :: <%d , %d> -> <%d , %d>" % (self.type, self.source[0], \
                                                 self.source[1], self.destination[0], \
                                                 self.destination[1])
    
    
        

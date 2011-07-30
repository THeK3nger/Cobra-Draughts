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
        * CHAIN : Chain Captures
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
        self.next = None # Next Capture in `CHAIN`.
        
    def _undochain(self):
        '''
        Returns Undo-Action for `CHAIN` one.
        
        RETURN:
            @return: Undo-Action for Chain-Captures.
        '''
        if self.next == None : # Last element.
            return self._raw_undo()
        
        undo_rest = self.next._undochain() # Invert chain tail.
        undo_this = self._raw_undo() # Invert current step.
        undo_rest._append_capture(undo_this)
        return undo_rest
    
    def _raw_undo(self):
        '''
        Return Raw-Undo-Action.
        
        Don't check difference between MOVE, CAPTURE and CHAIN.
        
        RETURN :
            @return: Undo Action.
        '''
        return DAction('UNDO', self.destination, self.source, self.captured, self.promote)
    
    def _append_capture(self,action):
        '''
        Append an item in Chain-Captures at the end of chain.
        
        ARGS:
            @param action: Action to append.
        '''
        p = self
        while p.next :
            p = p.next
        p.next = action
              
    def undo(self):
        '''
        Create Undo Action from current Action.
        
        RETURN:
            @return: Undo Action
        '''
        if self.type == 'CHAIN' :
            return self._undochain()
        else :
            return self._raw_undo()
    
    def __eq__(self, other):
        if other == None :
            return False
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
    
    
        

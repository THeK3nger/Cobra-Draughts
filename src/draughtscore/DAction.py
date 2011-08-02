'''
Created on Jul 21, 2011

@author: Davide Aversa
'''

class DAction(object):
    '''
    This Class represent an Action on the Draughts Board.
    
    Exists three type of action:
        * MOVE : Standard Move
        * CAPTURE : Capture Enemy Piece - Can be a Chain Capture.
        * UNDO : Undo Move
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
        self.next = None # Next Capture if `CAPTURE` is a Chain-Capture.
    
    def _append_capture(self, action):
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
        raw_undo = DAction('UNDO', self.destination, self.source, self.captured, self.promote)
        
        if self.next == None : # Last element.
            return raw_undo
        
        undo_rest = self.next.undo() # Invert chain tail.
        undo_this = raw_undo # Invert current step.
        undo_rest._append_capture(undo_this)
        return undo_rest
    
    def copy(self):
        return DAction(self.type,self.source,self.destination,self.captured,self.promote)
    
    def __len__(self):
        if self.next :
            return 1 + len(self.next)
        return 1
    
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
        
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "%s :: <%d , %d> -> <%d , %d> { %s }" % (self.type, self.source[0], \
                                                 self.source[1], self.destination[0], \
                                                 self.destination[1], \
                                                 str(self.next))
    
    
        

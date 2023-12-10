

import numpy as np

# A board is represented by a 3x3 numpy array of integers
# Each value on the board is either 0 - Empty cell
#                                   1 - Marked 'X'
#                                   2 - Marked '0'

# Every move is represented by an index from 0 to 8 where it should be played (use row-major linearization)

class TicTacToeBoard:
    
    def __init__(self, **kwargs):
        if('copyFrom' in kwargs.keys()):
            other = kwargs['copyFrom']
            self.board = other.board.copy()
            self.nextTurn = other.nextTurn
            self.moveHistory = other.moveHistory[:]
            return    
        
        self.board = np.zeros(shape=(9,), dtype=np.uint8)
        
        self.nextTurn = self.Xmark
        
        self.moveHistory = list()
    


#                CLASS PROPETIES
#######################################################
    Xmark = 1
    Ymark = 2
    
    WinPatterns = [
                    slice(0,3),         # row 1
                    slice(3,6),         # row 2
                    slice(6,9),         # row 3
                    slice(0,9,3),       # col 1
                    slice(1,9,3),       # col 2
                    slice(2,9,3),       # col 3
                    np.array((0,4,8)),  # diag 1
                    np.array((2,4,6))   # diag 2
                  ]
#######################################################
    
    
    # Checks if anyone has won the game.
    # Returns Xmark/Ymark if either player won, otherwise returns 0.
    # If the position is illegal (i.e. more than 1 3-in-a-row reached),
    # ... then return value may be either player.
    def checkWin(self):
        
        # If less than 5 moves have been made => no winner.
        if(np.sum(self.board > 0) < 5):
            return 0
        
        for idxs in self.WinPatterns:
            if((self.board[idxs]==self.Xmark).all()):
                return self.Xmark
            if((self.board[idxs]==self.Ymark).all()):
                return self.Ymark
        
        return 0
            
        
    # Makes a move for the player 'self.nextTurn' at the position 'pos'
    def move(self, pos):
        try:
            assert self.board[pos] == 0
            self.board[pos] = self.nextTurn
            #assert self.board[pos//3,pos%3] == 0
            #self.board[pos//3, pos%3] = self.nextTurn
            
            self.changeTurn()
            self.moveHistory.append(pos)
            
        except (TypeError,IndexError,ValueError):
            msg = "In call to move(), pos must be an integer in [0,8]. Received '{}'"
            msg = msg.format(pos)
            raise ValueError(msg)
        
        except AssertionError:
            msg = "In call to move({}), the board is already marked {} at position {}"
            val = self.board[pos//3, pos%3]
            msg = msg.format(pos, val, pos)
            raise ValueError(msg)
            
        
    def undoLastMove(self):
        lpos = self.moveHistory.pop()
        self.board[lpos] = 0
        self.changeTurn()
        
        
    # Returns a list of all possible next moves
    def possibleNextMoves(self):
        ret = np.nonzero(self.board==0)[0]
        return ret
        
    # Updates whose turn it is
    def changeTurn(self):
        self.nextTurn = self.Xmark if(self.nextTurn==self.Ymark) else self.Ymark
        
    
    # Returns the other player w.r.t self.nextTurn
    def getOtherMark(self):
        return (self.Ymark if(self.nextTurn==self.Xmark) else self.Xmark)
    
    
    def __repr__(self):
        ret = ''
        for i in range(3):
            for j in range(3):
                ret += ' ' + str(self.board[3*i + j])
            ret += '\n'
        return ret
    
    def __eq__(self, other):
        ret =   (self.board == other.board) and \
                (self.nextTurn == other.nextTurn) and \
                (self.moveHistory == other.moveHistory)
        return ret
                
                
                
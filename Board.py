

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
    Xmark = 1   # must never be set to 0
    Ymark = 2   # must never be set to 0
    
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
    # If the position is illegal with more than 1 instance of a 3-in-a-row, then
    #   ... the output may be either player depending on whose 3-in-a-row is found first
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
            val = self.board[pos]
            msg = msg.format(pos, val, pos)
            raise ValueError(msg)
            
    # Uses self.moveHistory to reset the board to its state before the most recent move.
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
    
    
    # Pretty printing of a board
    def show(self, Xchar='X', Ychar='O'):
        symbol = {
              0        :  " ",
              self.Xmark :  Xchar,
              self.Ymark :  Ychar
              }
        
        ret = ""
        for i in range(3):
            for j in range(3):
                ret += " " + symbol[self.board[3*i+j]] + " |"
            if(i!=2):
                ret = ret[:-1] + "\n" + "-"*11 + "\n"
            else:
                ret = ret[:-1] + '\n'
                
        print(ret)
        
        
    def __eq__(self, other):
        ret =   (self.board == other.board).all() and \
                (self.nextTurn == other.nextTurn) # and \
                # (self.moveHistory == other.moveHistory)
        return ret
                
    



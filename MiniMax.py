
import numpy as np
from Board import TicTacToeBoard


# returns which next moves lead to: X will win, Y will win, other
# returned value is an array of 9 elements where:
    # arr[i] = X,       if playing position 'i' will lead to Y eventually winning.
    # arr[i] = Y,       if playing position 'i' will lead to Y eventually winning.
    # arr[i] = X+Y+1,   if playing position 'i' is an illegal move (it's already filled with X or 0)
    # arr[i] = X+Y+3,   if playing position 'i' will lead to open-ended result
def minimax(tb:TicTacToeBoard) -> (list,list,list):
    (X,Y) = (tb.Xmark, tb.Ymark)
    
    ret = np.zeros(9,dtype=np.uint8)
    ret[:] = (X + Y + 1)
    
    nextMoves = tb.possibleNextMoves()
    
    for pos in nextMoves:
        
        tb.move(pos)
        
        winVal = tb.checkWin()
        if(winVal==X):
            ret[pos] = X
        elif(winVal==Y):
            ret[pos] = Y
        else:
            remMoves = tb.possibleNextMoves()
            if(remMoves.size>0):
                z = minimax(tb)
                if((z[remMoves]==X).all()):
                    ret[pos] = X
                elif((z[remMoves]==Y).all()):
                    ret[pos] = Y
                else:
                    ret[pos] = (X + Y + 3)
            else:
                ret[pos] = (X + Y + 3)
        
        tb.undoLastMove()
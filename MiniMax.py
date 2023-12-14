
import numpy as np

from Board import TicTacToeBoard



# returns which next moves lead to: will win, will lose, other
# returned value is an array of 9 elements where:
    # arr[i] = 1,       if playing position 'i' will lead to a forced win.
    # arr[i] = -1,       if playing position 'i' will lead to a loss with best play from opponent
    # arr[i] = 0,   if playing position 'i' will lead to open-ended result
    # arr[i] = 8,   if playing position 'i' is an illegal move (it's already filled with X or 0)
def minimax(tb : TicTacToeBoard, myMark, otherMark):
    
    ret  = np.zeros(9, dtype=np.int8)
    ret[:] = 8
    
    nextMoves = tb.possibleNextMoves()
    for mv in nextMoves:
        
        tb.move(mv)
        
        if(tb.checkWin()==myMark):
            ret[mv] = 1
        else:
            remMoves = tb.possibleNextMoves()
            if(remMoves.size>0):
                Z = minimax(tb, myMark = otherMark, otherMark = myMark)
                if(np.any(Z[remMoves]==1)):
                    ret[mv] = -1
                elif(np.all(Z[remMoves]==-1)):
                    ret[mv] = 1
                else:
                    ret[mv] = 0
            else:
                ret[mv] = 0
        tb.undoLastMove()

    return ret


# Run the minimax algorithm, but produce the results of all evaluations in the position tree
# Yields (tb,Z) for every position checked in the tree of next positions
#       tb: The TicTacToeBoard
#       Z : The minimax vector evaluation of the position tb
# Does not yield evaluations for a position that is won
# The last pair (tb,Z) yielded will correspond to the input position to the fn.

def minimaxAllContinuations(tb : TicTacToeBoard, myMark, otherMark):
    ret = np.zeros(9, dtype=np.int8)
    ret[:] = 8
    
    nextMoves = tb.possibleNextMoves()
    for mv in nextMoves:
        
        tb.move(mv)
        if(tb.checkWin() == myMark):
            ret[mv] = 1
        else:
            remMoves = tb.possibleNextMoves()
            if(remMoves.size>0):
                for Y in minimaxAllContinuations(tb, otherMark, myMark):
                    yield Y
                Z = Y[1]
                if(np.any(Z[remMoves]==1)):
                    ret[mv] = -1
                elif(np.all(Z[remMoves]==-1)):
                    ret[mv] = 1
                else:
                    ret[mv] = 0
            else:
                ret[mv] = 0
        tb.undoLastMove()
        
    yield tb,ret
            

# Show for each of the remaining moves, what result it'll lead to with best play
# Calls minimax() internally
def showCalc(tb:TicTacToeBoard):
    orig = tb
    tb = TicTacToeBoard(copyFrom=orig)
    
    res = minimax(tb, tb.nextTurn, tb.getOtherMark())
    
    LUT = {1:'W', -1:'L', 0:'0'}
    ret = str(tb.nextTurn) + " to move:\n"
    for i in range(3):
        for j in range(3):
            k = 3*i + j
            ret += ' '
            ret += (str(tb.board[k]) if(tb.board[k]!=0) else LUT[res[k]])
        ret += '\n'
        
    print(ret)
    

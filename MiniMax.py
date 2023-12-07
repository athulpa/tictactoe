
import numpy as np

from Board import TicTacToeBoard



# returns which next moves lead to: will win, will lose, other
# returned value is an array of 9 elements where:
    # arr[i] = 1,       if playing position 'i' will lead to a forced win.
    # arr[i] = -1,       if playing position 'i' will lead to a loss with best play from opponent
    # arr[i] = 8,   if playing position 'i' is an illegal move (it's already filled with X or 0)
    # arr[i] = 0,   if playing position 'i' will lead to open-ended result
def minimax(tb:TicTacToeBoard, myMark, otherMark):
    #assert myMark == tb.nextTurn
    
    ret  = np.zeros(9, dtype=np.int8)
    ret[:] = 8
    
    nextMoves = tb.possibleNextMoves()
    
    for mv in nextMoves:
        #l = len(tb.moveHistory)
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
        #assert len(tb.moveHistory)==l
        
    return ret


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
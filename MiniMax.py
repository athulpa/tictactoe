
import numpy as np

from Board import TicTacToeBoard


# Returns the evaluation of the current position 
#   ... if both sides play the best moves from here
#       Return  1, if the position is winning for X (i.e. who played the first move)
#       Return -1, if the position is winning for Y (i.e. who played the second move)
#       Return  0, if it's a draw
def minimax(tb : TicTacToeBoard):
    cW = tb.checkWin()
    if(cW == tb.Xmark):
        return 1
    elif(cW == tb.Ymark):
        return -1
    nextMoves = tb.possibleNextMoves()
    vals = list()
    for mv in nextMoves:
        tb.move(mv)
        
        Z = minimax(tb)
        
        tb.undoLastMove()
        vals.append(Z)
    
    if(tb.nextTurn == tb.Xmark and (1 in vals)):
        return 1
    if(tb.nextTurn == tb.Ymark and (-1 in vals)):
        return -1
    if(len(nextMoves)==0 or (0 in vals)):
        return 0
    if(tb.nextTurn == tb.Xmark):
        return -1
    if(tb.nextTurn == tb.Ymark):
        return 1
    

# Same output as the minimax() function but faster because it prunes the recursion tree
def minimax_AlphaBetaPruning(tb : TicTacToeBoard, parentFoundADraw=False):
    cW = tb.checkWin()
    if(cW == tb.Xmark):
        return 1
    elif(cW == tb.Ymark):
        return -1

    nextMoves = tb.possibleNextMoves()
    if(len(nextMoves) == 0):
        return 0
    
    foundADraw = False
    for mv in nextMoves:
        tb.move(mv)
        Z = minimax_AlphaBetaPruning(tb, foundADraw)
        tb.undoLastMove()
        
        if(Z==0):
            foundADraw = True
        
        # When the next player can win
        if(tb.nextTurn == tb.Xmark and (Z == 1)):
            return 1
        if(tb.nextTurn == tb.Ymark and (Z == -1)):
            return -1
        
        if(Z==0):
            foundADraw = True
            if(parentFoundADraw):
                return 0
            
    # When the next player can't win but can draw
    if(foundADraw):
        return 0
    
    # When the next player can't win or draw
    return (    (-1) if (tb.nextTurn == tb.Xmark) else (1)  )
    


# Return the minimax() evaluations for all moves of the given board
# Returns an array 'arr' such that for all positions 'i' in [0-8],
#       arr[i] is the evaluation of the board after playing the next move at 'i'
#       arr[i] is 8 if the next move can't be played at 'i'
def minimaxEvalsForNextMoves(tb, pruning=True):
    ret = np.zeros(shape=9, dtype=np.int8) + 8
    for i in range(9):
        if(i in tb.possibleNextMoves()):
            tb.move(i)
            
            if(pruning):
                ret[i] = minimax_AlphaBetaPruning(tb)
            else:
                ret[i] = minimax(tb)
                
            tb.undoLastMove()

    return ret
    


# Run the minimax algorithm, but produce the results of all evaluations in the position tree
# NOTE: It does not call minimax(); minimax algo is baked into this fn itself
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
    

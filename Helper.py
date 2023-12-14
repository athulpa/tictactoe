
import numpy as np

from Board import TicTacToeBoard
## Contains misc. functions that don't belong in other files


# Construct a T-Board object from a given board vector
# The move history is also valid for the returned T-Board
def makeBoardFromPosition(vec):
    tb = TicTacToeBoard()
    xpos = np.nonzero(vec==tb.Xmark)[0]
    ypos = np.nonzero(vec==tb.Ymark)[0]
    
    lx,ly = len(xpos),len(ypos)
    if(lx>9 or ly>9 or lx<ly or lx>(ly+1)):
        msg = "In makeBoardFromPosition({}), this board cannot ".format(vec) + \
                " arise from any legal sequence of moves in TicTacToe"
        raise ValueError(msg)
        
    i = -1 # for boards with only 1 move played (which will be for X). See the if-condition below.
    for i in range(len(ypos)):
        tb.move(xpos[i])
        tb.move(ypos[i])
    if(len(xpos) > len(ypos)):
        tb.move(xpos[i+1])
    return tb



# Construct a T-Borad object from a given board vector when that 
# ... vector's position cannot be reached from any legal game.
# USE JUDICIOUSLY AND CAREFULLY (when no other workaround is feasible)
def makeBoardFromIllegalPosition(vec):
    tb = TicTacToeBoard()
    tb.board = vec
    return tb
    
    
# Given a T-Board object, generate all of the possible positions that can follow from it.
# Returns a generator object that yields each position one-by-one.
# May modify the input board in-place during the generation, but leaves it as-is by the end.
# REMARK: The generated continuations may not all have different positions, 
#           ... since you can get the same position in many move-orders.
def generateAllPossibleContinuations(tb : TicTacToeBoard):
    for mv in tb.possibleNextMoves():
        tb.move(mv)
        yield tb
        for nxt in generateAllPossibleContinuations(tb):
            yield nxt
        tb.undoLastMove()
        

# Generate all possible T-Board positions (there are 3**9=19683 of them)
def generateAllPossiblePositions():
    for N in range(3**9):
        l = []
        for i in range(9):
            l.append(N%3)
            N //= 3
        try:
            ret = makeBoardFromPosition(np.array(l, dtype=np.uint8))
            yield ret
        except ValueError:
            continue
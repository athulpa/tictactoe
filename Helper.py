
import numpy as np

from Board import TicTacToeBoard
## Contains misc. functions that don't belong in other files


# Construct a T-Board object from a given board vector
# The move history is also valid for the returned T-Board
def boardFromPosition(vec):
    tb = TicTacToeBoard()
    xpos = np.nonzero(vec==tb.Xmark)[0]
    ypos = np.nonzero(vec==tb.Ymark)[0]
    for i in range(len(ypos)):
        tb.move(xpos[i])
        tb.move(ypos[i])
    if(len(xpos) > len(ypos)):
        tb.move(xpos[i+1])
    return tb


# Given a T-Board object, generate all of the possible positions that can follow from it.
# May modify the input board in-place during the generation, but leaves it as-is by the end
def getAllPossibleContinuations(tb : TicTacToeBoard):
    for mv in tb.possibleNextMoves():
        tb.move(mv)
        yield tb
        for nxt in getAllPossibleContinuations(tb):
            yield nxt
        tb.undoLastMove()
        

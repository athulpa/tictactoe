
#       Boilerplate for path-relative Imports
#########################################################################
import os
cdir = os.getcwd()
if("Board.py" not in os.listdir(".")):
    os.chdir("./..")
if("Board.py" not in os.listdir(".")):
    msg = "Must run tests from the project's root directory or" + \
            "the /test directory. Now ran from: {}".format(cdir)
    raise RuntimeError(msg)
#########################################################################


import numpy as np

from Board import TicTacToeBoard
from Symmetry import transformBoard, newIndex, oldIndex


# Check whether the values in newIndex[[]] are correct
def tNewIndex():
    for op in range(8):
        for i in range(9):
            tb = TicTacToeBoard()
            tb.move(i)
            newTb = transformBoard(tb, op)
            gtruth = np.nonzero(newTb.board == tb.Xmark)[0][0]
            data = newIndex(i,op)
            if(gtruth != data):
                print("Failed for operation {} on:".format(op))
                tb.show()
                return False
    return True
            

# Check whether the getOldIndex() fn. also works.
def tOldIndex():
    for op in range(8):
        for i in range(9):
            tb = TicTacToeBoard()
            tb.move(i)
            newTb = transformBoard(tb, op)
            gtruth = i
            newIdx = np.nonzero(newTb.board == tb.Xmark)[0][0]
            data = oldIndex(newIdx,op)
            if(gtruth != data):
                print("Failed for operation {} on:".format(op))
                tb.show()
                return False
    return True

